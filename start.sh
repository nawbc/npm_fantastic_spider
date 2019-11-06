#! /bin/sh
#
# dev.sh
# Copyright (C) 2019 sewer <sewer@super-fake-hack>
#
# Distributed under terms of the MIT license.

#!/bin/bash

python3 ./npm_fantastic_no_scrapy/npm_fantastic.py $*
#echo $*
#while getopts ds OPT; do
#    case $OPT in
#        d)
#            python3 ./npm_fantastic_no_scrapy/npm_fantastic.py
#            ;;
#        s)
#            python3 ./npm_fantastic_no_scrapy/npm_fantastic.py
#            ;;
#        [?])
#            echo "nothing happened"
#            ;;
#    esac
#done
#
#shift $(($OPTIND - 1))