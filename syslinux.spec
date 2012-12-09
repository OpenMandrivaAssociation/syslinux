%define git_url git://git.kernel.org/pub/scm/boot/syslinux/syslinux.git
%define tftpbase /var/lib/tftpboot
%define pxebase %{tftpbase}/X86PC/linux

Summary:    A bootloader for linux using floppies, CD
Name:       syslinux
Version:    4.05
Release:    4
License:    GPLv2+
Group:      System/Kernel and hardware
Url:        http://syslinux.zytor.com/
Source0:    http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.bz2
Source4:    http://www.kernel.org/pub/linux/utils/boot/syslinux/%{name}-%{version}.tar.sign
Source1:    pxelinux-help.txt
Source2:    pxelinux-messages
Source3:    pxelinux-default
Patch4:     remove-win32-from-build.patch
# (fc) 3.73-3mdv fix partition table created by isohybrid (pterjan)
Patch6:     syslinux-3.84-fixisohybrid.patch
Patch7:     syslinux-3.84_remove_keytab-lilo.patch
Patch8:     syslinux-4.05-use-ext2_fs.h-from-e2fsprogs.patch
Patch9:     syslinux-4.05.LD.test.patch
ExclusiveArch:  %{ix86} x86_64
BuildRequires:  nasm
BuildRequires:  netpbm
Buildrequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(ext2fs)
Provides:   isolinux = %{version}

%description
SYSLINUX is a boot loader for the Linux operating system which
operates off an MS-DOS/Windows FAT filesystem.  It is intended to
simplify first-time installation of Linux, and for creation of rescue-
and other special-purpose boot disks.

%package -n pxelinux
Summary:    A PXE bootloader
Group:      System/Kernel and hardware
Requires:   syslinux

%description -n pxelinux
PXELINUX is a PXE bootloader.

%package    perl
Summary:    Syslinux tools written in perl
Group:      System/Kernel and hardware
Requires:   syslinux
Conflicts:  syslinux < 4.05-3

%description    perl
Syslinux tools written in perl.

%package    devel
Summary:    Development environment for SYSLINUX add-on modules
Group:      Development/Other
Requires:   tftp-server
Requires:   syslinux

%description    devel
The SYSLINUX boot loader contains an API, called COM32, for writing
sophisticated add-on modules.  This package contains the libraries
necessary to compile such modules.

%prep
%setup -q
#%patch4 -p1 -b .win32
#%patch6 -p1 -b .fixisohybrid
#%patch7 -p0
%patch8 -p1 -b .ext2fs~
%patch9 -p1

%build
rm -f diag/geodsp/mk-lba-img
%make DATE="%{vendor} Linux" installer

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


%changelog
* Fri Jun 01 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 4.05-4
+ Revision: 801894
- don't try building different builds for loading from different paths
- use ext2_fs.h from e2fsprogs (P8)
- be sure to own %%{_prefix}/lib/%%{name}
- minor cleaning

* Wed Feb 08 2012 Matthew Dawkins <mattydaw@mandriva.org> 4.05-3
+ Revision: 772010
- fixed duplicate files
- split out perl package
- cleaned up spec
- attempt to make spec distro agnostic
- removed legacy conflicts, obsoletes

* Fri Jan 27 2012 Antoine Ginies <aginies@mandriva.com> 4.05-2
+ Revision: 769309
- back to understandable BR.... pkgconfig really sux
- back to understandable BR....
- bump the release
- fix the BR on libpn12-source
- add missing BR libuuid
- use libpng0 instead of libpng15
- add missing BR libpng-devel
- update to release 4.05

* Fri May 13 2011 Eugeni Dodonov <eugeni@mandriva.com> 4.04-1
+ Revision: 674363
- Upgraded to syslinux 4.04, fixes non-bootable 2011 isos issue.

* Fri May 13 2011 Eugeni Dodonov <eugeni@mandriva.com> 3.84-4
+ Revision: 674361
- Rebuild

* Fri May 06 2011 Antoine Ginies <aginies@mandriva.com> 3.84-3
+ Revision: 669880
- bump the release
- remove keytab-lilo script

* Tue Apr 19 2011 Antoine Ginies <aginies@mandriva.com> 3.84-2
+ Revision: 656030
- fix isohybrid.patch

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

  + Christophe Fergeau <cfergeau@mandriva.com>
    - upload 3.84 tarball, some patches are still not rediffed
    - rediff win32 patch for syslinux 3.84

