import sys


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


if sys.version_info <= (2, 5):
    raise Exception('Requires Python Version 2.6 or above... exiting.')


REQUIREMENTS = [
    'httplib2',
    'oauth2client',
    'protobuf >= 2.5.0',
    'pycrypto',
    'pyopenssl',
    'pytz',
    'six',
]

setup(
    name='gcloud',
    version='0.3.0',
    description='API Client library for Google Cloud',
    author='JJ Geewax',
    author_email='jj@geewax.org',
    scripts=[],
    url='https://github.com/GoogleCloudPlatform/gcloud-python',
    packages=find_packages(),
    license='Apache 2.0',
    platforms='Posix; MacOS X; Windows',
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
    ]
)
