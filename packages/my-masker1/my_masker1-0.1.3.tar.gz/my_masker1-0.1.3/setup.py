from setuptools import setup, find_packages

setup(
    name='my_masker1',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy~=2.0.22',
        'Flask~=3.0.0',
    ],
    entry_points={
        'console_scripts': [
            'your_script_name=masking.test.app:main',
        ],
    },
)
