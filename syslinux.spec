%define git_url git://git.kernel.org/pub/scm/boot/syslinux/syslinux.git
%define tftpbase /var/lib/tftpboot
%define pxebase %{tftpbase}/X86PC/linux

Summary:	A bootloader for linux using floppies, CD
Name:		syslinux
Epoch:		1
Version:	6.03
Release:	7
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://syslinux.zytor.com/
Source0:	https://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.xz
Source1:	pxelinux-help.txt
Source2:	pxelinux-messages
Source3:	pxelinux-default
Source4:	syslinux.rpmlintrc
Patch0:		syslinux-6.03-dont-build-syslinux.exe-as-we-have-no-mingw-available.patch
Patch1:		0001-Add-install-all-target-to-top-side-of-HAVE_FIRMWARE.patch
# Backport from upstream git master to fix RHBZ #1234653
Patch2: 0035-SYSAPPEND-Fix-space-stripping.patch
# From upstream ML, these should fix some GCC 5 issues, e.g. RHBZ #1263988
# http://www.syslinux.org/archives/2015-September/024317.html
# http://www.syslinux.org/archives/2015-September/024318.html
Patch3: fix-alignment-change-gcc-5.patch
# http://www.syslinux.org/archives/2015-September/024319.html
Patch4: dont-guess-section-alignment.patch
Patch5:	0014_fix_ftbfs_no_dynamic_linker.patch

ExclusiveArch:	%{ix86} %{x86_64}
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
# b/c mbr.bin is in both syslinux & extlinux:
Conflicts:	syslinux < 6.03

%description -n extlinux
Extlinux is an ext{2|3|4} bootloader.

%package efi
Summary:	An efi loader
Group:		System/Kernel and hardware

%description efi
An efi loader.

%package    perl
Summary:    Syslinux tools written in perl
Group:      System/Kernel and hardware
Requires:   syslinux = %{EVRD}
Conflicts:  syslinux < 4.05-3

%description    perl
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
%autopatch -p1

%build
# build fails with ld-gold
mkdir ld
ln -s `which ld.bfd` ld/ld 
export PATH=`pwd`/ld:$PATH

make DATE="%{vendor}" clean || true 

make DATE="%{vendor}" bios

%ifarch %{ix86}
make DATE="%{vendor}" efi32
%endif

%ifarch %{x86_64}
make DATE="%{vendor}" efi64
%endif


%install
TARGETS="bios"

%ifarch %{ix86}
export TARGETS="$TARGETS efi32"
%endif

%ifarch %{x86_64}
export TARGETS="$TARGETS efi64"
%endif

make $TARGETS install \
  INSTALLROOT=%{buildroot} \
  BINDIR=%{_bindir} \
  SBINDIR=%{_sbindir} \
  LIBDIR=%{_prefix}/lib \
  MANDIR=%{_mandir} \
  INCDIR=%{_includedir} \
  AUXDIR=%{_prefix}/lib/%{name} \
  LDLINUX=ldlinux.c32

mkdir -p %{buildroot}/%{_prefix}/lib/%{name}/menu
cp -av com32/menu/*  %{buildroot}/%{_prefix}/lib/%{name}/menu/

install -d %{buildroot}%{pxebase}/pxelinux.cfg/
install -m 0644 %SOURCE1 %{buildroot}%{pxebase}/help.txt
install -m 0644 %SOURCE2 %{buildroot}%{pxebase}/messages
install -m 0644 %SOURCE3 %{buildroot}%{pxebase}/pxelinux.cfg/default
perl -pi -e "s|VERSION|%version|g" %{buildroot}%{pxebase}/messages
install -m 0644 bios/core/pxelinux.0 %{buildroot}%{pxebase}/linux.0
install -m 0644 bios/memdisk/memdisk %{buildroot}%{pxebase}/memdisk
install -m 0644 bios/core/isolinux-*.bin %{buildroot}/%{_prefix}/lib/syslinux/

# This file is already provided by lilo's package
rm -f %{buildroot}/%{_bindir}/keytab-lilo
rm -f doc/keytab-lilo.txt

%files
%doc COPYING NEWS README doc/*.txt
%{_bindir}/gethostip
%{_bindir}/isohybrid
%{_bindir}/memdiskfind
%{_bindir}/syslinux
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/*
%exclude %{_prefix}/lib/%{name}/efi*
%{_mandir}/man1/gethostip*
%{_mandir}/man1/syslinux*
%{_mandir}/man1/isohybrid*
%{_mandir}/man1/memdiskfind*
%exclude %{_mandir}/man1/syslinux2ansi*
%exclude %{_prefix}/lib/%{name}/com32
%exclude %{_prefix}/lib/%{name}/menu

%files efi
%{_prefix}/lib/%{name}/efi*/*

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
%{_mandir}/man1/extlinux*

%files perl
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
