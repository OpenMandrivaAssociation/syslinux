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
Source4:	syslinux.rpmlintrc
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
	TFTPBOOT=%tftpbase  EXTLINUXDIR=/boot/extlinux \
	LDLINUX=ldlinux.c32

%ifarch %{x86_64}
make efi64 install netinstall \
	INSTALLROOT=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} \
	AUXDIR=%{_prefix}/lib/%{name} \
	LIBDIR=%{_prefix}/lib DATADIR=%{_datadir} \
	TFTPBOOT=%tftpbase  EXTLINUXDIR=/boot/extlinux \
	MANDIR=%{_mandir} INCDIR=%{_includedir} \
	LDLINUX=ldlinux.c32
%endif

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

%files
%doc COPYING NEWS README doc/*.txt
%{_bindir}/*
%{_prefix}/lib/%{name}/altmbr.bin
%{_prefix}/lib/%{name}/altmbr_c.bin
%{_prefix}/lib/%{name}/altmbr_f.bin
%{_prefix}/lib/%{name}/cat.c32
%{_prefix}/lib/%{name}/chain.c32
%{_prefix}/lib/%{name}/cmd.c32
%{_prefix}/lib/%{name}/cmenu.c32
%{_prefix}/lib/%{name}/config.c32
%{_prefix}/lib/%{name}/cpu.c32
%{_prefix}/lib/%{name}/cpuid.c32
%{_prefix}/lib/%{name}/cpuidtest.c32
%{_prefix}/lib/%{name}/cptime.c32
%{_prefix}/lib/%{name}/debug.c32
%{_prefix}/lib/%{name}/dhcp.c32
%{_prefix}/lib/%{name}/diag/geodsp1s.img.xz
%{_prefix}/lib/%{name}/diag/geodspms.img.xz
%{_prefix}/lib/%{name}/diag/handoff.bin
%{_prefix}/lib/%{name}/disk.c32
%{_prefix}/lib/%{name}/dmi.c32
%{_prefix}/lib/%{name}/dmitest.c32
%{_prefix}/lib/%{name}/dosutil/copybs.com
%{_prefix}/lib/%{name}/dosutil/eltorito.sys
%{_prefix}/lib/%{name}/dosutil/mdiskchk.com
%{_prefix}/lib/%{name}/elf.c32
%{_prefix}/lib/%{name}/ethersel.c32
%{_prefix}/lib/%{name}/gfxboot.c32
%{_prefix}/lib/%{name}/gptmbr.bin
%{_prefix}/lib/%{name}/gptmbr_c.bin
%{_prefix}/lib/%{name}/gptmbr_f.bin
%{_prefix}/lib/%{name}/gpxecmd.c32
%{_prefix}/lib/%{name}/gpxelinux.0
%{_prefix}/lib/%{name}/gpxelinuxk.0
%{_prefix}/lib/%{name}/hexdump.c32
%{_prefix}/lib/%{name}/hdt.c32
%{_prefix}/lib/%{name}/host.c32
%{_prefix}/lib/%{name}/ifcpu.c32
%{_prefix}/lib/%{name}/ifcpu64.c32
%{_prefix}/lib/%{name}/ifplop.c32
%{_prefix}/lib/%{name}/ifmemdsk.c32
%{_prefix}/lib/%{name}/isohdpfx.bin
%{_prefix}/lib/%{name}/isohdpfx_c.bin
%{_prefix}/lib/%{name}/isohdpfx_f.bin
%{_prefix}/lib/%{name}/isohdppx.bin
%{_prefix}/lib/%{name}/isohdppx_c.bin
%{_prefix}/lib/%{name}/isohdppx_f.bin
%{_prefix}/lib/%{name}/isolinux-debug.bin
%{_prefix}/lib/%{name}/isolinux.bin
%{_prefix}/lib/%{name}/isolinux-i586.bin
%{_prefix}/lib/%{name}/isolinux-x86_64.bin
%{_prefix}/lib/%{name}/kbdmap.c32
%{_prefix}/lib/%{name}/kontron_wdt.c32
%{_prefix}/lib/%{name}/ldlinux.c32
%{_prefix}/lib/%{name}/lfs.c32
%{_prefix}/lib/%{name}/linux.c32
%{_prefix}/lib/%{name}/libcom32.c32
%{_prefix}/lib/%{name}/libgpl.c32
%{_prefix}/lib/%{name}/liblua.c32
%{_prefix}/lib/%{name}/libmenu.c32
%{_prefix}/lib/%{name}/libutil.c32
%{_prefix}/lib/%{name}/lpxelinux.0
%{_prefix}/lib/%{name}/ls.c32
%{_prefix}/lib/%{name}/lua.c32
%{_prefix}/lib/%{name}/mboot.c32
%{_prefix}/lib/%{name}/mbr.bin
%{_prefix}/lib/%{name}/mbr_c.bin
%{_prefix}/lib/%{name}/mbr_f.bin
%{_prefix}/lib/%{name}/memdisk
%{_prefix}/lib/%{name}/meminfo.c32
%{_prefix}/lib/%{name}/menu.c32
%{_prefix}/lib/%{name}/pci.c32
%{_prefix}/lib/%{name}/pcitest.c32
%{_prefix}/lib/%{name}/pmload.c32
%{_prefix}/lib/%{name}/poweroff.c32
%{_prefix}/lib/%{name}/prdhcp.c32
%{_prefix}/lib/%{name}/pxelinux.0
%{_prefix}/lib/%{name}/pxechn.c32
%{_prefix}/lib/%{name}/pwd.c32
%{_prefix}/lib/%{name}/reboot.c32
%{_prefix}/lib/%{name}/rosh.c32
%{_prefix}/lib/%{name}/sanboot.c32
%{_prefix}/lib/%{name}/sdi.c32
%{_prefix}/lib/%{name}/syslinux.com
%{_prefix}/lib/%{name}/syslinux.c32
%{_prefix}/lib/%{name}/sysdump.c32
%{_prefix}/lib/%{name}/vesa.c32
%{_prefix}/lib/%{name}/vesainfo.c32
%{_prefix}/lib/%{name}/vesamenu.c32
%{_prefix}/lib/%{name}/vpdtest.c32
%{_prefix}/lib/%{name}/whichsys.c32
%{_prefix}/lib/%{name}/zzjson.c32
%{_mandir}/man1/*.1*

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
