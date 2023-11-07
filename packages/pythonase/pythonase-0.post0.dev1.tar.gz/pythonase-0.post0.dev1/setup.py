from setuptools import setup
import versioneer

setup(
    name='pythonase',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['pythonase', 'pythonase.file_parser_mem', ],
    install_requires=("numpy", "pandas", "matplotlib", "scipy", ),
    url='',
    license='',
    author='Li Yao',
    author_email='py_packages@yaobio.com',
    description='Pythonase is a collection of gist functions (mainly for bioinformatic analysis) for saving time.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
