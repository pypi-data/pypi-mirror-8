from distutils.core import setup

setup(
    name='tube',
    version='1.0.1',
    author='Adam Gilman',
    author_email='me@adamgilman.com',
    packages=['tube'],
    url='https://github.com/adamgilman/tube-python',
    download_url='https://github.com/adamgilman/tube-python/archive/1.0.1.tar.gz',
    license='LICENSE',
    description='Python object wrapper for TfL (Transport for London) TrackerNet information service',
    install_requires=[
        "requests >= 2.5.0",
        "xmltodict >= 0.9.0",
    ],
)