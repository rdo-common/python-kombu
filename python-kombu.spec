%if 0%{?fedora}
%global with_python3 1
%endif

%global srcname kombu

Name:           python-%{srcname}
Version:        3.0.33
Release:        7%{?dist}
Epoch:          1
Summary:        An AMQP Messaging Framework for Python

Group:          Development/Languages
# utils/functional.py contains a header that says Python
License:        BSD and Python
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/k/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0:         563.patch
Patch1:         569.patch
Patch2:         571.patch
Patch3:         577.patch
Patch4:         2124.patch
BuildArch:      noarch

BuildRequires:  python2-devel


BuildRequires:  python-setuptools
BuildRequires:  python-nose
BuildRequires:  python-anyjson

# required for tests:
BuildRequires: python-nose-cover3
BuildRequires: python-coverage
BuildRequires: python-mock
BuildRequires: python-simplejson
BuildRequires: PyYAML
BuildRequires: python-msgpack
BuildRequires: python-amqp
BuildRequires: python-pymongo


# For documentation
#BuildRequires:  pymongo python-sphinx
#This causes tests error, needs fixing upstream. Incompatible with python > 2.7
#BuildRequires:  python-couchdb
Requires: python-amqp >= 1.4.9
Requires: python-anyjson >= 0.3.3

%description
AMQP is the Advanced Message Queuing Protocol, an open standard protocol
for message orientation, queuing, routing, reliability and security.

One of the most popular implementations of AMQP is RabbitMQ.

The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQP protocol, and
also provide proven and tested solutions to common messaging problems.

%if 0%{?with_python3}
%package -n python3-kombu
Summary:        AMQP Messaging Framework for Python3
Group:          Development/Languages

Requires:       python3-amqp
Requires:       python3-anyjson
BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-setuptools
BuildRequires:  python3-anyjson
BuildRequires:  python3-amqp
BuildRequires:  python3-pymongo

# for python3 tests
BuildRequires:  python3-mock
BuildRequires:  python3-nose-cover3
BuildRequires:  python3-coverage
BuildRequires:  python3-nose



%description -n python3-kombu
AMQP is the Advanced Message Queuing Protocol, an open standard protocol
for message orientation, queuing, routing, reliability and security.

One of the most popular implementations of AMQP is RabbitMQ.

The aim of Kombu is to make messaging in Python as easy as possible by
providing an idiomatic high-level interface for the AMQP protocol, and
also provide proven and tested solutions to common messaging problems.

This subpackage is for python3
%endif # with_python3

%prep
%setup -q -n %{srcname}-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

# build python3-kombu
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
### Note: Probably should rm -rf kombu/tests prior to install instead.
#fix non executable test script
chmod +x %{buildroot}/%{python2_sitelib}/kombu/tests/test_serialization.py


%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
### Note: Probably should rm -rf kombu/tests prior to install instead.
#fix non executable test script
chmod +x %{buildroot}/%{python3_sitelib}/kombu/tests/test_serialization.py
sed -i 's!/usr/bin/python$!/usr/bin/python3!' %{buildroot}/%{python3_sitelib}/kombu/tests/test_serialization.py
%endif

%files
%doc AUTHORS Changelog FAQ LICENSE READ* THANKS TODO examples/
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}*.egg-info

%if 0%{?with_python3}
%files -n python3-kombu
%doc AUTHORS Changelog FAQ LICENSE READ* THANKS TODO examples/
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/kombu-%{version}-py%{python3_version}.egg-info
%endif

%changelog
* Fri Aug 05 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-7
- Adds additional patch for 577 which prevents leaking file descriptors in Qpid transport

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.33-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 06 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-5
- Adds patch to fix upstream issue 577

