import json
from pathlib import Path
from setuptools import setup, find_packages


BASE_DIR = Path(__file__).resolve().parent
version_info = json.load(BASE_DIR.joinpath('xfyun_auth', 'version.json').open())

setup(
    name=version_info['prog'],
    version=version_info['version'],
    author=version_info['author'],
    author_email=version_info['author_email'],
    description=version_info['desc'],
    long_description=BASE_DIR.joinpath('README.md').read_text(),
    long_description_content_type='text/markdown',
    url=version_info['url'],
    license='MIT License',
    install_requires=BASE_DIR.joinpath('requirements.txt').read_text().strip().split(),
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'name = project.bin.main:main',
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ]
)
