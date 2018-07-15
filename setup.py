from setuptools import setup, find_packages

setup(
    name='mobius-client-python',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'PyJWT',
        'stellar-base',
    ],
)
