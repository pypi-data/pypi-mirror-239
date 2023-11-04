from setuptools import setup, find_packages

NAME = 'o3r_docker_manager'
VERSION = '0.0.9'
DESCRIPTION = 'O3R docker deployment utilities'
LONG_DESCRIPTION = 'A package that makes it easy to manage deployment and testing of code for the O3R camera system'

setup(
    name= NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="ifm gmbh",
    # author_email="",
    packages=find_packages(include=['o3r_docker_manager']),
    install_requires=[
        'pyyaml',
        'scp',
        'ifm3dpy',
    ],
    entry_points = {
        'console_scripts':[
            'o3r_docker_manager=o3r_docker_manager.o3r_docker_manager:manage']
    }
)