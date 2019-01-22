import os
from setuptools import setup, find_packages


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='2048',
    version='0.1',
    url='https://trevorxander.com/#2048',
    license='GNU Affero General Public License v3.0',
    author='Trevor Xander',
    author_email='trevorcolexander@gmail.com',
    long_description=read('README'),
    install_requires=['PyQt5', 'anytree', 'setuptools'],
    py_modules=['2048'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            '2048 = 2048:run_game'
        ]
    }
)
