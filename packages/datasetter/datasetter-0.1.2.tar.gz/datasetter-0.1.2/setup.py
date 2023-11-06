from setuptools import setup, find_packages

setup(
    name='datasetter',
    version='0.1.2',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'datasetter = datasetter.hello:say_hello',
        ],
    },
)
