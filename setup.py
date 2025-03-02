from setuptools import setup, find_packages

setup(
    name='weather_etl',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "pandas",
        "psycopg2",
    ],
    entry_points={
        'console_scripts': [
            'weather_etl-extract=weather_etl.extract:main',
            'weather_etl-transform=weather_etl.transform:main',
            'weather_etl-load=weather_etl.load:main',
        ],
    },
)
