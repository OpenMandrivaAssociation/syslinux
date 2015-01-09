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
Patch0:		syslinux-6.03-dont-build-syslinux.exe-as-we-have-no-mingw-available.patch
Patch1:		0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
ExclusiveArch:	%{ix86} x86_64
BuildRequires:	nasm
BuildRequires:	netpbm
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	upx
BuildRequires:	gnu-efi
Provides:	isolinux = %{EVRD}
Requires:	efibootmgr
Requires:	dosfstools
Requires:	mtools
Requires:	upx

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

%package -n extlinux
Summary:	An ext{2|3|4} bootloader
Group:		System/Kernel and hardware

%description -n extlinux
Extlinux is an ext{2|3|4} bootloader.

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
%patch0 -p1 -b .nomingw~
%patch1 -p1 -b .install_all~

%build
export CC="gcc -fuse-ld=bfd"

make CC="$CC" LD="ld.bfd -melf_i386" DATE="OpenMandriva"  bios clean all
%ifarch %{x86_64}
make CC="$CC" LD="ld.bfd" DATE="OpenMandriva"  efi64 clean all
%endif

%install
install -d %{buildroot}{%{_bindir},%{_sbindir},%{_prefix}/lib/%{name},%{_includedir}}
install bios/core/ldlinux.sys %{buildroot}%{_prefix}/lib/%{name}

make bios install-all \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	AUXDIR=%{_prefix}/lib/%{name} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	LDLINUX=ldlinux.c32

%ifarch %{x86_64}
make efi64 install netinstall \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	AUXDIR=%{_prefix}/lib/%{name} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	LDLINUX=ldlinux.c32
%endif

%files
%doc COPYING NEWS README doc/*.txt
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

%files -n extlinux
%doc doc/extlinux.txt
%{_sbindir}/extlinux
%{_prefix}/lib/%{name}/mbr.bin

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
