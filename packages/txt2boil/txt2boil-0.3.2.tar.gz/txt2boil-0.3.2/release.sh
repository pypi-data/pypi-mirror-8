#!/bin/bash


increment_version () {
    local num basever
    for ver
    do
	num=`echo $ver | sed 's/^\(.*\.\)\([0-9]\+\)$/\2/'`
	((num+=1))
	basever=`echo $ver | sed 's/^\(.*\.\)\([0-9]\+\)$/\1/'`
	echo $basever$num
    done
}

cur=`git describe --abbrev=0 --match=v*`
new=`increment_version $cur`

#echo $new
git tag -a -m "Version $num" $num
git push --all --follow-tags

. upload.sh
