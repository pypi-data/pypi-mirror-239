from setuptools import setup, find_packages, Command
from setuptools.command.install import install
import pathlib
import os

try:
    import fused_dense_lib, dropout_layer_norm, rotary_emb, xentropy_cuda_lib
except ImportError:
    fused_dense_lib, dropout_layer_norm, rotary_emb, xentropy_cuda_lib = None, None, None, None
    

CUDA_RELATED_INSTALL = os.getenv("GALVATRON_SKIP_CUDA_DEP", "TRUE") == "FALSE"

here = pathlib.Path(__file__).parent.resolve()

class CustomInstall(install):
    def run(self):
        install.run(self)
        print(os.getenv("PATH"))

        # custom install apex and flash-attention by running prepare_env.sh
        if CUDA_RELATED_INSTALL:
            cwd = pathlib.Path.cwd()
            
            if fused_dense_lib is None or dropout_layer_norm is None or rotary_emb is None or xentropy_cuda_lib is None:
                self.spawn(['bash', cwd / 'src' / 'galvatron' / 'flash_attn_ops_install.sh'])

dependencies = [
    "transformers>=4.31.0",
    "h5py>=3.6.0",
    "pybind11>=2.9.1",
    "timm>=0.5.4",
    "attrs>=21.4.0",
    "yacs>=0.1.8",
    "sentencepiece"
]

if CUDA_RELATED_INSTALL:
    dependencies.append("flash-attn>=2.0.8")

setup(
    name='hetu-galvatron',
    version='0.0.2',
    description='Galvatron, a Efficient Transformer Training Framework for Multiple GPUs Using Automatic Parallelism',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yujie Wang, Shenhan Zhu',
    author_email='alfredwang@pku.edu.cn, shenhan.zhu@pku.edu.cn',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={'galvatron': ['*.json']},
    include_package_data=True,
    scripts=['src/galvatron/flash_attn_ops_install.sh'],
    python_requires=">=3.8",
    cmdclass={
        'install': CustomInstall
    },
    install_requires=dependencies
)