* Fri Nov 06 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.83-1mdv2010.1
+ Revision: 461268
- syslinux 3.83

* Fri Oct 16 2009 Pascal Terjan <pterjan@mandriva.org> 3.82-2mdv2010.0
+ Revision: 457914
- Add a -fatfirst option to isohybrid to create a small fat partition so that Windows does not offer to format the key

* Wed Jun 10 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.82-1mdv2010.0
+ Revision: 384770
- rediff patches for syslinux 3.82

  + Erwan Velu <erwan@mandriva.org>
    - Mandrake is dead :p

* Tue May 05 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.80-1mdv2010.0
+ Revision: 372078
- 3.80
- 3.80pre8
- drop patches that were merged upstream
- fixes the ugly bug #48814

  + Pascal Terjan <pterjan@mandriva.org>
    - Fix partition size in isohybrid for dvd images
    - Preserve id in isohybrid when run several times

* Thu Apr 16 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.75-1mdv2009.1
+ Revision: 367776
- 3.75

* Fri Apr 10 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.74-1mdv2009.1
+ Revision: 365705
- 3.74:
- removed patches merged upstream
- syslinux 3.74pre17
  resync win32 patch

* Wed Apr 01 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.74-0.pre14.1mdv2009.1
+ Revision: 363154
- 3.74-pre14

* Thu Mar 26 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.74-0.pre11.1mdv2009.1
+ Revision: 361326
- Update to 3.74pre11
- Add git url

* Tue Mar 17 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.74-0.pre6.1mdv2009.1
+ Revision: 356608
- 3.74-pre6:
  * remove obsolete patch1 (integrated in 3.74-pre6)

* Mon Mar 09 2009 Pascal Terjan <pterjan@mandriva.org> 3.73-4mdv2009.1
+ Revision: 353256
- isohybrid: no need to shift the end of the partition

* Fri Mar 06 2009 Frederic Crozat <fcrozat@mandriva.com> 3.73-3mdv2009.1
+ Revision: 349946
- Patch6 (pterjan): fix partition table created by isohybrid

  + Christophe Fergeau <cfergeau@mandriva.com>
    - More accurate licensing information

* Thu Feb 26 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.73-2mdv2009.1
+ Revision: 345176
- Add patch for gfxboot to make it parse DEFAULT entries in isolinux.cfg

* Mon Jan 26 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.73-1mdv2009.1
+ Revision: 333647
- syslinux 3.73
  reorder patches in a more logical order, fix content of README.gfxboot

* Fri Jan 23 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.72-1mdv2009.1
+ Revision: 332733
- Pick UI directive patch from syslinux git since it the cleanest way to start GFXBOOT upon isolinux startup
- syslinux 3.72
  gethostip, sha1pass, mkdiskimage, syslinux2ansi.pl, keytab-lilo.pl are now
  installed in /usr/bin (as upstream). syslinux2ansi and keytab-lilo lost their
  .pl suffix

  + Olivier Blin <blino@mandriva.org>
    - remove date patch (fixed upstream)
    - remove duplicate local_boot code, upstream factorized it
    - remove string now defined upstream
    - adapt to cwritestr being renamed as writestr
    - rediff gfxboot patch
    - 3.71

* Mon Aug 11 2008 Olivier Blin <blino@mandriva.org> 3.63-1mdv2009.0
+ Revision: 270715
- package README.gfxboot
- fix doc installation
- fix manpages installation
- sys2ansi has been renamed syslinux2ansi
- use updated gfxboot patch from opensuse
- 3.63

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 3.51-6mdv2009.0
+ Revision: 225587
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.51-5mdv2008.1
+ Revision: 179591
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Aug 08 2007 Pixel <pixel@mandriva.com> 3.51-4mdv2008.0
+ Revision: 60126
- move files from /usr/lib64/syslinux to /usr/lib/syslinux
  (since they really are no x86_64 files)

* Tue Aug 07 2007 Anssi Hannula <anssi@mandriva.org> 3.51-3mdv2008.0
+ Revision: 59569
- build on x86_64 as well

* Wed Jul 18 2007 Erwan Velu <erwan@mandriva.org> 3.51-2mdv2008.0
+ Revision: 53300
- Adding missing documentation

