%define eclipse_base %{_libdir}/eclipse
# We want the version to match that shipped in Eclipse's Orbit project
%define qualifier 20081021

Name:           sat4j
Version:        2.0.3
Release:        9
Summary:        A library of SAT solvers written in Java

Group:          Development/Java
License:        EPL and LGPLv2
URL:            http://www.sat4j.org/
# Created by sh %{name}-fetch.sh
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}-fetch.sh

#BuildRequires:  java-devel >= 1.6
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  java-rpmbuild
BuildRequires:  ant
Requires:       java >= 1.6
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


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 2.0.3-5mdv2011.0
+ Revision: 669959
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.3-4mdv2011.0
+ Revision: 607511
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 2.0.3-3mdv2010.1
+ Revision: 523963
- rebuilt for 2010.1

* Fri Feb 27 2009 Jérôme Soyer <saispo@mandriva.org> 2.0.3-2mdv2009.1
+ Revision: 345520
- New upstream release
- Remove strict java version

* Fri Feb 27 2009 Jérôme Soyer <saispo@mandriva.org> 2.0.3-1mdv2009.1
+ Revision: 345460
- New upstream release

* Wed Jul 16 2008 Alexander Kurtakov <akurtakov@mandriva.org> 2.0.0-0.6.1mdv2009.0
+ Revision: 236246
- fix group
- import sat4j


