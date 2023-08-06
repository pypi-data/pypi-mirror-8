#!/bin/bash

# Copyright (C) 2014 Kieran Colford

# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.


#gpl=$(< gpl_declaration.py)
for f in `git ls-files '*.py'`
do
    case "$(< $f)" in
	*'# Copyright'*)	# License already there, do nothing
	    ;;
	'#!'*)			# Preserve the sh-bang line
	    { 
		head -n 1 $f; 
		echo; 
		cat gpl_declaration.py;
		tail -n +2 $f;
	    } > $f-t
	    ;;
	*)			# Prepend the notice
	    cat gpl_declaration.py $f > $f-t
	    ;;
    esac

    # Replace old file with new file.
    if [ -f $f-t ]; then
	chmod --reference=$f $f-t # preserve mode bits
	mv $f-t $f
    fi
done
