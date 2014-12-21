%define git_url git://git.kernel.org/pub/scm/boot/syslinux/syslinux.git
%define tftpbase /var/lib/tftpboot
%define pxebase %{tftpbase}/X86PC/linux

Summary:	A bootloader for linux using floppies, CD
Name:		syslinux
Epoch:		1
Version:	6.03
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://syslinux.zytor.com/
Source0:	https://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.xz
Source1:	pxelinux-help.txt
Source2:	pxelinux-messages
Source3:	pxelinux-default
ExclusiveArch:	%{ix86} x86_64
BuildRequires:	nasm
BuildRequires:	netpbm
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(ext2fs)
Provides:	isolinux = %{EVRD}
Requires:	efibootmgr
Requires:	dosfstools
Requires:	mtools

%description
SYSLINUX is a boot loader for the Linux operating system which
operates off an MS-DOS/Windows FAT filesystem.  It is intended to
simplify first-time installation of Linux, and for creation of rescue-
and other special-purpose boot disks.

%package -n pxelinux
Summary:	A PXE bootloader
Group:		System/Kernel and hardware
Requires:	syslinux = %{EVRD}

%description -n pxelinux
PXELINUX is a PXE bootloader.

%package perl
Summary:	Syslinux tools written in perl
Group:		System/Kernel and hardware
Requires:	syslinux = %{EVRD}
Conflicts:	syslinux < 4.05-3

%description perl
Syslinux tools written in perl.

%package devel
Summary:	Development environment for SYSLINUX add-on modules
Group:		Development/Other
Requires:	tftp-server
Requires:	syslinux = %{EVRD}

%description devel
The SYSLINUX boot loader contains an API, called COM32, for writing
sophisticated add-on modules.  This package contains the libraries
necessary to compile such modules.

%prep
%setup -q

%build
%make CC="%{_cc}" bios
%make CC="%{_cc}" installer
%make CC="%{_cc}" efi64

%install
install -d %{buildroot}{%{_bindir},%{_prefix}/lib/%{name},%{_includedir}}
install bios/core/ldlinux.sys %{buildroot}%{_prefix}/lib/%{name}

%make install \
	firmware="bios efi64" \
	INSTALLROOT=%{buildroot} \
	LIBDIR=%{_prefix}/lib \
	MANDIR=%{_mandir}


%files
%doc NEWS README* doc/*.txt
%{_bindir}/gethostip
%{_bindir}/isohybrid
%{_bindir}/memdiskfind
%{_bindir}/syslinux
%{_sbindir}/extlinux
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/*
%{_mandir}/man1/gethostip*
%{_mandir}/man1/syslinux*
%{_mandir}/man1/extlinux*
%exclude %{_mandir}/man1/syslinux2ansi*
%exclude %{_prefix}/lib/%{name}/com32
%exclude %{_prefix}/lib/%{name}/menu

%files -n pxelinux
%doc doc/pxelinux.txt
%{pxebase}/*.0
%{pxebase}/memdisk
%config(noreplace) %{pxebase}/messages
%config(noreplace) %{pxebase}/help.txt
%config(noreplace) %{pxebase}/pxelinux.cfg/default

%files perl
%{_bindir}/keytab-lilo
%{_bindir}/lss16toppm
%{_bindir}/md5pass
%{_bindir}/mkdiskimage
%{_bindir}/ppmtolss16
%{_bindir}/pxelinux-options
%{_bindir}/sha1pass
%{_bindir}/syslinux2ansi
%{_bindir}/isohybrid.pl
%{_mandir}/man1/lss16toppm*
%{_mandir}/man1/ppmtolss16*
%{_mandir}/man1/syslinux2ansi*

%files devel
%{_prefix}/lib/%{name}/com32
%{_prefix}/lib/%{name}/menu
