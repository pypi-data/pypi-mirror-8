from distutils.core import setup

setup(
    name='py2opencl',
    version='0.3.0',
    author='kieran hervold',
    author_email='hervold@gmail.com',
    packages=['py2opencl', 'py2opencl.test'],
    url='https://github.com/hervold/py2opencl',
    license='LICENSE.txt',
    description='auto-creation of OpenCL kernels from pure Python code',
    long_description=open('README.txt').read(),
    install_requires=[
        "pyopencl >= 2014.1",
	"pillow >= 2.3.3",
    ],
    package_data={
	'sample': ['py2opencl/test/Lenna.png'],
    },
)
