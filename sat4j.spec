%define eclipse_base %{_libdir}/eclipse
# We want the version to match that shipped in Eclipse's Orbit project
%define qualifier 20081021

Name:           sat4j
Version:        2.0.3
Release:        %mkrel 2
Summary:        A library of SAT solvers written in Java

Group:          Development/Java
License:        EPL and LGPLv2
URL:            http://www.sat4j.org/
# Created by sh %{name}-fetch.sh
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-fetch.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  java-devel
BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  junit4
BuildRequires:  eclipse-pde
Requires:       java
Requires:       jpackage-utils

BuildArch:      noarch

%description
The aim of the SAT4J library is to provide an efficient library of SAT
solvers in Java. The SAT4J library targets first users of SAT "black
boxes", those willing to embed SAT technologies into their application
without worrying about the details.

%prep
%setup -q

# Only used for the tests
rm lib/commons-cli.jar

%build
ant -Drelease=%{version} -DBUILD_DATE=%{qualifier} p2

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
%{_javadir}/org.sat4j*
