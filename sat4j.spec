%{?_javapackages_macros:%_javapackages_macros}
%{?scl:%scl_package sat4j}
%{!?scl:%global pkg_name %{name}}

%global eclipse_base %{_libdir}/eclipse

# should be consistent across one release
%global build_date 20130405

Name:           %{?scl_prefix}sat4j
Version:        2.3.5
Release:        2.0%{?dist}
Summary:        A library of SAT solvers written in Java


License:        EPL or LGPLv2
URL:            http://www.sat4j.org/
# Created by sh %{pkg_name}-fetch.sh
Source0:        %{pkg_name}-%{version}.tar.xz
Source1:        %{pkg_name}-fetch.sh
Patch0:         %{pkg_name}-classpath.patch
BuildRoot:      %{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  java-devel >= 1:1.6
BuildRequires:  ant
BuildRequires:  ecj
Requires:       java >= 1:1.6
Requires:       jpackage-utils
%{?scl:Requires: %scl_runtime}

BuildArch:      noarch

%description
The aim of the SAT4J library is to provide an efficient library of SAT
solvers in Java. The SAT4J library targets first users of SAT "black
boxes", those willing to embed SAT technologies into their application
without worrying about the details.

%prep
%setup -q -n %{pkg_name}-%{version}
%patch0

pushd lib
	ln -s /usr/share/java/commons-beanutils.jar
	ln -s /usr/share/java/commons-logging.jar
	ln -s /usr/share/java/mockito.jar mockito-all-1.9.5.jar
popd

%build
ant -Dbuild.compiler=modern -Drelease=%{version} \
 -Dtarget=1.5 -DBUILD_DATE=%{build_date} p2 


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

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Krzysztof Daniel <kdaniel@redhat.com> 2.3.5-1
- Update to latest upstream.

* Fri May 10 2013 Krzysztof Daniel <kdaniel@redhat.com> 2.3.4-1
- Update to latest upstream.

* Wed Apr 17 2013 Krzysztof Daniel <kdaniel@redhat.com> 2.3.3-7
- Remove jars from source.

* Fri Apr 5 2013 Krzysztof Daniel <kdaniel@redhat.com> 2.3.0-6
- Update to 2.3.3
- Initial sclization.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 25 2011 Andrew Overholt <overholt@redhat.com> 2.3.0-2
- Make 1.5-level bytecode.  This enables bootstrapping of Eclipse
  with OpenJDK 7.

* Mon Apr 04 2011 Chris Aniszczyk <zx@redhat.com> 2.3.0-1
- Update to 2.3.0.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 8 2010 Alexander Kurtakov <akurtako@redhat.com> 2.2.0-1
- Update to 2.2.0.

* Tue Mar 30 2010 Andrew Overholt <overholt@redhat.com> 2.1.1-3
- Fix license tag

* Fri Mar 26 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1.1-2
- Switch to lzma tarball.
- Remove classpath in manifest.

* Sun Mar 7 2010 Alexander Kurtakov <akurtako@redhat.com> 2.1.1-1
- Update to 2.1.1.

* Tue Aug 4 2009 Alexander Kurtakov <akurtako@redhat.com> 2.1.0-1
- Update to 2.1.0 final.

* Wed Apr 8 2009 Alexander Kurtakov <akurtako@redhat.com> 2.1.0-0.1.rc2
- Update to 2.1.0.RC2.

* Thu Feb 26 2009 Alexander Kurtakov <akurtako@redhat.com> 2.0.3-1
- Update to 2.0.3.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Andrew Overholt <overholt@redhat.com> 2.0.0-7
- eclipse_base is now libdir/eclipse

* Tue Jul 15 2008 Andrew Overholt <overholt@redhat.com> 2.0.0-6
- Build with OpenJDK (java.util.Scanner)

* Tue Jul 15 2008 Andrew Overholt <overholt@redhat.com> 2.0.0-5
- Use sed instead of dos2unix

* Mon Jul 14 2008 Andrew Overholt <overholt@redhat.com> 2.0.0-4
- Remove jmock JARs
- Don't run tests as part of build

* Mon Jul 14 2008 Andrew Overholt <overholt@redhat.com> 2.0.0-3
- Remove Class-Path from pb MANIFEST.MF

* Mon Jul 14 2008 Andrew Overholt <overholt@redhat.com> 2.0.0-2
- Add eclipse-pde BR for pdebuild script

* Fri Jun 27 2008 Andrew Overholt <overholt@redhat.com> 2.0.0-1
- 2.0.0
- Run tests

* Thu Mar 13 2008 Andrew Overholt <overholt@redhat.com> 2.0-0.1.RC5
- Initial version
