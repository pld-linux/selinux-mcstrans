Summary:	MCS (Multiple Category System) SELinux service
Summary(pl.UTF-8):	Usługa SELinuksa MCS (Multiple Category System)
Name:		selinux-mcstrans
Version:	3.7
Release:	1
License:	GPL v2
Group:		Daemons
#Source0Download: https://github.com/SELinuxProject/selinux/wiki/Releases
Source0:	https://github.com/SELinuxProject/selinux/releases/download/%{version}/mcstrans-%{version}.tar.gz
# Source0-md5:	64e17a58f2d70c1acb1e4a5e507a289b
Patch0:		mcstrans-init.patch
URL:		https://github.com/SELinuxProject/selinux/wiki
BuildRequires:	gcc >= 6:3.4
BuildRequires:	libcap-devel
BuildRequires:	libselinux-devel >= 3.7
BuildRequires:	libsepol-static >= 3.7
BuildRequires:	pcre2-8-devel
BuildRequires:	pkgconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	libselinux >= 3.7
Requires:	rc-scripts
Obsoletes:	policycoreutils-mcstrans < 2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Security-enhanced Linux is a patch of the Linux kernel and a number of
utilities with enhanced security functionality designed to add
mandatory access controls to Linux. The Security-enhanced Linux kernel
contains new architectural components originally developed to improve
the security of the Flask operating system. These architectural
components provide general support for the enforcement of many kinds
of mandatory access control policies, including those based on the
concepts of Type Enforcement, Role-based Access Control, and
Multi-level Security.

This package contains MCS (Multiple Category System) SELinux service.

%description -l pl.UTF-8
Security-enhanced Linux jest prototypem jądra Linuksa i wielu
aplikacji użytkowych o funkcjach podwyższonego bezpieczeństwa.
Zaprojektowany jest tak, aby w prosty sposób ukazać znaczenie
obowiązkowej kontroli dostępu dla społeczności linuksowej. Ukazuje
również jak taką kontrolę można dodać do istniejącego systemu typu
Linux. Jądro SELinux zawiera nowe składniki architektury pierwotnie
opracowane w celu ulepszenia bezpieczeństwa systemu operacyjnego
Flask. Te elementy zapewniają ogólne wsparcie we wdrażaniu wielu typów
polityk obowiązkowej kontroli dostępu, włączając te wzorowane na: Type
Enforcement (TE), kontroli dostępu opartej na rolach (RBAC) i
zabezpieczeniach wielopoziomowych.

Ten pakiet zawiera usługę SELinuksa MCS (Multiple Category System).

%prep
%setup -q -n mcstrans-%{version}
%patch -P0 -p1

%build
CFLAGS="%{rpmcflags} %{rpmcppflags} -Wall -W -Wundef -Wmissing-noreturn -Wmissing-format-attribute" \
%{__make} \
	CC="%{__cc}" \
	LIBDIR="%{_libdir}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir} \
	SYSTEMDDIR=/lib/systemd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mcstrans
%service mcstrans restart

%preun
if [ "$1" = "0" ]; then
	%service mcstrans stop
	/sbin/chkconfig --del mcstrans
fi

%files
%defattr(644,root,root,755)
%doc TODO
%attr(755,root,root) /sbin/mcstransd
%attr(754,root,root) /etc/rc.d/init.d/mcstrans
%{systemdunitdir}/mcstrans.service
%{_mandir}/man5/setrans.conf.5*
%{_mandir}/man8/mcs.8*
%{_mandir}/man8/mcstransd.8*
