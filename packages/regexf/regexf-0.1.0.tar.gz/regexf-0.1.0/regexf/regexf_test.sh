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
#echo "Call: `which regexf`"

#assertContains "./regexf -h","Compare patterns"
assertEquals "./regexf aa/bb/cc","./regexf.ini:re.match<aa/bb/cc> fail"

#assertEquals "./regexf sys/tg_test/1",""
#assertEquals "./regexf sys/tg_test/1 -v","./regexf.ini:re.match\(^sys/\w+/\w+$,sys/tg_test/1\) pass"
