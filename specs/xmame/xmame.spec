# $Id$
# Authority: matthias

#define rcver rc2
%define targets %{?!_without_mame:mame} %{?!_without_mess:mess}

%{!?_without_opengl: %{expand %%define opengl true}}
%ifarch %{ix86}
%{!?_without_3dfx:   %{expand %%define 3dfx true}}
%endif

Summary: The X Multi Arcade Machine Emulator
Name: xmame
Version: 0.87cvs
Release: %{?rcver:0.%{rcver}.}1
Source0: http://x.mame.net/download/xmame-%{version}%{?rcver:-%{rcver}}.tar.bz2
# http://cheat.retrogames.com/ 0.81 - 21/04/2004
Source20: http://cheat.retrogames.com/cheat.zip
# http://www.mameworld.net/highscore/ 0.87 - 25/07/2004
Source21: http://www.mameworld.net/highscore/uhsdat087.zip
# http://www.arcade-history.com/ 0.87a - 30/09/2004
Source22: http://www.arcade-history.com/download/history0_87a.zip
# http://www.mameworld.net/mameinfo/ 0.87u1 - 30/09/2004
Source23: http://www.mameworld.net/mameinfo/update/Mameinfo087u1.zip
# http://www.mameworld.net/catlist/ 0.87u1 - 03/10/2004
Source30: http://www.mameworld.net/catlist/files/catver.zip
License: MAME
URL: http://x.mame.net/
Group: Applications/Emulators
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Obsoletes: %{name}-x11 <= 0.87
Obsoletes: %{name}-xgl <= 0.87
BuildRequires: unzip, XFree86-devel, zlib-devel, expat-devel
%{?opengl:BuildRequires: Mesa-devel, libjpeg-devel}
%{?3dfx:BuildRequires: Glide3-devel}
%{!?_without_alsa:BuildRequires: alsa-lib-devel}
%{!?_without_esound:BuildRequires: esound-devel}
%{!?_without_arts:BuildRequires: arts-devel}
%ifarch %{ix86} x86_64
%{!?_without_asm68000:BuildRequires: nasm >= 0.98}
%{!?_without_mips3:BuildRequires: nasm >= 0.98}
%endif

%description
This the the *nix port of the almost legendary mame. Mame is an arcade
machine emulator, started in 1997 by Nicola Salmoria. It started out as a
series of emulators for individual games. This series of emulators was
combined into a single multi-game emulator.

The main package contains the docs, data files, and three free games so that
you have your X-Mame ready to run in no time! You will still need to pick
a package containing the main xmame binary though, from either the basic
x11 version, the SDL version or the special OpenGL xgl version.

This version has been compiled for X11 DGA and XV, and OpenGL displays.

Available rpmbuild rebuild options :
--without mame mess asm68000 mips3 effmmx opengl 3dfx
          alsa esound arts opts quietbuild


#package SDL
#Summary: X-Mame arcade game emulator compiled for SDL display
#Group: Applications/Emulators
#Provides: %{name}-bin = %{version}
#BuildRequires: SDL-devel
#
#description SDL
#This the the *nix port of the almost legendary mame. Mame is an arcade
#machine emulator, started in 1997 by Nicola Salmoria. It started out as a
#series of emulators for individual games. This series of emulators was
#combined into a single multi-game emulator.
#
#This version has been compiled for SDL display.


%package -n xmess
Summary: The Multi Emulator Super System
Group: Applications/Emulators
Obsoletes: mess-x11 <= 0.87
Obsoletes: mess-xgl <= 0.87

%description -n xmess
This is the *nix port of MESS. MESS is a free emulator which emulates a
large variety of different systems, including old Atari, Apple, BBC,
Commodore, MSX, ZX Spectrum computers. For full list of supported systems
see http://www.mess.org/


