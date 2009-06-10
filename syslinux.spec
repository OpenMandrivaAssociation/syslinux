%define name syslinux
%define version 3.82
%define prerelease pre8
%define git_url	git://git.kernel.org/pub/scm/boot/syslinux/syslinux.git

%define tftpbase /var/lib/tftpboot
%define pxebase %{tftpbase}/X86PC/linux

Summary:	A bootloader for linux using floppies, CD
Name:		%{name}
Version:	%{version}
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Kernel and hardware
Source0:	http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.bz2
Source1:	pxelinux-help.txt
Source2:	pxelinux-messages
Source3:	pxelinux-default
Url:		http://syslinux.zytor.com/
BuildRoot:	%{_tmppath}/%{name}-buildroot/
BuildRequires:	nasm >= 0.97, netpbm
BuildRequires:	libpng-source
Patch4:		remove-win32-from-build.patch
# (fc) 3.73-3mdv fix partition table created by isohybrid (pterjan)
Patch6:		syslinux-3.73-fixisohybrid.patch
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
%patch4 -p1 -b .win32
%patch6 -p1 -b .fixisohybrid

# (blino) overwrite bundled libpng files with system one
# we can't link directly with libpng.a since the com32 library
# is build with a specific libc
install %{_prefix}/src/libpng/*.h com32/include
rm -rf com32/lib/libpng
install -d com32/lib/libpng
install %{_prefix}/src/libpng/*.c com32/lib/libpng

%build
%make DATE="Mandriva Linux"
mv core/isolinux.bin core/isolinux.bin.normal

perl -pi -e 's,^(isolinux_dir.*)/isolinux,$1/x86_64/isolinux,' core/isolinux.asm
%make DATE="Mandriva Linux"
mv core/isolinux.bin core/isolinux-x86_64.bin

perl -pi -e 's,^(isolinux_dir.*)/x86_64/isolinux,$1/i586/isolinux,' core/isolinux.asm
%make DATE="Mandriva Linux"
mv core/isolinux.bin core/isolinux-i586.bin

mv core/isolinux.bin.normal core/isolinux.bin

%clean 
rm -rf %{buildroot}

%install
rm -rf %{buildroot}
# AUXDIR is explicitly set because upstream sets AUXDIR to %{_datadir}/%{name}
# but we favour AUXDIR set to %{_prefix}/lib/%{name} for backward compatibility
# with our syslinux 3.63 package
%make install \
  INSTALLROOT=%{buildroot} \
  BINDIR=%{_bindir} \
  SBINDIR=%{_sbindir} \
  LIBDIR=%{_prefix}/lib \
  MANDIR=%{_mandir} \
  INCDIR=%{_includedir} \
  AUXDIR=%{_prefix}/lib/%{name}

mkdir -p %{buildroot}/%{_prefix}/lib/%{name}/menu
cp -av com32/menu/*  %{buildroot}/%{_prefix}/lib/%{name}/menu/

install -d %{buildroot}%{pxebase}/pxelinux.cfg/
install -m 0644 %SOURCE1 %{buildroot}%{pxebase}/help.txt
install -m 0644 %SOURCE2 %{buildroot}%{pxebase}/messages
install -m 0644 %SOURCE3 %{buildroot}%{pxebase}/pxelinux.cfg/default
perl -pi -e "s|VERSION|%version|g" %{buildroot}%{pxebase}/messages
install -m 0644 core/pxelinux.0 %{buildroot}%{pxebase}/linux.0
install -m 0644 memdisk/memdisk %{buildroot}%{pxebase}/memdisk
install -m 0644 core/isolinux-i586.bin %{buildroot}/%{_prefix}/lib/syslinux/
install -m 0644 core/isolinux-x86_64.bin %{buildroot}/%{_prefix}/lib/syslinux/

%files
%defattr(-,root,root)
%doc COPYING NEWS README TODO doc/*.txt
%{_bindir}/*
%{_sbindir}/*
%exclude %{_prefix}/lib/%{name}/com32
%exclude %{_prefix}/lib/%{name}/menu
%{_prefix}/lib/%{name}/*
%{_mandir}/man1/*.1*

%files -n pxelinux
%doc doc/pxelinux.txt
%{pxebase}/*.0
%{pxebase}/memdisk
%config(noreplace) %{pxebase}/messages
%config(noreplace) %{pxebase}/help.txt
%config(noreplace) %{pxebase}/pxelinux.cfg/default

%files devel
%defattr(-,root,root)
%{_prefix}/lib/%{name}/com32
%{_prefix}/lib/%{name}/menu
