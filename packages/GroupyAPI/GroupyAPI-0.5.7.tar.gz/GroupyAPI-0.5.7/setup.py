from setuptools import setup

setup(
    name = 'GroupyAPI',
    packages = ['groupy', 'groupy.object', 'groupy.api'],
    version = '0.5.7',
    install_requires = open('requirements.txt').read().splitlines(),
    description = 'The simple yet powerful wrapper for the GroupMe API',
    author = 'Robert Grant',
    author_email = 'rhgrant10@gmail.com',
    url = 'https://github.com/rhgrant10/Groupy', # use the URL to the github repo
    keywords = ['api', 'GroupMe'], # arbitrary keywords
    classifiers = ['Programming Language :: Python :: 3'],
    long_description=open('README.rst', 'r').read()
)