* Wed Jul 11 2007 Olivier Blin <blino@mandriva.org> 3.51-1mdv2008.0
+ Revision: 51245
- overwrite bundled libpng files with system one (and drop patch trying to link with system one, it can't work since the com32 lib use a specific libc)
- rediff gfxboot patch
- 3.51
- drop vfat patch (merged upstream)


* Mon Jan 29 2007 Olivier Blin <oblin@mandriva.com> 3.35-1mdv2007.0
+ Revision: 114837
- 3.35
- rediff opensuse gfxboot patch

* Fri Nov 17 2006 Olivier Blin <oblin@mandriva.com> 3.31-1mdv2007.1
+ Revision: 85219
- rediff patch10
- update gfxboot (from OpenSuse package)
- delete mime-type property
- remove mime-type property
- remove bzipped patches
- bunzip patches
- 3.31
- use system libpng not to be subject to png 1.2.8 bugs
- Import syslinux

* Thu Sep 21 2006 Olivier Blin <blino@mandriva.com> 3.20-3mdv2007.0
- Patch2: correctly pass DATE when running make in subdirs
- remove extra backslash in DATE (#25966)

* Mon Aug 28 2006 Warly <warly@mandriva.com> 3.20-2mdv2007.0
- also add a isolinux-x86_64 for x86_64 only CDs

* Mon Aug 28 2006 Olivier Blin <blino@mandriva.com> 3.20-1mdv2007.0
- 3.20
- rediff Patch1

* Sat Aug 12 2006 Erwan Velu <erwan@seanodes.com> 3.11-7mdv2007.0
- Adding gethostip, sha1pass
- Adding menu & libmenu to devel

* Sun Aug 06 2006 Olivier Blin <blino@mandriva.com> 3.11-6mdv2007.0
- fix default pxelinux configuration installation

* Fri Jul 14 2006 Warly <warly@mandriva.com> 3.11-5mdv2007.0
- revert isolinux.bin default dir
- add an extra isolinux-i586.bin for dual arch CDs

* Fri Jun 30 2006 Warly <warly@mandriva.com> 3.11-4mdk2007.0
- change boot dir from /isolinux to /i586/isolinux

* Sat Jun 24 2006 Olivier Blin <oblin@mandriva.com> 3.11-3mdv2007.0
- reupload because of broken rpmctl that applies and (re)computes
  commands hours later, packages being merged meanwhile...

* Fri Jun 23 2006 Olivier Blin <oblin@mandriva.com> 3.11-2mdv2007.0
- conflicts with previous pxelinux packages (thanks Pixel)

* Fri Jun 23 2006 Olivier Blin <oblin@mandriva.com> 3.11-1mdv2007.0
- 3.11
- switch to Mandriva Linux
- remove old 1.67 version (used for mkbootdisk only?)
- drop ASM graphic patch, not maintained anymore (Patch1)
- drop Patch4 (was a backport from 2.06)
- rediff Patch0
- Patch1: GFX support and build fixes (CLK_TCK)
  (courtesy of openSUSE, thanks dudes!)
- package mkdiskimage
- merge back with pxelinux src package

* Sat Jul 23 2005 Erwan Velu <velu@seanodes.com> 1.76-18mdk
- Splitting pxelinux

* Mon Feb 21 2005 Erwan Velu <velu@seanodes.com> 1.76-17mdk
- Adding mkdiskimage

* Wed Dec 15 2004 Erwan Velu <velu@seanodes.com> 1.76-16mdk
- Add a devel package for the com32 library added in 2.12.
- New pxelinux 2.13
- Removing patch5

* Thu Aug 19 2004 Erwan Velu <erwan@mandrakesoft.com> 1.76-15mdk
- New pxelinux 2.11

* Thu Aug 05 2004 Olivier Blin <blino@mandrake.org> 1.76-14mdk
- Patch6 for syslinux-1.76 (backport from syslinux-2.06-pre1) :
    Fix problem that would occationally cause a boot failure,
    depending on the length of the kernel

* Sun Jun 20 2004 Erwan Velu <erwan@mandrakesoft.com> 1.76-13mdk
- New pxelinux 2.10
- Fixing help.txt & messages
- Removing patch4

* Thu May 06 2004 Erwan Velu <erwan@mandrakesoft.com> 1.76-12mdk
- New pxelinux 2.09
- s/Mandrake Linux/Mandrakelinux/
- Switching from Os to O1 in memdisk