* Tue Feb 23 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-4
- Adds patch to fix upstream issue 569
- Adds patch to fix upstream issue 571

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-2
- Adds patch to fix upstream issue 563 (rhbz#1300811)

* Wed Jan 20 2016 Brian Bouterse <bmbouter@redhat.com> - 1:3.0.33-1
- Update to latest upstream version 3.0.33 (rhbz#1297116)

* Tue Dec 22 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 1:3.0.32-1
- Upstream 3.0.32 (RHBZ#1289079)
- Fix python3 guards
- Bugfix for debug log flooding and redis transport

* Wed Dec 02 2015 Matthias Runge <mrunge@redhat.com> - 1:3.0.29-5
- add requires: python3-anyjson
- minor spec cleanup

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov  9 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 3.0.29-2
- Make it so the python3 subpackage doesn't drag in python2

* Wed Oct 28 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.29-1
- Update to latest upstream version 3.0.29 (rhbz#1275450)

* Thu Oct 15 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.28-1
- Update to latest upstream version 3.0.28 (rhbz#1270505)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 07 2015 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.26-1
- Update to latest upstream version 3.0.26 (rhbz#1214720)

* Fri Nov 21 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.24-1
- Update to latest upstream version 3.0.24 (rhbz#1166402)

* Thu Sep 18 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.23-1
- Update to latest upstream version 3.0.23 (rhbz#1142995)

* Sun Sep 14 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.22-1
- Update to latest upstream version 3.0.22 (rhbz#1118674)

* Tue Jul 15 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 1:3.0.21-2
- reintroduce adjusted conditions for EPEL
- fix permission for a test script

* Sun Jul 13 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 1:3.0.21-1
- update to 3.0.21
- drop conditionals in spec

* Thu Jul 03 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.20-1
- Update to latest upstream version 3.0.20 (rhbz#1114337)

* Mon Jun 23 2014 Fabian Affolter <mail@fabian-affolter.ch> - 1:3.0.19-1
- Update to latest upstream version 3.0.19 (rhbz#1095266)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1:3.0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon May 05 2014 Matthias Runge <mrunge@redhat.com> - 3.0.15-2
- fix broken build
- have files listed only once

* Thu Apr 17 2014 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.15-1
- Update to latest upstream version 3.0.15 (rhbz#1072265)

* Wed Mar 26 2014 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.14-1
- update to 3.0.14 (rhbz#1072265)

* Wed Feb 26 2014 Matthias Runge <mrunge@redhat.com> - 3.0.12-1
- update to 3.0.12 (rhbz#1052424)

* Wed Jan 08 2014 Matthias Runge <mrunge@redhat.com> - 3.0.8-2
- Remove requirements patch, bump epoch to be upgradeable

* Wed Jan 08 2014 Matthias Runge <mrunge@redhat.com> - 3.0.8-1
- Update to 3.0.8 (rhbz#1037549)

* Fri Nov 22 2013 Matthias Runge <mrunge@redhat.com> - 3.0.6-1
- Update to 3.0.6 and enable tests for py3 as well 

* Sun Nov 17 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.5-1
- Updated to latest upstream version 3.0.5 (rhbz#1024916)

* Sat Nov 16 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.4-1
- Update to latest upstream version 3.0.4 (rhbz#1024916)

* Fri Nov 15 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.3-1
- Update to latest upstream version 3.0.3 (rhbz#1024916)

* Sun Nov 03 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.2-1
- Updatd to latest upstream version 3.0.2 (rhbz#1024916)

* Mon Oct 28 2013 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.1-1
- Update to latest upstream version 3.0.1 (rhbz#1019148)

* Mon Oct 14 2013 Matthias Runge <mrunge@redhat.com> - 2.5.15-2
- Enable tests for python2

* Mon Oct 14 2013 Matthias Runge <mrunge@redhat.com> - 2.5.15-1
- Update to 2.5.15 (rhbz#1016271)

* Sun Aug 25 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.14-1
- Update to latest upstream version 2.5.14 (rhbz#1000696)

* Wed Aug 21 2013 Matthias Runge <mrunge@redhat.com> - 2.5.13-1
- Update to latest upstream version 2.5.13 (rhbz#998104)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.12-1
- Update to latest upstream version 2.5.12

* Mon Jun 24 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 2.5.10-2
- Add requires on python-amqp/python3-amqp. resolves rhbz#974684
- Fix rpmlint warnings about macro in comments

* Sun Apr 21 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.10-1
- Update to latest upstream version 2.5.10

* Sat Mar 23 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.8-1
- Update to latest upstream version 2.5.8

* Sat Mar 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.7-1
- Update to latest upstream version 2.5.7

* Mon Feb 11 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.6-1
- Update to latest upstream version 2.5.6

* Sat Feb 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.5-1
- Update to latest upstream version 2.5.5

* Thu Dec 13 2012 Matthias Runge <mrunge@redhat.com> - 2.5.4-1
- Update to upstream version 2.5.4 (rhbz#886001)

* Tue Dec 04 2012 Matthias Runge <mrunge@redhat.com> - 2.5.3-1
- Update to latest upstream version 2.5.3

* Mon Nov 26 2012 Matthias Runge <mrunge@redhat.com> - 2.4.10-1
- Update to latest upstream version 2.4.10

* Tue Nov 06 2012 Matthias Runge <mrunge@redhat.com> - 2.4.8-1
- Update to new upstream version 2.4.8

* Thu Sep 20 2012 Matthias Runge <mrunge@redhat.com> - 2.4.7-1
- Update to new upstream version 2.4.7

* Sun Aug 26 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.4.3-1
- Update to new upstream version 2.4.3

* Thu Aug 23 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.4.0-1
- Update to new upstream version 2.4.0

* Fri Aug 03 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.3.2-1
- Update to version 2.3.2
- Enable tests
- Require python2 and/or python3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.1.3-1
- Initial spec
- Derived from the one written by Fabian Affolter
- Spec patch from Lakshmi Narasimhan

