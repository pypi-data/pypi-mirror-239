from setuptools import setup

setup(
    name='salure_helpers_zoho',
    version='0.1.1',
    description='ZOHO wrapper from Salure',
    long_description='ZOHO wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.zoho"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1'
    ],
    zip_safe=False,
)
