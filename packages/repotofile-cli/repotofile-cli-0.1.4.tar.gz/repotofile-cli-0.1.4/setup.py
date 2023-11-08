from setuptools import setup, find_packages

setup(
    name='repotofile-cli',
    version='0.1.4',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'repotofile=repotofile.cli:main',
            'rtf=repotofile.cli:main'
        ],
    },
    # Additional metadata to include according to your needs
    author='Maurits Bos',
    author_email='maurits.bos@gmail.com',
    description='A CLI tool to clone and process GitHub repositories.',
    keywords='github cli tool repository conversion',
    url='https://github.com/mbbrainz/repotofile-cli',  # Replace with your actual url
    project_urls={
        'Bug Tracker': 'https://github.com/mbbrainz/repotofile-cli/issues',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control :: Git',
        'License :: OSI Approved :: MIT License',  # Or your chosen license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
