%define eclipse_base %{_datadir}/eclipse
# We want the version to match that shipped in Eclipse's Orbit project
%define sat4jversion 2.0.0.v20080602

Name:           sat4j
Version:        2.0.0
Release:        %mkrel 0.6.1
Summary:        A library of SAT solvers written in Java

Group:          Development/Libraries
License:        EPL and LGPLv2
URL:            http://www.sat4j.org/
Source0: http://forge.objectweb.org/tracker/download.php/228/350289/310427/1838/org.sat4j.core-src.zip
Source1: http://forge.objectweb.org/tracker/download.php/228/350289/310427/1839/org.sat4j.pb-src.zip
# These have been reported upstream
# http://forge.objectweb.org/tracker/index.php?func=detail&aid=310427&group_id=228&atid=350289
# There are erroneous @Overrides statements which are caught with ecj.
# We remove them.
Patch0:         sat4j-core-nooverrides.patch
Patch1:         sat4j-core-Dimacs-nooverrides.patch
# This is so we can run the tests.  Some errors are expected; see up for
# OW tracker thread.
Patch2:         sat4j-junit4fortests.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  java-rpmbuild >= 1.6
BuildRequires:  junit4
BuildRequires:  eclipse-pde
Requires:       java >= 1.6
Requires:       jpackage-utils

BuildArch:      noarch

%description
The aim of the SAT4J library is to provide an efficient library of SAT
solvers in Java. The SAT4J library targets first users of SAT "black
boxes", those willing to embed SAT technologies into their application
without worrying about the details.

%prep
%setup -q -c -a 1
/bin/sh %{eclipse_base}/buildscripts/copy-platform SDK %{eclipse_base}

pushd core
# Only used for the tests
rm lib/jmock-*.jar

echo %{sat4jversion} > src/sat4j.version
sed -i "s/9.9.9.token/%{sat4jversion}/" META-INF/MANIFEST.MF 
%patch0 -p0
%patch1 -p0
mv build{,.upstream}
cd build.upstream
%patch2 -p0
sed -i "s:/usr/share/java:%{_datadir}/java:" build.xml
popd

pushd pb
sed -i "s/9.9.9.token/%{sat4jversion}/" META-INF/MANIFEST.MF 
sed -i "/^Class-Path/d" META-INF/MANIFEST.MF 
# Only used for the tests
rm lib/jmock-*.jar
popd

# I don't think package build can handle DOS line endings in MANIFEST.MF
sed -i 's/\r//' core/META-INF/MANIFEST.MF
sed -i 's/\r//' pb/META-INF/MANIFEST.MF

%build
SDK=$(cd SDK > /dev/null && pwd)

pushd core
mkdir home build
home=$(cd home > /dev/null && pwd)

# These can go away when package build handles plugins (not just
# features)
echo "<project default=\"main\"><target name=\"main\"></target></project>" \
 > build/assemble.org.sat4j.core.all.xml
echo "<project default=\"main\"><target name=\"main\"></target></project>" \
 > build/package.org.sat4j.core.all.xml

%java -cp $SDK/startup.jar \
 -Duser.home=$home \
 -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
 org.eclipse.core.launcher.Main \
 -application org.eclipse.ant.core.antRunner \
 -Dtype=plugin \
 -DjavacSource=1.5 \
 -DjavacTarget=1.5 \
 -Did=org.sat4j.core \
 -DbaseLocation=$SDK \
 -DsourceDirectory=$(pwd) \
 -DbuildDirectory=$(pwd)/build \
 -Dbuilder=$SDK/plugins/org.eclipse.pde.build/templates/package-build \
 -f $SDK/plugins/org.eclipse.pde.build/scripts/build.xml

pushd build/plugins/org.sat4j.core/
%java -cp $SDK/startup.jar \
 -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
 org.eclipse.core.launcher.Main \
 -application org.eclipse.ant.core.antRunner \
 -Duser.home=$home \
 -f build.xml \
 build.update.jar
popd
popd

# pb depends upon core
cp -rp core/build/plugins/org.sat4j.core/org.sat4j.core_*.jar \
 $SDK/plugins

# the class-path in pb's MANIFEST.MF references a versionless core jar.
CORE_VERSION=$(ls $SDK/plugins | grep org.sat4j.core | \
 sed 's/org.sat4j.core_//')
sed -i "s/org.sat4j.core.jar/org.sat4j.core_$CORE_VERSION/" \
 pb/META-INF/MANIFEST.MF
 
pushd pb
mkdir home build
home=$(cd home > /dev/null && pwd)

# These can go away when package build handles plugins (not just
# features)
echo "<project default=\"main\"><target name=\"main\"></target></project>" \
 > build/assemble.org.sat4j.pb.all.xml
echo "<project default=\"main\"><target name=\"main\"></target></project>" \
 > build/package.org.sat4j.pb.all.xml

%java -cp $SDK/startup.jar \
 -Duser.home=$home \
 -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
 org.eclipse.core.launcher.Main \
 -application org.eclipse.ant.core.antRunner \
 -Dtype=plugin \
 -DjavacSource=1.5 \
 -DjavacTarget=1.5 \
 -Did=org.sat4j.pb \
 -DbaseLocation=$SDK \
 -DsourceDirectory=$(pwd) \
 -DbuildDirectory=$(pwd)/build \
 -Dbuilder=$SDK/plugins/org.eclipse.pde.build/templates/package-build \
 -f $SDK/plugins/org.eclipse.pde.build/scripts/build.xml

pushd build/plugins/org.sat4j.pb
%java -cp $SDK/startup.jar \
 -Dosgi.sharedConfiguration.area=%{_libdir}/eclipse/configuration \
 org.eclipse.core.launcher.Main \
 -application org.eclipse.ant.core.antRunner \
 -Duser.home=$home \
 -f build.xml \
 build.update.jar
popd
popd

# For testing
#cd core/build.upstream
#mkdir -p bin report/junit
#ant tests

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
cp -rp core/build/plugins/org.sat4j.core/org.sat4j.core_*.jar \
 $RPM_BUILD_ROOT%{_javadir}
cp -rp pb/build/plugins/org.sat4j.pb/org.sat4j.pb_*.jar \
 $RPM_BUILD_ROOT%{_javadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
# No %%doc files as the about.html is in the jar
%{_javadir}/org.sat4j*
