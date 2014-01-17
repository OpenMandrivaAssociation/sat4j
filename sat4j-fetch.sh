#!/bin/sh
name=sat4j
tag=org.ow2.sat4j.pom-2.3.5
version=2.3.5
tar_name=$name-$version

rm -fr $tar_name && mkdir $tar_name
pushd $tar_name

# Fetch plugins
svn co svn://svn.forge.objectweb.org/svnroot/sat4j/maven/tags/$tag .
find . -name *.jar -delete

popd
# create archive
tar -caf $tar_name.tar.xz $tar_name
