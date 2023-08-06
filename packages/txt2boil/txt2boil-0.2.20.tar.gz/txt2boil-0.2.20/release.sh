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

cur=`git describe --tags --abbrev=0 --match=v*`
new=`increment_version $cur`

#echo $new
git tag $num
git push --all --tags

. upload.sh
