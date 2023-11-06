from setuptools import setup, find_packages

setup(
    name='shieldb',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy~=2.0.22',
        'Flask~=3.0.0',
        'psycopg2-binary~=2.9.1'
    ],
    entry_points={
        'console_scripts': [
            'shieldb=test2.app:main',
        ],
    },
)
