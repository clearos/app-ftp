
Name: app-ftp
Epoch: 1
Version: 1.4.8
Release: 1%{dist}
Summary: FTP Server
License: GPLv3
Group: ClearOS/Apps
Source: %{name}-%{version}.tar.gz
Buildarch: noarch
Requires: %{name}-core = 1:%{version}-%{release}
Requires: app-base
Requires: app-network
Requires: app-users
Requires: app-groups

%description
The FTP Server provides file management and storage using the standard FTP and FTP Secure protocols

%package core
Summary: FTP Server - Core
License: LGPLv3
Group: ClearOS/Libraries
Requires: app-base-core
Requires: app-ftp-plugin-core
Requires: csplugin-filewatch
Requires: proftpd >= 1.3.4a

%description core
The FTP Server provides file management and storage using the standard FTP and FTP Secure protocols

This package provides the core API and libraries.

%prep
%setup -q
%build

%install
mkdir -p -m 755 %{buildroot}/usr/clearos/apps/ftp
cp -r * %{buildroot}/usr/clearos/apps/ftp/

install -d -m 0755 %{buildroot}/etc/clearos/ftp.d
install -d -m 0755 %{buildroot}/var/clearos/ftp
install -d -m 0755 %{buildroot}/var/clearos/ftp/backup/
install -D -m 0644 packaging/authorize %{buildroot}/etc/clearos/ftp.d/authorize
install -D -m 0644 packaging/filewatch-ftp-configuration.conf %{buildroot}/etc/clearsync.d/filewatch-ftp-configuration.conf
install -D -m 0644 packaging/proftpd.php %{buildroot}/var/clearos/base/daemon/proftpd.php

%post
logger -p local6.notice -t installer 'app-ftp - installing'

%post core
logger -p local6.notice -t installer 'app-ftp-core - installing'

if [ $1 -eq 1 ]; then
    [ -x /usr/clearos/apps/ftp/deploy/install ] && /usr/clearos/apps/ftp/deploy/install
fi

[ -x /usr/clearos/apps/ftp/deploy/upgrade ] && /usr/clearos/apps/ftp/deploy/upgrade

exit 0

%preun
if [ $1 -eq 0 ]; then
    logger -p local6.notice -t installer 'app-ftp - uninstalling'
fi

%preun core
if [ $1 -eq 0 ]; then
    logger -p local6.notice -t installer 'app-ftp-core - uninstalling'
    [ -x /usr/clearos/apps/ftp/deploy/uninstall ] && /usr/clearos/apps/ftp/deploy/uninstall
fi

exit 0

%files
%defattr(-,root,root)
/usr/clearos/apps/ftp/controllers
/usr/clearos/apps/ftp/htdocs
/usr/clearos/apps/ftp/views

%files core
%defattr(-,root,root)
%exclude /usr/clearos/apps/ftp/packaging
%exclude /usr/clearos/apps/ftp/tests
%dir /usr/clearos/apps/ftp
%dir /etc/clearos/ftp.d
%dir /var/clearos/ftp
%dir /var/clearos/ftp/backup/
/usr/clearos/apps/ftp/deploy
/usr/clearos/apps/ftp/language
/usr/clearos/apps/ftp/libraries
%config(noreplace) /etc/clearos/ftp.d/authorize
/etc/clearsync.d/filewatch-ftp-configuration.conf
/var/clearos/base/daemon/proftpd.php
