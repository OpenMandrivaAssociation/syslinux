%define git_url	git://git.kernel.org/pub/scm/boot/syslinux/syslinux.git
%define tftpbase /var/lib/tftpboot
%define pxebase %{tftpbase}/X86PC/linux

Summary:	A bootloader for linux using floppies, CD
Name:		syslinux
Version:	4.05
Release:	3
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://syslinux.zytor.com/
Source0:	http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.bz2
Source4:	http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.sign
Source1:	pxelinux-help.txt
Source2:	pxelinux-messages
Source3:	pxelinux-default
Patch4:		remove-win32-from-build.patch
# (fc) 3.73-3mdv fix partition table created by isohybrid (pterjan)
Patch6:		syslinux-3.84-fixisohybrid.patch
Patch7:		syslinux-3.84_remove_keytab-lilo.patch
ExclusiveArch:	%{ix86} x86_64
BuildRequires:	nasm
BuildRequires:	netpbm
BuildRequires:	libpng12-source
Buildrequires:	pkgconfig(libpng12)
Buildrequires:	pkgconfig(uuid)
Provides:	isolinux = %{version}

%description
SYSLINUX is a boot loader for the Linux operating system which
operates off an MS-DOS/Windows FAT filesystem.  It is intended to
simplify first-time installation of Linux, and for creation of rescue-
and other special-purpose boot disks.

%package -n	pxelinux
Summary:	A PXE bootloader
Group:		System/Kernel and hardware
Requires:	syslinux

%description -n	pxelinux
PXELINUX is a PXE bootloader.

%package	perl
Summary:	Syslinux tools written in perl
Group:		System/Kernel and hardware
Requires:	syslinux
Conflicts:	syslinux < 4.05-3

%description	perl
Syslinux tools written in perl.

%package	devel
Summary:	Development environment for SYSLINUX add-on modules
Group:		Development/Other
Requires:	tftp-server
Requires:	syslinux

%description	devel
The SYSLINUX boot loader contains an API, called COM32, for writing
sophisticated add-on modules.  This package contains the libraries
necessary to compile such modules.

%prep
%setup -q
#%patch4 -p1 -b .win32
#%patch6 -p1 -b .fixisohybrid
#%patch7 -p0

# (blino) overwrite bundled libpng files with system one
# we can't link directly with libpng.a since the com32 library
# is build with a specific libc
install %{_prefix}/src/libpng/*.h com32/include
rm -rf com32/lib/libpng
install -d com32/lib/libpng
install %{_prefix}/src/libpng/*.c com32/lib/libpng

%build
rm -f diag/geodsp/mk-lba-img
%make DATE="%{vendor} Linux"
mv core/isolinux.bin core/isolinux.bin.normal

perl -pi -e 's,^(isolinux_dir.*)/isolinux,$1/x86_64/isolinux,' core/isolinux.asm
%make DATE="%{vendor} Linux"
mv core/isolinux.bin core/isolinux-x86_64.bin

perl -pi -e 's,^(isolinux_dir.*)/x86_64/isolinux,$1/i586/isolinux,' core/isolinux.asm
%make DATE="%{vendor} Linux"
mv core/isolinux.bin core/isolinux-i586.bin

mv core/isolinux.bin.normal core/isolinux.bin

%install
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
