from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mobius-client',
    version='1.0.2',
    url="https://github.com/mobius-network/mobius-client-python",
    author="Mobius Team",
    author_email="developers@mobius.network",
    description="Mobius DApp Store SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'PyJWT',
        'stellar-base',
    ],
    extras_require={
        'example': ['flask'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        'Mobius Store': 'https://store.mobius.network',
        'Documentation': 'https://docs.mobius.network',
        'Bug Reports': 'https://github.com/mobius-network/mobius-client-python/issues',
        'Source': 'https://github.com/mobius-network/mobius-client-python/',
    },
)
