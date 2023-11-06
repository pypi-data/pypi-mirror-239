import os
import sys
import torch
from torch import nn
import numpy as np
from ..utils import gen_groups_dist, modules_to_devices, wrap_modules_data_parallel, wrap_modules_relocation, wrap_data_parallel, wrap_modules_checkpoint
from ..utils import read_json_config, config2strategy, str2array
from ..pipeline import PipelineParallel, PipeSequential
from flash_attn.modules.block import Block

def get_chunks(args):
    if args.chunks == -1:
        args.chunks = 1
        if args.pp_deg > 1:
            world_size = torch.distributed.get_world_size()
            max_dp_deg = world_size // args.pp_deg
            local_bsz = args.global_train_batch_size // max_dp_deg
            optimal_micro_bsz = np.ceil(local_bsz / 4)
            optimal_micro_bsz = 1 if optimal_micro_bsz == 0 else optimal_micro_bsz
            args.chunks = int(optimal_micro_bsz)
    return args.chunks

def overwrite_megatron_args(config, args):
    args.hidden_size = config.hidden_size
    args.num_layers = config.num_hidden_layers
    args.num_attention_heads = config.num_attention_heads
    # args.ffn_hidden_size = config.intermediate_size
    args.max_position_embeddings = config.max_position_embeddings
    # args.attention_dropout = config.attention_probs_dropout_prob
    # args.hidden_dropout = config.hidden_dropout_prob
    args.use_cpu_initialization = True

