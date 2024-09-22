#
# Conditional build:
%bcond_without	python	# CPython (2.x) module

%define	rel	2
%define	subver	20230423
Summary:	NAT Port Mapping Protocol library and client
Summary(pl.UTF-8):	Biblioteka i program kliencki protokołu NAT Port Mapping Protocol
Name:		libnatpmp
Version:	0
Release:	0.%{subver}.%{rel}
License:	BSD
Group:		Libraries
Source0:	http://miniupnp.tuxfamily.org/files/%{name}-%{subver}.tar.gz
# Source0-md5:	85baa91ffd6a75f411e387f1bfbb1b12
URL:		http://miniupnp.tuxfamily.org/libnatpmp.html
BuildRequires:	/sbin/ldconfig
%if %{with python}
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	python-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NAT Port Mapping Protocol library and client.

%description -l pl.UTF-8
Biblioteka i program kliencki protokołu NAT Port Mapping Protocol.

%package devel
Summary:	Header files for libnatpmp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnatpmp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libnatpmp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnatpmp.

%package static
Summary:	Static libnatpmp library
Summary(pl.UTF-8):	Statyczna biblioteka libnatpmp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libnatpmp library.

%description static -l pl.UTF-8
Statyczna biblioteka libnatpmp.

%package -n python-libnatpmp
Summary:	Python binding for libnatpmp library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki libnatpmp
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libnatpmp
Python binding for libnatpmp library.

%description -n python-libnatpmp -l pl.UTF-8
Wiązanie Pythona do biblioteki libnatpmp.

%prep
%setup -q -n %{name}-%{subver}

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC -Wall -DENABLE_STRNATPMPERR"

%if %{with python}
export CFLAGS="%{rpmcflags}"
%py_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALLPREFIX=$RPM_BUILD_ROOT%{_prefix} \
	INSTALLDIRLIB=$RPM_BUILD_ROOT%{_libdir}

# missing in make install
cp -p natpmp_declspec.h $RPM_BUILD_ROOT%{_includedir}

# let SONAME be the symlink
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libnatpmp.so.{1,1.0}
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

# omitted by Makefile
install -D natpmpc.1 $RPM_BUILD_ROOT%{_mandir}/man1/natpmpc.1

%if %{with python}
%py_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog.txt README LICENSE
%attr(755,root,root) %{_bindir}/natpmpc
%attr(755,root,root) %{_libdir}/libnatpmp.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libnatpmp.so.1
%{_mandir}/man1/natpmpc.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnatpmp.so
%{_includedir}/natpmp.h
%{_includedir}/natpmp_declspec.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libnatpmp.a

%if %{with python}
%files -n python-libnatpmp
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/libnatpmp.so
%{py_sitedir}/libnatpmp-1.0-py*.egg-info
%endif