#package -n xmess-SDL
#Summary: The Multi Emulator Super System compiled for SDL display
#Group: Applications/Emulators
#BuildRequires: SDL-devel
#
#description -n xmess-SDL
#This is the *nix port of MESS. MESS is a free emulator which emulates a
#large variety of different systems, including old Atari, Apple, BBC,
#Commodore, MSX, ZX Spectrum computers. For full list of supported systems
#see http://www.mess.org/
#
#This version has been compiled for SDL display.


%prep
%setup -n %{name}-%{version}%{?rcver:-%{rcver}}


%build
%{__rm} -f makefile Makefile; %{__cp} -a makefile.unix Makefile

# For CVS snapshots, there are empty instead of symlinks, so fix that
for dir in contrib doc; do
    if test -d ${dir}; then
        %{__rm} -rf ${dir}
        %{__ln_s} src/unix/${dir}
    fi
done

# Comment out the defaults, to enable overriding with the env variables
%{__perl} -pi -e 's/^CFLAGS/# CFLAGS/g' Makefile
%{__perl} -pi -e 's/^MY_CPU/# MY_CPU/g' Makefile

# Replace lib with lib64 when required
%{__perl} -pi -e 's|/usr/X11R6/lib|/usr/X11R6/%{_lib}|g' Makefile

# Use system expat library
%{__perl} -pi -e 's/^BUILD_EXPAT/# BUILD_EXPAT/g' Makefile

# Make the package build verbose by default (to see opts etc.)
%{?_without_quietbuild: %{__perl} -pi -e 's/^QUIET/# QUIET/g' src/unix/unix.mak}

# The default, if not overwritten below
export PREFIX=%{_prefix}
export CFLAGS="%{optflags}"
export JOY_I386=1
export JOY_PAD=1
%{!?_without_alsa:export SOUND_ALSA=1}
%{!?_without_esound:export SOUND_ESOUND=1}
%{!?_without_arts:export SOUND_ARTS_SMOTEK=1; export SOUND_ARTS_TEIRA=1}

# Optimization flags, CPU type and defaults for the makefile
%ifarch %{ix86}
    export MY_CPU="i386"
    # With FC3 gcc, -mtune is preferred as -mcpu is marked obsolete
    %{!?_without_opts: export CFLAGS="-O3 -g -pipe -march=i386 -mcpu=pentium4 -Wall -fno-merge-constants"}
    %{!?_without_asm68000: export X86_ASM_68000=1}
    %{!?_without_mips3: export X86_MIPS3_DRC=1}
    %{!?_without_effmmx: export EFFECT_MMX_ASM=1}
%endif

%ifarch i686
    %{!?_without_opts: export CFLAGS="-O3 -g -pipe -march=pentium4 -msse2 -mfpmath=sse -Wall -fno-merge-constants"}
%endif

%ifarch athlon
    %{!?_without_opts: export CFLAGS="-O3 -g -pipe -march=athlon-4 -msse2 -mfpmath=sse -Wall -fno-merge-constants"}
%endif

%ifarch ppc
    export MY_CPU="risc"
    %{!?_without_opts: export CFLAGS="-O3 -g -pipe -march=powerpc -Wall -mlongcall -fno-merge-constants"}
%endif

%ifarch x86_64
    export MY_CPU="amd64"
    %{!?_without_opts: export CFLAGS="-O3 -g -pipe -march=k8 -m64 -Wall -fno-merge-constants"}
    %{!?_without_asm68000: export X86_ASM_68000=1}
    %{!?_without_mips3: export X86_MIPS3_DRC=1}
    %{!?_without_effmmx: export EFFECT_MMX_ASM=1}
%endif

# Now, do all the building (this is long!)
for target in %{targets}; do
    %{__make} %{?_smp_mflags} %{?opengl:X11_OPENGL=1} %{?3dfx:X11_GLIDE=1} TARGET=$target
#   %{!?_without_SDL: %{__make} %{?_smp_mflags} DISPLAY_METHOD=SDL TARGET=$target}
done


%install
%{__rm} -rf %{buildroot} _doc _datfiles

