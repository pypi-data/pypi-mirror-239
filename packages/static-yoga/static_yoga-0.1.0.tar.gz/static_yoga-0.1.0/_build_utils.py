from pathlib import Path
from subprocess import check_call
from tempfile import TemporaryDirectory

from setuptools import Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py

ROOT = Path(__file__).parent.resolve()
name = 'static_yoga'
YOGA_ROOT = ROOT / name / 'yoga' / 'yoga'
# BUILD_ROOT = None
# useful for caching the compilation
BUILD_ROOT = ROOT / 'build' / 'yoga'


class PyprojectBuild(build_py):
    def initialize_options(self):
        super().initialize_options()

        self.distribution.ext_modules = [Extension(
            f'{name}.yoga.bridge',
            sources=[f'{name}/yoga/bridge.pyx'],
            include_dirs=[str(YOGA_ROOT)],
            language='c++',
            extra_compile_args=['-std=c++11'],
        )]


class YogaBuilder(build_ext):
    def build_extension(self, ext):
        with TemporaryDirectory() as _root:
            if BUILD_ROOT is not None:
                BUILD_ROOT.mkdir(parents=True, exist_ok=True)
                root = BUILD_ROOT
            else:
                root = Path(_root)

            # build
            check_call(['cmake', '-S', str(YOGA_ROOT), f'-B{root}'])
            # compile
            check_call(['make'], cwd=root)

            ext.extra_objects.append(str(root / 'libyogacore.a'))
            self.compiler.add_include_dir(str(YOGA_ROOT / 'yoga'))
            super().build_extension(ext)
