import os
from setuptools import setup, find_packages

def read(fname):
    with open(fname) as fhandle:
        return fhandle.read()

def readMD(fname):
    # Utility function to read the README file.
    full_fname = os.path.join(os.path.dirname(__file__), fname)
    if 'PANDOC_PATH' in os.environ:
        import pandoc
        pandoc.core.PANDOC_PATH = os.environ['PANDOC_PATH']
        doc = pandoc.Document()
        with open(full_fname) as fhandle:
            doc.markdown = fhandle.read()
        return doc.rst
    else:
        return read(fname)

required = [req.strip() for req in read('requirements.txt').splitlines() if req.strip()]
version = '1.0.2'
setup(
    name='Carpenter',
    version=version,
    author='Matthew Seal',
    author_email='mseal@opengov.us',
    description='A utility library which repairs and analyzes tablular data',
    long_description=readMD('README.md'),
    install_requires=required,
    license='LGPL 2.1',
    packages=find_packages(),
    test_suite='tests',
    zip_safe=False,
    url='https://github.com/OpenGov/carpenter',
    download_url='https://github.com/OpenGov/carpenter/tarball/v' + version,
    keywords=['tables', 'data', 'analysis', 'extraction'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2 :: Only'
    ]
)
