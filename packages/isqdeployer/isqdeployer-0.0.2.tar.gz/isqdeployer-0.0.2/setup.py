
import setuptools

setuptools.setup(
    name='isqdeployer',
    scripts=[],
    version='0.0.2',
    packages=setuptools.find_packages(),
    license='LICENSE.md',
    description='Python lib for using isq',
    long_description=open('README.md',encoding="utf8").read(),
    long_description_content_type="text/markdown",
    install_requires=['isqtools>=0.1.4'],
    python_requires='>=3.7',
    url = "https://www.arclightquantum.com/",
    package_dir={'isQ': '/home/hengyue/Dropbox/ALQ/Projects/isqdeployer/isqdeployer/isQ','fortran':'/home/hengyue/Dropbox/ALQ/Projects/isqdeployer/isqdeployer/fortran'}
)
