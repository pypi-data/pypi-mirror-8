from distutils.spawn import find_executable
import os
import pandoc
from setuptools import setup, find_packages

from dockerfabric import __version__

pandoc.core.PANDOC_PATH = find_executable('pandoc')


def include_readme():
    readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
    doc = pandoc.Document()
    with open(readme_file, 'r') as rf:
        doc.markdown = rf.read()
        return doc.rst


setup(
    name='docker-fabric',
    version=__version__,
    packages=find_packages(),
    install_requires=['six', 'Fabric>=1.8.0', 'docker-py>=0.5.0', 'docker-map>=0.1.1'],
    license='MIT',
    author='Matthias Erll',
    author_email='matthias@erll.de',
    url='https://github.com/merll/docker-fabric',
    description='Integration for Docker into Fabric.',
    long_description=include_readme(),
    platforms=['OS Independent'],
    keywords=['docker', 'fabric'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Software Distribution',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    include_package_data=True,
)
