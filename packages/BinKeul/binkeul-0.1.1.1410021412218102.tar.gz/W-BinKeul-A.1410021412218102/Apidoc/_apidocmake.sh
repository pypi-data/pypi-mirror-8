#! /bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
echo $SCRIPTPATH
cd $SCRIPTPATH

rm -rf ./modules
sphinx-apidoc -f -e ../binkeul/ -o ./modules
make doctest
make html
