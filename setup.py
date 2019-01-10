from setuptools import setup, find_packages

setup(
    name='2048',
    version='0.1',
    url='https://github.com/trevorxander/2048',
    license='',
    author='Trevor Xander',
    author_email='trevorcolexander@gmail.com',
    description='',
    install_requires = ['PyQt5', 'anytree','setuptools'],
    py_modules=['2048'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            '2048 = 2048:run_game'
        ]
    }
)
