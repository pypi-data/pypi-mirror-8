import sys

from setuptools import setup


description = "Command line script that automatically searches for video subtitles using OpenSubtitles.org APIs."
long_description = ''

dependencies = ['guessit>=0.7.1', 'colorama']
if sys.version_info <= (3, 1):
    dependencies.append('futures')

setup(
    name="ss",
    version="1.5.1",
    packages=[],
    scripts=['ss.py'],
    py_modules=['ss'],
    install_requires=dependencies,
    entry_points={'console_scripts': ['ss = ss:main']},

    # metadata for upload to PyPI
    author="nicoddemus@gmail.com",
    author_email="nicoddemus@gmail.com",
    description=description,
    long_description=long_description,
    license="GPL",
    keywords="subtitles script",
    url="http://nicoddemus.github.io/ss/",

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

    ]
)
