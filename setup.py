import os
import os.path

from setuptools import setup, find_packages, Extension
import versioneer

# Default description in markdown
LONG_DESCRIPTION = open('README.md').read()


PKG_NAME     = 'deluge-uils'
AUTHOR       = 'Rafael Gonzalez'
AUTHOR_EMAIL = 'astrorafael@gmail.com'
DESCRIPTION  = 'Utils for Deluge',
LICENSE      = 'MIT'
KEYWORDS     = 'Music'
URL          = 'https://github.com/astrorafael/deluge-utils/'
DEPENDENCIES = ['tabulate','jinja2']

CLASSIFIERS  = [
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.7',
    'Development Status :: 4 - Beta',
]

# Package additional data inside
PACKAGE_DATA = {
    'deluge': ['templates/kit-template.j2'],
}

SCRIPTS = [ "scripts/deluge"]

DATA_FILES = []

setup(
    name             = PKG_NAME,
    version          = versioneer.get_version(),
    cmdclass         = versioneer.get_cmdclass(),
    author           = AUTHOR,
    author_email     = AUTHOR_EMAIL,
    description      = DESCRIPTION,
    long_description_content_type = "text/markdown",
    long_description = LONG_DESCRIPTION,
    license          = LICENSE,
    keywords         = KEYWORDS,
    url              = URL,
    classifiers      = CLASSIFIERS,
    packages         = find_packages("src"),
    package_dir      = {"": "src"},
    install_requires = DEPENDENCIES,
    scripts          = SCRIPTS,
    package_data     = PACKAGE_DATA,
    data_files       = DATA_FILES,
)