# Prepare all the extra .dat files
%{__mkdir} _datfiles
for file in %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}; do
    %{__unzip} -o -d _datfiles/ $file
done

for target in %{targets}; do
    %{__make} install-man \
        INSTALL_USER=`id -un` \
        INSTALL_GROUP=`id -gn` \
        MANDIR=%{buildroot}%{_mandir}/man6 \
        TARGET=$target
done

%{__mkdir_p} %{buildroot}%{_bindir}
for target in %{targets}; do
    %{__install} -m 755 x${target}.x11 %{buildroot}%{_bindir}/x${target}
#   %{!?_without_SDL: %{__install} -m 755 x${target}.SDL %{buildroot}%{_bindir}/}
done
%{?!_without_mame: %{__install} -m 755 chdman romcmp xml2info %{buildroot}%{_bindir}/}

# We don't want all the docs
%{__mkdir_p} _doc/{xmame/html,xmess}
pushd src/unix/doc
    %{__cp} -a {*.html,*.css,img} ../../../_doc/xmame/html/
    %{__cp} -a changes.* dga2.txt multiplayer-readme.txt \
        xmame-doc.txt xmamerc.dist mame/* ../../../_doc/xmame/
    %{__cp} -a xmessrc.dist mess/* ../../../_doc/xmess/
popd

%if %{?_without_mame:0}%{!?_without_mame:1}
# Add all directories
%{__mkdir_p} %{buildroot}%{_datadir}/xmame/{artwork,roms,samples,snap}

# The extra dat files
%{__install} -m 0664 _datfiles/*.dat %{buildroot}%{_datadir}/xmame/

# Install the OpenGL cabinets
%{!?_without_xgl: %{__cp} -a src/unix/cab %{buildroot}%{_datadir}/xmame/}
%endif

%if %{?_without_mess:0}%{!?_without_mess:1}
# Add all directories
%{__mkdir_p} %{buildroot}%{_datadir}/xmess/{artwork,bios,crc,samples,snap,software}
%endif

# Uncompress catver.ini (will be in the docs)
%{__unzip} -o %{SOURCE30}


%clean
%{__rm} -rf %{buildroot}


%if %{?_without_mame:0}%{!?_without_mame:1}
%files
%defattr(-, root, root, 0755)
%doc README _doc/xmame/* contrib/tools/mame-cd 
%doc catver.ini
%{_bindir}/chdman
%{_bindir}/romcmp
%attr(2755, root, games) %{_bindir}/xmame
%{_bindir}/xml2info
%dir %attr(2775, root, games) %{_datadir}/xmame
%dir %attr(2775, root, games) %{_datadir}/xmame/artwork
%attr(-, root, root) %{_datadir}/xmame/cab
%dir %attr(2775, root, games) %{_datadir}/xmame/roms
%dir %attr(2775, root, games) %{_datadir}/xmame/samples
%dir %attr(2775, root, games) %{_datadir}/xmame/snap
%{_datadir}/xmame/*.dat
%{_mandir}/man6/xmame.6*
%endif

#if %{?_without_SDL:0}%{!?_without_SDL:%{?_without_mame:0}%{!?_without_mame:1}}
#files SDL
#attr(2755, root, games) %{_bindir}/xmame.SDL
#endif


%if %{?_without_mess:0}%{!?_without_mess:1}
%files -n xmess
%defattr(-, root, root, 0755)
%doc README _doc/xmess/*
%attr(2755, root, games) %{_bindir}/xmess
%dir %attr(2775, root, games) %{_datadir}/xmess
%dir %attr(2775, root, games) %{_datadir}/xmess/artwork
%dir %attr(2775, root, games) %{_datadir}/xmess/bios
%dir %attr(2775, root, games) %{_datadir}/xmess/crc
%dir %attr(2775, root, games) %{_datadir}/xmess/samples
%dir %attr(2775, root, games) %{_datadir}/xmess/snap
%dir %attr(2775, root, games) %{_datadir}/xmess/software
%{_mandir}/man6/xmess.6.*
%endif

#if %{?_without_SDL:0}%{!?_without_SDL:%{?_without_mess:0}%{!?_without_mess:1}}
#files -n xmess-SDL
#attr(2755, root, games) %{_bindir}/xmess.SDL
#endif


%changelog
* Sun Oct 24 2004 Matthias Saou <http://freshrpms.net/> 0.87cvs-1
- Removed specific sparc opts, please report if broken.
- Removed xgl target, as the OpenGL support is now built in the x11 one.
- Moved the main mame/mess binary into the main pakage, remove wrapper.
- Reworked gcc options, added some for i686 and athlon rebuilds.
- Renamed mmxasm build option to effmmx to be more explicit.
- Disable SDL build for now, as this way, we only have one pakage left!
- Removed x11 DGA, does anyone use that anymore?
- Added Glide3 support to the x11 target.
- Added -fno-merge-constants cflag to workaround unsorted coinage errors.

* Sun Oct  3 2004 Matthias Saou <http://freshrpms.net/> 0.87-1
- Update to 0.87, with the usual related files too.
- Now enable both aRts drivers are they can co-exist.
- Remove explicit binary requires.
- Enable X86_ASM_68000, seems to compile properly now.

* Thu Aug 26 2004 Matthias Saou <http://freshrpms.net/> 0.86-1
- Update to 0.86, with the usual related files too.
- Split off the roms to a separate source package.

* Mon Aug 16 2004 Matthias Saou <http://freshrpms.net/> 0.85-1
- Update to 0.85, with the usual related files too.
- Added romcmp to be included, simplified the chdman and xml2info build.

* Thu Jul 22 2004 Matthias Saou <http://freshrpms.net/> 0.84.1-2
- Add 0.84.2 preview patch to fix xmess xgl build and other improvements.

* Sat Jul 17 2004 Matthias Saou <http://freshrpms.net/> 0.84.1-1
- Update to 0.84.1, with the usual related files too.
- Added the xml2info utility to be built and included.
- Added temporary fix for \" -> " to fix make problems with xgl target.

* Sun Jun 13 2004 Matthias Saou <http://freshrpms.net/> 0.83.1-1
- Update to 0.83.1, with the usual related files too.

* Sun May 16 2004 Matthias Saou <http://freshrpms.net/> 0.82.1-1
- Update to 0.82.1, with the usual related files too.

* Mon May  3 2004 Matthias Saou <http://freshrpms.net/> 0.81.1-1
- Update to 0.81.1, with the usual related files too.
- Added arts support by default.

* Fri Feb 20 2004 Matthias Saou <http://freshrpms.net/> 0.79.1-1
- Update to 0.79.1, with the usual related files too.

* Thu Feb 12 2004 Matthias Saou <http://freshrpms.net/> 0.78.1-3
- Added xmame-0.78.1-fix.patch to fix PPC build.

* Fri Jan 16 2004 Matthias Saou <http://freshrpms.net/> 0.78.1-1
- Update to 0.78.1.
- Updated all related files too.
- Added chdman to the mame build.

* Wed Nov 19 2003 Matthias Saou <http://freshrpms.net/> 0.77.1-1
- Update to 0.77.1.
- Updated all related files too, catver is up-to-date at last.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 0.76.1-2
- Rebuild for Fedora Core 1.

* Sun Oct 26 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.76.1, updated related files too (catver is still 0.74u1 though).

* Tue Sep 16 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.74.1.
- Updated all related files too.

* Sat Aug 16 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.72.1.
- Updated all related files too.

* Sat Jul 19 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.71.1.
- Updated all related files too.
- Added patch to fix build with the MIPS3_DRC.

* Thu Jun 19 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.70.1.
- Updated all related files too.

* Fri Jun 13 2003 Matthias Saou <http://freshrpms.net/>
- Added mips3 build option.

* Tue May 27 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.69.1.
- Updated all extra files.
- Changes to reflect the new doc organisation.
- Replace the default prefix, defaults should work and be coherent now.
- Removed "optional" directories from %{_datadir}/xmame.

* Fri May 22 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.68.1.
- Updated all the extra files to their 0.68 versions.
- Merged Panu's mess additions and new wrapper script.

* Mon Apr 14 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.67.2.
- Update catver and history to 0.67.
- Removed nno longer needed install patch.

* Thu Apr 10 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.67.1.
- Split the free (beer ;-)) roms in a sub-package at last.
- Many spec tweaks.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Thu Mar 20 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.66.2.

* Tue Mar 18 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.66.1, and update all related files.
- Removed now unneeded patches.
- Fix CFLAGS and CPU_TYPE for ppc!

* Sat Feb 22 2003 Matthias Saou <http://freshrpms.net/>
- Build with new blit and xgl patches.
- Re-enable asm68000 on x86.
- Added the OpenGL cabinets to the xgl package.

* Wed Feb 12 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.65.1.
- Disable xgl by default (been broken for some time now).

* Fri Feb  7 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.64.1-rc2.
- Cleanup of the optflags to reflect upstream changes.
- Remove obsolete cpu patch.

* Fri Jan 31 2003 Matthias Saou <http://freshrpms.net/>
- Major changes : Files are now in %%{_datadir}/xmame.
- All directories are now 2775 to allow more to be done by "game" members.
- Removed "snap" link, "cab" directory and added "icons" one.
- Disable asm68000 by default as it's broken.

* Wed Jan 29 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.64.1rc1.
- Updated all associated files and added catver to the docs!
- Added romalizer to the docs + a few cleanups.

* Mon Jan 13 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.62.2.
- Update history to 62b and mameinfo to 4.26.

* Tue Dec 11 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.62.1-rc3.
- Included the latest testing netmame code.

* Mon Dec  2 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.62.1-rc1.

* Mon Nov 25 2002 Matthias Saou <http://freshrpms.net/>
- Cleanup and Sparc fixes thanks to Ralf Ertzinger.

* Fri Nov 15 2002 Matthias Saou <http://freshrpms.net/>
- Updated history data to 62.
- Updated Mameinfo to 4.20.
- Added default ALSA support.
- Fixed missing "samples" directory.

* Thu Nov 14 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.61.1 final.
- Updated highscore data to 7.95.
- Updated history data to 61f.
- Updated Mameinfo to 4.1b.

* Sun Oct 27 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.61.1-pr9.
- Removed XV specific stuff, just add it to the x11 target.
- Moved binaries to %%{_bindir} in order to have them in the search path.
- New %%{_prefix}/lib/games/xmame link to work with gxmame's default config.

* Fri Oct  4 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 8.0.
- Updated all obsolete -malign to -falign.
- Simplified --without stuff.
- Added XV build.

* Wed Sep 25 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.61.1-pr7.

* Tue Aug 20 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.61.1-pr3.

* Tue Aug 13 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.61.1-pr2.

* Thu Jul 18 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.61.1-pr1.

* Mon May 27 2002 Matthias Saou <http://freshrpms.net/>
- Mostly fixes for building on PPC, thanks to Ralf Ertzinger.

* Mon May  6 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.60.1.

* Thu May  2 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt against Red Hat Linux 7.3.
- Added the %{?_smp_mflags} expansion.

* Fri Apr 19 2002 Matthias Saou <http://freshrpms.net/>
- Looking quite good now.
- Update to 0.59.2.
- Added %post and %postun scriptlets for the /usr/bin/xmame link.

* Thu Apr 11 2002 Matthias Saou <http://freshrpms.net/>
- Spec file maturing a bit, still in constant development.

* Sun Jan 13 2002 Matthias Saou <http://freshrpms.net/>
- Spec file rewrite from scratch.

