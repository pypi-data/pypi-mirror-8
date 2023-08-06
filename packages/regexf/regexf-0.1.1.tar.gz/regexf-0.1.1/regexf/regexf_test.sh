#!/bin/bash
#   author:martinmhan@yahoo.com date:  22/04/2014
#   regexf is a bash command line interface to the tango scada (and in future epics)
#   Copyright (C) <2014>  <Martin Mohan>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

#set -x
verbose=0
if [ x$1 = x"" ]; then 
    export verbose=0
else
    export verbose=1
fi

export PATH=.:$PATH
source regexf_unittest.sh

configFile=/usr/local/bin/regexf.ini
assertEquals "regexf aa/bb/cc" "$configFile:re.match<aa/bb/cc> no_match"
assertEquals "regexf aa/bb/cc vac/bb/cc" "$configFile:re.match<aa/bb/cc> no_match"
assertContains "regexf vac/bb/cc -v" " match"
assertContains "regexf -i -f $configFile" "regexf_version"

test_file=/usr/local/bin/regexf_test.ini

#test_file
#echo "[tango]
#patterns=
#    ^([amk])/(\w+)/(\w+)$" > $test_file

assertEquals "regexf -f $test_file aa/bb/cc" "$test_file:re.match<aa/bb/cc> no_match"
assertEquals "regexf -f $test_file m/bb/cc" ""
#rm $test_file
