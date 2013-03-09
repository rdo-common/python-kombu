%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global srcname kombu

Name:           python-%{srcname}
Version:        2.5.7
Release:        1%{?dist}
Summary:        AMQP Messaging Framework for Python

Group:          Development/Languages
# utils/functional.py contains a header that says Python
License:        BSD and Python
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/k/%{srcname}/%{srcname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-nose
BuildRequires:  python3-setuptools
BuildRequires:  python3-anyjson
# for python3 tests
BuildRequires:  python3-mock
BuildRequires:  python3-nose-cover3
BuildRequires:  python3-coverage
%endif # if with_python3

BuildRequires:  python-setuptools
BuildRequires:  python-nose
BuildRequires:  python-anyjson
BuildRequires:  python-amqplib

# required for tests:
BuildRequires: python-nose-cover3
BuildRequires: python-unittest2
BuildRequires: python-coverage
BuildRequires: python-mock
BuildRequires: python-simplejson
BuildRequires: PyYAML
BuildRequires: python-msgpack
# For documentation
#BuildRequires:  pymongo python-sphinx
#This causes tests error, needs fixing upstream. Incompatible with python > 2.7
#BuildRequires:  python-couchdb

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

Requires:       python3

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
%if 0%{?with_python3}
cp -a . %{py3dir}
%endif


%build
%{__python} setup.py build

# build python3-kombu
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3


%install
%{__python} setup.py install --skip-build --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif # with_python3


# Documentation in docs folder is not useful without doing a make
# Seems to have a circular dependency.  Not building for now
#cd docs && make html
#cd - && mv docs/.build/html htmldocs
#rm -rf docs
#rm -f htmldocs/.buildinfo

# sadly, tests don't succeed, yet
#%check
#%{__python} setup.py test
#
#%if 0%{?with_python3}
#pushd %{py3dir}
#%{__python3} setup.py test
#popd
#%endif # with_python3

%files
%doc AUTHORS Changelog FAQ LICENSE READ* THANKS TODO examples/
%{python_sitelib}/%{srcname}/
%{python_sitelib}/%{srcname}*.egg-info

%if 0%{?with_python3}
%files -n python3-kombu
%doc AUTHORS Changelog FAQ LICENSE READ* THANKS TODO examples/
%{python3_sitelib}/*
%endif # with_python3


%changelog
* Sat Mar 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.7-1
- update to latest upstream version 2.5.7

* Mon Feb 11 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.6-1
- update to latest upstream version 2.5.6

* Sat Feb 09 2013 Fabian Affolter <mail@fabian-affolter.ch> - 2.5.5-1
- update to latest upstream version 2.5.5

* Thu Dec 13 2012 Matthias Runge <mrunge@redhat.com> - 2.5.4-1
- update to upstream version 2.5.4 (rhbz#886001)

* Tue Dec 04 2012 Matthias Runge <mrunge@redhat.com> - 2.5.3-1
- update to latest upstream version 2.5.3

* Mon Nov 26 2012 Matthias Runge <mrunge@redhat.com> - 2.4.10-1
- update to latest upstream version 2.4.10

* Tue Nov 06 2012 Matthias Runge <mrunge@redhat.com> - 2.4.8-1
- update to new upstream version 2.4.8

* Thu Sep 20 2012 Matthias Runge <mrunge@redhat.com> - 2.4.7-1
- update to new upstream version 2.4.7

* Sun Aug 26 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.4.3-1
- update to new upstream version 2.4.3

* Thu Aug 23 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.4.0-1
- update to new upstream version 2.4.0

* Wed Aug 03 2012 Matthias Runge <mrunge@matthias-runge.de> - 2.3.2-1
- update to version 2.3.2
- enable tests
- require python2 and/or python3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.1.3-1
- initial spec.  
- derived from the one written by Fabian Affolter
- spec patch from Lakshmi Narasimhan

