#!/bin/sh

# Copyright (C) 2014 Kieran Colford

# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

# Print out help message.
help() {
    echo "usage: $0 [<version-id>]
Bump the version number to version-id.  If not specified then get the
version-id from git-flow.

Options:
  -h, --help       print this help message and exit

Note that the version bump script can only figure out the version
during a hotfix or a release.  At any other time you have to supply
the version-id manually."

    exit 0
}

# Function to print out the code for the new version file.
update() {
    echo "version = '$verid'"
}

versionfile="txt2boil/version.py"
verid=`git branch | sed 's/\* \(release\|hotfix\)\/\(.*\)/\2/;t;d'`

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

if [ x$verid = x ]; then
    echo "Error: no version-id available"
    help
fi

update > $versionfile
./addcopy.sh
git add $versionfile
git commit -m "Bumped version number to $verid" $versionfile
