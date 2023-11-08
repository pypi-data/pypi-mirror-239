from setuptools import setup

setup(
    name='fastapi_prime',
    version='1.0',
    author='Manoj',
    author_email='mmanoj20037@gmail.com',
    description='This is library can make you fast whole structure',
    install_requires=[
        'fastapi >= 0.104.0',
        'uvicorn >= 0.23.0'
    ],
    entry_points={
        'console_scripts': [
            'fastapi-prime-create = fastapi_prime.fastapi_prime:main',
        ],
    },
    classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
)
