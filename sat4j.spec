%global eclipse_base %{_libdir}/eclipse
# We want the version to match that shipped in Eclipse's Orbit project
%global qualifier 20100429

Name:           sat4j
Version:        2.3.0
Release:        2
Summary:        A library of SAT solvers written in Java

Group:          Development/Java
License:        EPL or LGPLv2
URL:            http://www.sat4j.org/
# Created by sh %{name}-fetch.sh
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}-fetch.sh
Patch0:         %{name}-classpath.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  java-devel >= 0:1.6
BuildRequires:  ant
BuildRequires:  ecj
Requires:       java >= 0:1.6
Requires:       jpackage-utils

BuildArch:      noarch

%description
The aim of the SAT4J library is to provide an efficient library of SAT
solvers in Java. The SAT4J library targets first users of SAT "black
boxes", those willing to embed SAT technologies into their application
without worrying about the details.

%prep
%setup -q
%patch0 -p0

# Only used for the tests
rm lib/commons-cli.jar

%build
ant -Dbuild.compiler=modern -Drelease=%{version} -DBUILD_DATE=%{qualifier} p2 

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
cp -rp dist/%{version}/org.sat4j.core.jar \
 $RPM_BUILD_ROOT%{_javadir}
cp -rp dist/%{version}/org.sat4j.pb.jar \
 $RPM_BUILD_ROOT%{_javadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
# No %%doc files as the about.html is in the jar
%{_javadir}/org.sat4j*

