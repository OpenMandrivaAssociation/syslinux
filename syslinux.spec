%define name syslinux
%define version 3.51
%define release %mkrel 4

%define tftpbase /var/lib/tftpboot
%define pxebase %{tftpbase}/X86PC/linux

Summary:	A bootloader for linux using floppies, CD
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
Source0:	http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.bz2
Source1:	pxelinux-help.txt
Source2:	pxelinux-messages
Source3:	pxelinux-default
Url:		http://syslinux.zytor.com/
BuildRoot:	%{_tmppath}/%{name}-buildroot/
BuildRequires:	nasm >= 0.97, netpbm
BuildRequires:	libpng-source
# (blino) rediffed from opensuse 3.31 patch
# modified mostly about lsr stuff in add_crc and Makefile
Patch1:		syslinux-3.51-gfxboot.patch
Patch2:		syslinux-3.20-date.patch
ExclusiveArch:	%{ix86} x86_64
Obsoletes:	isolinux < %{version}
Provides:	isolinux = %{version}
Conflicts:	pxelinux <= 3.11-1mdk

%description
SYSLINUX is a boot loader for the Linux operating system which
operates off an MS-DOS/Windows FAT filesystem.  It is intended to
simplify first-time installation of Linux, and for creation of rescue-
and other special-purpose boot disks.

%package -n pxelinux
Summary:	A PXE bootloader
Group:		System/Kernel and hardware
Requires:	syslinux

%description -n pxelinux
PXELINUX is a PXE bootloader.

%package devel
Summary: Development environment for SYSLINUX add-on modules
Group: Development/Other
Requires:	tftp-server
Requires:	syslinux
Conflicts:	pxe < 1.4.2-8mdk
Obsoletes:	pxelinux-devel
Provides:	pxelinux-devel

%description devel
The SYSLINUX boot loader contains an API, called COM32, for writing
sophisticated add-on modules.  This package contains the libraries
necessary to compile such modules.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .gfxboot
%patch2 -p1 -b .date
# (blino) overwrite bundled libpng files with system one
# we can't link directly with libpng.a since the com32 library
# is build with a specific libc
install %{_prefix}/src/libpng/*.h com32/include
rm -rf com32/lib/libpng
install -d com32/lib/libpng
install %{_prefix}/src/libpng/*.c com32/lib/libpng

%build
chmod +x add_crc
%make DATE="Mandriva Linux"
mv isolinux.bin isolinux.bin.normal

perl -pi -e 's,^(isolinux_dir.*)/isolinux,$1/x86_64/isolinux,' isolinux.asm
%make DATE="Mandriva Linux" isolinux.bin
mv isolinux.bin isolinux-x86_64.bin

perl -pi -e 's,^(isolinux_dir.*)/x86_64/isolinux,$1/i586/isolinux,' isolinux.asm
%make DATE="Mandriva Linux" isolinux.bin
mv isolinux.bin isolinux-i586.bin

mv isolinux.bin.normal isolinux.bin

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%make install \
  INSTALLROOT=$RPM_BUILD_ROOT \
  BINDIR=%{_bindir} \
  SBINDIR=%{_sbindir} \
  LIBDIR=%{_prefix}/lib \
  INCDIR=%{_includedir}

mkdir -p $RPM_BUILD_ROOT/%{_prefix}/lib/%{name}/menu
cp -av menu/*  $RPM_BUILD_ROOT/%{_prefix}/lib/%{name}/menu/

cp gethostip sha1pass mkdiskimage sys2ansi.pl keytab-lilo.pl $RPM_BUILD_ROOT/%{_prefix}/lib/syslinux

install -d $RPM_BUILD_ROOT%{pxebase}/pxelinux.cfg/
install -m 0644 %SOURCE1 $RPM_BUILD_ROOT%{pxebase}/help.txt
install -m 0644 %SOURCE2 $RPM_BUILD_ROOT%{pxebase}/messages
install -m 0644 %SOURCE3 $RPM_BUILD_ROOT%{pxebase}/pxelinux.cfg/default
perl -pi -e "s|VERSION|%version|g" $RPM_BUILD_ROOT%{pxebase}/messages
install -m 0644 pxelinux.0 $RPM_BUILD_ROOT%{pxebase}/linux.0
install -m 0644 memdisk/memdisk $RPM_BUILD_ROOT%{pxebase}/memdisk
install -m 0644 isolinux-i586.bin $RPM_BUILD_ROOT/%{_prefix}/lib/syslinux/
install -m 0644 isolinux-x86_64.bin $RPM_BUILD_ROOT/%{_prefix}/lib/syslinux/

%files
%defattr(-,root,root)
%doc COPYING NEWS README TODO README.usbkey README.menu
%doc syslinux.doc isolinux.doc comboot.doc extlinux.doc distrib.doc keytab-lilo.doc memdisk/memdisk.doc
%{_bindir}/*
%{_sbindir}/*
%exclude %{_prefix}/lib/%{name}/com32
%exclude %{_prefix}/lib/%{name}/menu
%{_prefix}/lib/%{name}/*

%files -n pxelinux
%doc pxelinux.doc
%{pxebase}/*.0
%{pxebase}/memdisk
%config(noreplace) %{pxebase}/messages
%config(noreplace) %{pxebase}/help.txt
%config(noreplace) %{pxebase}/pxelinux.cfg/default

%files devel
%defattr(-,root,root)
%{_prefix}/lib/%{name}/com32
%{_prefix}/lib/%{name}/menu


