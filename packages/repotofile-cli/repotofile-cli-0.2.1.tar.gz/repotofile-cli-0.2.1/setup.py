from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='repotofile-cli',
    version='0.2.1',
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
    long_description=long_description,
    long_description_content_type='text/markdown', 
    keywords='github cli tool repository conversion ai ai-tools',
    url='https://github.com/mbbrainz/repotofile-cli',  
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
