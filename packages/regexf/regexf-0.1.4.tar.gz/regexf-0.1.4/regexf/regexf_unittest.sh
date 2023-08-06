#!/bin/bash
#   author:martinmhan@yahoo.com date:  22/04/2014
#   unittest  Provide unit tests. Must be sourced
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

verbose=0
#To use this file add to your script "source ./unittest.sh"

TRUE=0
FALSE=1

PASS=0
FAIL=1

# eval command and check if expected = actual
function assertEqual()
{
    actual="`eval $1`"
    expected=$2;
    if [ "$expected" != "$actual" ]; then
        echo "fail:$1 expected: $expected actual: $actual"
        return $FAIL
    else
        echo pass: $1
        return $PASS
    fi
}

# eval command and check if actual results contains expected values
function assertGrep()
{
#    echo "assertGrep(): $0 $1 $2"
    actual="`eval $1`"
    grep_string=$2;

    if [[ "$actual" =~ "$grep_string" ]]; then
        echo pass: $1
        return $PASS
    else
        echo "fail:$1 expected_part: $grep_string actual: $actual"
        return $FAIL
    fi
}

# eval check if actual returns True 0
function assertTrue()
{
    actual=`eval $1`
    if [ $? -eq 0 ]; then
        echo "pass: assertTrue $1"
        return $PASS
    else
        echo "fail: assertTrue $1 $actual"
        return $FAIL
    fi
}

# eval check if actual returns False 1
function assertFalse()
{
    actual=`eval $1`
    if [ $? -eq 0 ]; then
        echo "fail: assertFalse $1 $actual"
        return $PASS
    else
        echo "pass: assertFalse $1"
        return $FAIL
    fi
}
