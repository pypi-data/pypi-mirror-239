from distutils.core import setup
from pathlib import Path
from setuptools import find_namespace_packages

version_module_path = Path(__file__).parent / 'datasphere' / 'version.py'

meta = {}
with open(version_module_path) as f:
    exec(f.read(), meta)

name = 'datasphere'

setup(
    name=name,
    version=meta['version'],
    license='Apache-2.0',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
    ],
    tests_require=['pytest', 'pytest-mock'],
    author="Yandex LLC",
    author_email="cloud@support.yandex.ru",
    packages=find_namespace_packages(include=(f'{name}*', 'yandex*', 'google*')),
    package_data={name: ['logs/logging.yaml']},
    install_requires=[
        'grpcio',
        'requests',
        'pyyaml',
        'tabulate>=0.9.0',
        'envzy>=0.2.0',
    ],
    entry_points={
        'console_scripts': [
            'datasphere = datasphere.main:main',
        ],
    },
    python_requires=">=3.8",
    description='Yandex Cloud DataSphere',
    long_description_content_type='text/markdown',
    long_description='Yandex Cloud DataSphere',
)