def get_hybrid_parallel_configs(args):
    local_rank = args.local_rank
    world_size = torch.distributed.get_world_size()
    config_type = 'JSON' if args.galvatron_config_path not in [None,'None'] else 'PYTHON' if args.apply_strategy else 'GLOBAL'
    if local_rank == 0:
        print('======================== Galvatron Parallel Config =============================')
        print('Galvatron parallel config mode: [%s config mode]'%config_type)
    if config_type == 'GLOBAL':
        pp_deg = args.pp_deg
        tp_sizes_enc = [args.global_tp_deg] * args.num_hidden_layers if args.global_tp_deg > 0 else [1]*args.num_hidden_layers
        tp_consecutive_flags = [args.global_tp_consec] * args.num_hidden_layers if args.global_tp_consec in [0, 1] else [1]*args.num_hidden_layers
        dp_types_enc = args.num_hidden_layers * [args.fsdp]
        checkpoint_flags_enc = [args.global_checkpoint] * args.num_hidden_layers
    else:
        if config_type == 'JSON':
            galvatron_config = read_json_config(args.galvatron_config_path)
            pp_deg, tp_sizes_enc, tp_consecutive_flags, dp_types_enc = config2strategy(galvatron_config)
            bsz, chunks = galvatron_config['global_bsz'], galvatron_config['chunks']
            if 'checkpoint' in galvatron_config.keys():
                checkpoint_flags_enc = str2array(galvatron_config['checkpoint'])
            else:
                checkpoint_flags_enc = [0] * len(tp_sizes_enc)
            config_source = 'Galvatron JSON config %s'%args.galvatron_config_path
        if local_rank == 0 and (args.num_hidden_layers != len(tp_sizes_enc) or args.chunks != chunks or args.global_train_batch_size != bsz):
            print('[Notice] The following hyper-parameters will be overwritten by Galvatron %s config:'%config_type)
            if args.global_train_batch_size != bsz:
                print('   global_batch_size =', bsz)
            if args.chunks != chunks:
                print('   chunks =', chunks)
            if args.num_hidden_layers != len(tp_sizes_enc):
                print('   num_hidden_layers =', len(tp_sizes_enc))
        args.global_train_batch_size = bsz
        args.chunks = chunks
        args.num_hidden_layers = len(tp_sizes_enc)

    avg_num_layers = args.num_hidden_layers // pp_deg
    pp_ranks_enc = []
    for i in range(pp_deg):
        pp_ranks_enc += [i] * avg_num_layers

    assert args.global_train_batch_size % (world_size//pp_deg) == 0, 'global_train_batch_size should be multiple of world_size//pp_deg!'
    if local_rank == 0:
        if config_type == 'GLOBAL':
            print('[GLOBAL config mode] Loaded global hybrid parallel strategy:')
            dp_type = 'sdp' if args.fsdp else 'dp'
            tp_deg, tp_consec = tp_sizes_enc[0], tp_consecutive_flags[0]
            dp_deg = world_size//args.global_tp_deg//args.pp_deg
            print('   global_batch_size: %d, chunks: %d'%(args.global_train_batch_size, get_chunks(args)))
            print('   pp_deg: %d, tp_deg: %d, %s_deg: %d, tp_consecutive_flag: %d, checkpoint_flag: %d'%(pp_deg, tp_deg, dp_type, dp_deg, tp_consec, args.global_checkpoint))
        else:
            print('[%s config mode] Loaded hybrid parallel config from %s:'%(config_type, config_source))
            print('   global_batch_size: %d, chunks: %d, pp_deg: %d'%(args.global_train_batch_size, args.chunks, pp_deg))
            print('   tp_sizes_enc:\t', tp_sizes_enc)
            print('   tp_consecutive_flags:', tp_consecutive_flags)
            print('   dp_types_enc:\t', dp_types_enc)
            print('   checkpoint_flags:\t', checkpoint_flags_enc)
        print('================================================================================')
    hybrid_parallel_configs =   {'pp_deg':pp_deg,
                                'tp_sizes_enc':tp_sizes_enc,
                                'tp_consecutive_flags':tp_consecutive_flags,
                                'dp_types_enc':dp_types_enc,
                                'pp_ranks_enc':pp_ranks_enc,
                                'checkpoint_flags_enc':checkpoint_flags_enc}
    return hybrid_parallel_configs

def construct_hybrid_parallel_model(model, model_config, training_args, hybrid_parallel_configs):
    gpt_model, config, args, hp_configs = model, model_config, training_args, hybrid_parallel_configs
    pp_deg, tp_sizes_enc, tp_consecutive_flags, dp_types_enc, pp_ranks_enc, checkpoint_flags_enc = \
        hp_configs['pp_deg'], hp_configs['tp_sizes_enc'], hp_configs['tp_consecutive_flags'], hp_configs['dp_types_enc'], hp_configs['pp_ranks_enc'], hp_configs['checkpoint_flags_enc']
    assert config.num_hidden_layers == len(tp_sizes_enc)
    assert config.num_hidden_layers == len(dp_types_enc) 
    assert config.num_hidden_layers == len(pp_ranks_enc)
    assert config.num_hidden_layers == len(checkpoint_flags_enc)
    world_size = torch.distributed.get_world_size()
    for tp_size in tp_sizes_enc:
        assert tp_size <= world_size//pp_deg and (world_size//pp_deg) % tp_size == 0 and tp_size >= 1, 'Wrong tp_size!'
    for dp_type in dp_types_enc:
        assert dp_type == 0 or dp_type == 1 or dp_type is None, 'Wrong dp_type!'
    for pp_rank in pp_ranks_enc:
        assert pp_rank >= 0 and pp_rank <= pp_deg - 1, 'Wrong pp_rank!'

    # [Step 0] Construct sizes & groups
    # Construct tp_sizes / dp_types / pp_stages for whole model
    tp_sizes_whole_model = [1] + tp_sizes_enc + [1, 1]
    dp_types_whole_model = [0] + dp_types_enc + [0, 0]
    pp_ranks_whole_model = [0] + pp_ranks_enc + [pp_deg-1, pp_deg-1]
    tp_consecutive_whole_model = [1] + tp_consecutive_flags + [1, 1]
    # Construct pp_group / tp_groups / dp_groups / allgather_groups / slice_funcs
    pp_group, tp_groups_whole_model, dp_groups_whole_model, allgather_groups_whole_model, slice_funcs_whole_model = gen_groups_dist(tp_sizes_whole_model, pp_deg, tp_consecutive_whole_model, show_rank = 0)
    tp_groups_enc = tp_groups_whole_model[1:-2]

    # # [Step 1] Construct Tensor Parallel Block based on tp_groups
    from flash_attn.models.gpt import create_mixer_cls, create_mlp_cls
    factory_kwargs = {'device': 'meta' if args.initialize_on_meta else 'cpu', 'dtype': None}
    for i in range(config.num_hidden_layers):
        layer = gpt_model.transformer.layers[i]
        setattr(layer, 'mixer', create_mixer_cls(config, layer_idx=i, process_group=tp_groups_enc[i].group, **factory_kwargs)(config.hidden_size))
        setattr(layer, 'mlp', create_mlp_cls(config, layer_idx=i, process_group=tp_groups_enc[i].group, **factory_kwargs)(config.hidden_size))

    # [Step 2] Construct Sequantial modules
    from .Llamamodel_pipeline import LlamaEmbeddings_, LlamaLayers_, LlamaPreNorm_, LlamaCls_
    model = PipeSequential()
    model.add_module('embeddings', LlamaEmbeddings_(gpt_model))
    for i in range(config.num_hidden_layers):
        enc = LlamaLayers_(gpt_model, i, i + 1)
        model.add_module('layer_%d'%i, enc)
    model.add_module('prenorm', LlamaPreNorm_(gpt_model))
    model.add_module('cls', LlamaCls_(gpt_model))

    # [Step 3] Wrap Relocation modules if necessary
    model = wrap_modules_relocation(model, allgather_groups_whole_model, slice_funcs_whole_model)

    # [Step 4] Construct Pipeline Module and place the layers on corresponding devices
    chunks = get_chunks(args)
    seq_len, hidden_size = args.seq_length, args.hidden_size
    layer_output_tensor_shapes = [None] + [[[-1,seq_len,hidden_size], [-1,seq_len]]] * config.num_hidden_layers + [None] * 2
    mixed_precision = {'fp32': torch.float, 'fp16': torch.float16, 'bf16': torch.bfloat16}[args.mixed_precision]
    layer_output_tensor_dtypes = [None] + [[mixed_precision, torch.long]] * config.num_hidden_layers + [None] * 2
    layer_dp_sizes = [world_size // pp_deg // tp_size for tp_size in tp_sizes_whole_model]
    hp_model = PipelineParallel(
                model = model, 
                model_ranks = pp_ranks_whole_model, 
                layer_output_tensor_shapes = layer_output_tensor_shapes, 
                layer_output_tensor_dtypes = layer_output_tensor_dtypes,
                layer_dp_sizes = layer_dp_sizes, 
                chunks=args.chunks, 
                process_group = pp_group.ranks, 
                nproc_per_node=8,
                info=False)

    # [Step 5] Wrap Data Parallel modules based on dp_types & dp_groups
    module_types = ['embed'] + ['gpt_dec']*config.num_hidden_layers + ['norm', 'cls']
    hp_model.wrap_pipeline_modules_data_parallel(dp_types_whole_model, dp_groups_whole_model, module_types=module_types, mixed_precision=mixed_precision, wrap_block_name=[Block])
    
    checkpoint_flags_whole_model = [0] + checkpoint_flags_enc + [0, 0]
    hp_model.wrap_pipeline_modules_checkpoint(checkpoint_flags_whole_model, wrap_block_name=[Block])
    
    return hp_model