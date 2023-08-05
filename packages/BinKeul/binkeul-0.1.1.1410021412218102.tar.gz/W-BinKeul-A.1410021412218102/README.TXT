
binkeul
========

Abstract
========

A Python library to support BinKeul.

a simple example::

    from binkeul import *
    import os 

    kd01 = LKode( 17929083 )
    BG30 = BtGrid( 20 )
    
    im = BG30.getImage(kd01.getL3())
    im.save( '17929083.png' )


for more examples see: examples/*.py

Installation
============

with pip::

    pip install binkeul

or from source::

    python setup.py install


Documentation
=============

  * http://packages.python.org/binkeul
  * http://readthedocs.org/docs/binkeul/

send feedback to ikw3179@naver.com

svgwrite can be found on bitbucket.org at:

http://bitbucket.org/sinabilo/binkeul
