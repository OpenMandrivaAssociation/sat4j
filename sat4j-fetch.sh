#!/bin/sh
name=sat4j
tag=2_0_3
version=2.0.3
tar_name=$name-$version

rm -fr $tar_name && mkdir $tar_name
pushd $tar_name

# Fetch plugins
svn co svn://svn.forge.objectweb.org/svnroot/sat4j/maven/tags/2_0_3 .

popd
# create archive
tar -cjf $tar_name.tar.bz2 $tar_name
