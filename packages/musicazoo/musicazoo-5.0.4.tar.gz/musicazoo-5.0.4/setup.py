#!/usr/bin/env python

from distutils.core import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='musicazoo',
    version='5.0.4',
    description='Modular media player',
    author='Zach Banks',
    author_email='zbanks@mit.edu',
    url='https://github.com/zbanks/musicazoo',
    packages=['musicazoo', 'musicazoo.wsgi', 'musicazoo.queue', 'musicazoo.volume', 'musicazoo.lib', 'musicazoo.nlp'],
    download_url="https://github.com/zbanks/musicazoo/tarball/5.0.4",
    install_requires=required,
    scripts=[
        "bin/musicazoo", "bin/mz"
    ],
    package_dir = {
        'musicazoo.wsgi': 'musicazoo/wsgi'
    },
    package_data={
        'musicazoo.wsgi': ['static/*.html', 'static/assets/*.js', 'static/assets/*.otf', 'static/assets/*.css', 'static/assets/images/*']
    }
)
