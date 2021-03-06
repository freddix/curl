Summary:	A utility for getting files from remote servers (FTP, HTTP, and others)
Name:		curl
Version:	7.42.1
Release:	1
License:	MIT-like
Group:		Applications/Networking
Source0:	http://curl.haxx.se/download/%{name}-%{version}.tar.bz2
# Source0-md5:	296945012ce647b94083ed427c1877a8
URL:		http://curl.haxx.se/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libssh2-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	rtmpdump-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	openssl-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cURL is a tool for getting files with URL syntax, supporting FTP,
HTTP, HTTPS, GOPHER, TELNET, DICT, FILE and LDAP. cURL supports HTTP
POST, HTTP PUT, FTP uploading, HTTP form based upload, proxies,
cookies, user+password authentication and a busload of other useful
tricks. The main use for curl is when you want to get or send files
automatically to or from a site using one of the supported protocols.

cURL is a tool for getting files from FTP, HTTP, Gopher, Telnet, and
Dict servers, using any of the supported protocols. cURL is designed
to work without user interaction or any kind of interactivity. cURL
offers many useful capabilities, like proxy support, user
authentication, FTP upload, HTTP post, and file transfer resume.

%package libs
Summary:	curl library
Group:		Libraries

%description libs
curl library.

%package devel
Summary:	Header files and development documentation for curl library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rtmpdump-devel

%description devel
Header files and development documentation for curl library.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-ldap			\
	--disable-ldaps			\
	--disable-static		\
	--enable-ipv6			\
	--enable-manual			\
	--enable-threaded-resolver	\
	--enable-versioned-symbols	\
	--with-ca-bundle=/etc/ssl/certs/ca-certificates.crt	\
	--with-random=/dev/urandom	\
	--with-ssl=%{_prefix}		\
	--without-libidn
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES COPYING README docs/{BUGS,FAQ,FEATURES,HISTORY,KNOWN_BUGS,MANUAL,SSLCERTS,THANKS,TODO,TheArtOfHttpScripting}
%attr(755,root,root) %{_bindir}/curl
%{_mandir}/man1/curl.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libcurl.so.4
%attr(755,root,root) %{_libdir}/libcurl.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc docs/{CONTRIBUTE,INTERNALS,LICENSE-MIXING,RESOURCES}
%attr(755,root,root) %{_bindir}/curl-config
%attr(755,root,root) %{_libdir}/libcurl.so
%{_libdir}/libcurl.la
%{_includedir}/curl
%{_aclocaldir}/libcurl.m4
%{_pkgconfigdir}/libcurl.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*curl*.3*

