
import io
from setuptools import setup, find_packages

setup(
    name='automate3chapter11',
    version='2023.11.7',
    url='https://github.com/asweigart/automateboringstuff3',
    author='Al Sweigart',
    author_email='al@inventwithpython.com',
    description=('This package installs the latest compatible version of the packages covered in Chapter 11 of Automate the Boring Stuff with Python, 3rd Edition.'),
    long_description='This package installs the latest compatible version of the packages covered in Chapter 11 of Automate the Boring Stuff with Python, 3rd Edition.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Send2Trash==1.8.2',
    ],
    keywords="automate boring stuff python",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
