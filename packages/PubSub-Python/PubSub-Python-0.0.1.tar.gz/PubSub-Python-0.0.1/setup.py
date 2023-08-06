from setuptools import find_packages
from setuptools import setup

VERSION = '0.0.1'

setup_args = dict(
    name='PubSub-Python',
    description=('Simple Python client for interacting with Google Cloud '
                 'Pub/Sub.'),
    url='https://github.com/tylertreat/PubSub-Python',
    version=VERSION,
    license='Apache',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['google-api-python-client', 'pyopenssl', 'httplib2'],
    author='Tyler Treat',
    author_email='ttreat31@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)

