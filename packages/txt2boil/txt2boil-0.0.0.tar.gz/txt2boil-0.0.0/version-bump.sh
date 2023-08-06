#!/bin/sh

# Copyright (C) 2014 Kieran Colford

# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

help() {
    echo "usage: $0 [<version-id>]
Bump the version number to version-id.  If not specified then get the
version-id from git-flow.

Options:
  -h, --help       print this help message and exit
"
    exit 0
}

versionfile="txt2boil/version.py"
verid=`git branch | sed 's/\* release\/\(.*\)/\1/;t;d'`

for opt in "$@"
do
    case $opt in
	-h|--help)
	    help
	    ;;
	-*)
	    echo "Error: Invalid Option:" $opt
	    help
	    ;;
	*)
	    verid=$opt
	    ;;
    esac
done

echo "version = '$verid'" > $versionfile
git add $versionfile
git commit -m "Bumped version number to $verid" $versionfile
