from distutils.core import setup

setup(
    name='quora',
    version='0.1.14',
    description='Fetches and parses data from Quora.',
    author='Christopher Su',
    author_email='chris+gh@christopher.su',
    url='https://github.com/csu/pyquora',
    packages=['quora'],
    install_requires=[
        "beautifulsoup4 == 4.3.2",
        "feedparser == 5.1.3",
        "requests==2.3.0"
    ]
)