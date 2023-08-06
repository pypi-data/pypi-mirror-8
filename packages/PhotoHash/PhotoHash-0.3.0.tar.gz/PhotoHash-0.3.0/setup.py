from distutils.core import setup

setup(
    name='PhotoHash',
    version='0.3.0',
    author='Chris Pickett',
    author_email='chris.pickett@gmail.com',
    packages=['photohash', ],
    url='https://github.com/bunchesofdonald/photohash',
    license='MIT',
    description='A Python Perceptual Image Hashing Module',
    long_description=open('README.rst').read(),
    install_requires=[
        'Pillow>=2.1.0',
    ],
)
