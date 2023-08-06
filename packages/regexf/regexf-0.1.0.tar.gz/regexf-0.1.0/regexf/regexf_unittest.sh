#!/bin/bash
#   author:martinmhan@yahoo.com date:  22/04/2014
#   scadat is a bash command line interface to the tango scada (and in future epics)
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

echo "$0 verbose=$verbose"

if (($verbose > 0));then
    echo "TestSummary: Expected: Actual:"
else
    echo "TestSummary"
fi

# eval command and check if expected = actual
function assertEquals()
{
    actual="`eval $1`"
    expected=$2;
    if [ "$expected" != "$actual" ]; then
        echo "fail:$1 expected: $expected actual: $actual"
        return -1
    else
        if (($verbose > 0));then
            echo "pass: $actual $expected"
            return -1
        else
            echo pass: $1
            return 0
        fi
    fi
}

# eval command and check if expected = actual
function assertContains()
{
#    echo "assertContains(): $0 $1 $2"
    actual="`eval $1`"
    part_string=$2;

    if [[ "$actual" =~ "$part_string" ]]; then
        if (($verbose > 0));then
            echo "pass: $1 $part_string contained in $actual"
            return -1
        else
            echo pass: $1
            return 0
        fi
    else
        echo "fail:$1 expected_part: $part_string actual: $actual"
    fi
}

# eval check if actual returns True 0
function assertTrue()
{
    actual="`eval $1`"
#    expected=$2;
    if [ "$actual" ]; then
        echo pass: $1 $actual
        return 0
    else
        echo "fail:$1 $actual"
        return -1
    fi
}
