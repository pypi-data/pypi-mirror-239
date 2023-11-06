from setuptools import setup, find_packages

setup(
    name='shieldb',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy~=2.0.22',
        'Flask~=3.0.0',
        'psycopg2-binary~=2.9.1'
    ],
    data_files=[('', ['script/app.py', 'README.md', 'requirements.txt'])],
    entry_points={
        'console_scripts': [
            'shieldb=script.app:main',
        ],
    },
)
