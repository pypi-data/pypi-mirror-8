from setuptools import find_packages
from setuptools import setup


setup(
    name='grow',
    version=open('grow/VERSION').read().strip(),
    description=(
          'Develop everywhere and deploy anywhere: a declarative '
          'static site generator/CMS for building high-quality web sites.'
    ),
    long_description=open('description.txt').read().strip(),
    url='http://growsdk.org',
    license='MIT',
    author='Grow SDK Authors',
    author_email='hello@grow.io',
    include_package_data=True,
    packages=find_packages(
        exclude=[
            'grow/submodules',
        ],
    ),
    scripts=[
        'bin/grow',
    ],
    keywords=[
        'grow',
        'cms',
        'static site generator',
        's3',
        'google cloud storage',
        'content management'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])
