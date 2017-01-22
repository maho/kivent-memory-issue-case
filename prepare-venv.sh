#!/bin/bash

set -ex

pip install --upgrade pip
pip install --upgrade setuptools
pip install "cython<0.24"


test -n "$SKIP_CYMUNK" || pip install git+https://github.com/tito/cymunk
#test -n "$SKIP_KIVY" || pip install git+git://github.com/kivy/kivy@master

mkdir -p .binpackages
cd .binpackages

if [ -z "$SKIP_KIVY" ];then
    git clone --single-branch -b rebatchmemleak2 git://github.com/mahomahomaho/kivy
    cd kivy 
    python setup.py install 2>&1 | tee ../../kivy-build-log.txt
    cd ..
    #pip install -e $PWD/kivy
fi

pip install git+https://github.com/kivy/plyer

if [ -n "$SKIP_KIVENT" ];then
    exit
fi
if [ ! -d .binpackages/kivent -o -n "$FORCE_KIVENT" ] ;then
    mkdir -p kivent
    #test -n "$SKIP_CLONE" || git clone -b 2.2-dev --single-branch https://github.com/kivy/kivent
    test -n "$SKIP_CLONE" || git clone -b rebatchmemleak2 --single-branch git://github.com/mahomahomaho/kivent
    cd kivent/modules/core
    python setup.py install 2>&1 | tee ../../kivent-build-log.txt
    cd ../cymunk
    python setup.py install
fi
