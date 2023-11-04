import os
import setuptools


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = os.path.join(lib_folder, 'requirements.txt')

requirements = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        requirements = f.read().splitlines()


setuptools.setup(
    version='1.0.0',
    name='ether_wallet',
    author='Alexey',
    author_email='abelenkov2006@gmail.com',
    description='The package, containing wrapper over EVM operations for interacting through Wallet entities.',
    keywords='ethereum wallet, ether wallet',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blnkoff/ether-wallet',
    project_urls={
        'Documentation': 'https://github.com/blnkoff/ether-wallet',
        'Bug Reports':
        'https://github.com/blnkoff/ether-wallet/issues',
        'Source Code': 'https://github.com/blnkoff/ether-wallet',
    },
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS'
    ],
    python_requires='>=3.11',
    package_data={'ether_wallet': ['*.abi']},
    install_requires=requirements
)

