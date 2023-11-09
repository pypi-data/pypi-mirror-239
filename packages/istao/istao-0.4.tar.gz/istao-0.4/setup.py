from setuptools import setup

setup(
    name='istao',
    version='0.4',
    author='Yatoub',
    description='Library for Tao Python applications to check if the intended operating system is being used',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Tao-Linux/python-istao',
    project_urls={
        'Bug Tracker': 'https://github.com/Tao-Linux/python-istao/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    packages=['istao'],
    install_requires=[
        'distro',
        'colorama',
    ],
)
