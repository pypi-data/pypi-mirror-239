from setuptools import setup, find_packages

setup(
    name='masker',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy~=2.0.23',
        'Flask~=2.2.5',
        'psycopg2-binary~=2.9.1'
    ],
    data_files=[('', ['run_masker/app.py', 'README.md', 'requirements.txt'])],
    entry_points={
        'console_scripts': [
            'masker=run_masker.app:main',
        ],
    },
)
