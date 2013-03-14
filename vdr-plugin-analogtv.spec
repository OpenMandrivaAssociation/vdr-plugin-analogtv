%define plugin	analogtv

Summary:	VDR plugin: Watch analogue TV
Name:		vdr-plugin-%plugin
Version:	1.0.00
Release:	22
Group:		Video
License:	GPL
URL:		http://www.ko0l.de/download/vdr/analogtv/
Source:		http://www.ko0l.de/download/vdr/analogtv/download/vdr-%plugin-%version.tar.bz2
Source2:	channels.conf.analogue.generic
Patch1:		analogtv-1.0.00-i18n-1.6.patch
Patch2:		analogtv-update-ffmpeg-params.patch
Patch3:		analogtv-fix-bitrate-menudescription.patch
Patch4:		analogtv-displaystatus-loglevel3.patch
Patch5:		analogtv-fix-non-x86.patch
Patch6:		analogtv-threadsafety.patch
Patch7:		analogtv-default-syslog.patch
# from e-tobi:
Patch10:	analogtv-sane-c++.patch
BuildRequires:	vdr-devel >= 1.6.0-7
BuildRequires:	libdvb-devel
BuildRequires:	libalsa-devel
BuildRequires:	jpeg-devel
Requires:	vdr-abi = %vdr_abi

%description
With the help of this plugin you could connect any analogue equipment
to your VDR:
 - bttv compatible analogue tv-cards (i.e. Hauppauge WinTV ...) to
   watch tv-channels which are only available analogue at your location
 - video grabber cards or the s-video input of your tv-card to connect
   your good old VHS-recorder and convert your old recordings into
   *.vdr files
 - your camcorder to watch your vacation videos on the tv-set
 - a webcam (maybe via USB) and watch yourself watching tv ;-)
 - your good old turntable to record your vinyl discs with the vdr

If your card doesn't have an MPEG encoder, you have to install a
supported software MPEG encoder (mp1e is recommended).

%prep
%setup -q -n %plugin-%version
%apply_patches

cp -a %SOURCE2 .

rm examples/hoerzu2vdr/channelid.Radio.conf

# No need for own cSchedules anymore, this is already handled by VDR.
sed -i 's,^NEED_OWN_SIP,#&,' Makefile

# README confuses too much with the old CA id
perl -pi -e 's/32001/A0/' README*

chmod 0644 examples/*.conf.*

%vdr_plugin_prep

%build
%ifarch %ix86
# fails build otherwise
VDR_PLUGIN_EXTRA_FLAGS="-fno-PIC"
%endif
%vdr_plugin_build

%install
%vdr_plugin_install

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README* PROBLEMS HOWTO HISTORY FAQ *.list examples CREDITS ChannelMap.h
%doc channels.conf.analogue.generic




%changelog
* Sun Jun 27 2010 Anssi Hannula <anssi@mandriva.org> 1.0.00-20mdv2010.1
+ Revision: 549191
- fix module load on non-x86 (fix-non-x86.patch, #59681); previous hacks
  were incorporated into this proper patch as well
- use direct syslog output by default (default-syslog.patch, fixes
  VDR startup when "any" is used in VDR_PLUGINS variable)
- fix non-threadsafe calls to time functions (threadsafety.patch)
- fix bitrate description in configuration menu
  (fix-bitrate-menudescription.patch)
- update FFmpeg params for current FFmpeg (update-ffmpeg-params.patch)
- disable private SIP, no longer needed with current VDR
- clean some C++ code (sane-c++.patch from e-tobi)

* Tue Jul 28 2009 Anssi Hannula <anssi@mandriva.org> 1.0.00-19mdv2010.0
+ Revision: 401088
- rebuild for new VDR
- adapt for vdr flags changes, bump buildrequires
- build player-analogtv.c with correct flags as well
- disable hardcoded -march and -mcpu in Makefile
- enable non-x86 build by disabling HAVE_FAST_MEMCPY and skipping
  cpuinfo.c and cpu_accel.c completely

* Fri Mar 20 2009 Anssi Hannula <anssi@mandriva.org> 1.0.00-18mdv2009.1
+ Revision: 359277
- rebuild for new vdr

* Mon Apr 28 2008 Anssi Hannula <anssi@mandriva.org> 1.0.00-17mdv2009.0
+ Revision: 197894
- rebuild for new vdr

* Sat Apr 26 2008 Anssi Hannula <anssi@mandriva.org> 1.0.00-16mdv2009.0
+ Revision: 197626
- add vdr_plugin_prep
- bump buildrequires on vdr-devel
- adapt to gettext i18n of VDR 1.6 (semi-automatic patch)

* Fri Jan 04 2008 Anssi Hannula <anssi@mandriva.org> 1.0.00-15mdv2008.1
+ Revision: 145014
- rebuild for new vdr

* Fri Jan 04 2008 Anssi Hannula <anssi@mandriva.org> 1.0.00-14mdv2008.1
+ Revision: 144969
- rebuild for new vdr
- adapt for changed vdr optflags scheme

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 29 2007 Anssi Hannula <anssi@mandriva.org> 1.0.00-13mdv2008.1
+ Revision: 103055
- rebuild for new vdr

* Sun Jul 08 2007 Anssi Hannula <anssi@mandriva.org> 1.0.00-12mdv2008.0
+ Revision: 49964
- rebuild for new vdr

* Thu Jun 21 2007 Anssi Hannula <anssi@mandriva.org> 1.0.00-11mdv2008.0
+ Revision: 42051
- rebuild for new vdr

* Sat May 05 2007 Anssi Hannula <anssi@mandriva.org> 1.0.00-10mdv2008.0
+ Revision: 22693
- rebuild for new vdr


* Tue Dec 05 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-9mdv2007.0
+ Revision: 90886
- rebuild for new vdr

* Tue Oct 31 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-8mdv2007.1
+ Revision: 73939
- rebuild for new vdr
- Import vdr-plugin-analogtv

* Thu Sep 07 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-7mdv2007.0
- rebuild for new vdr

* Fri Aug 25 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-6mdv2007.0
- fix mangled description

* Thu Aug 24 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-5mdv2007.0
- stricter abi requires
- compile with -fno-PIC, otherwise build fails

* Mon Aug 07 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-4mdv2007.0
- rebuild for new vdr

* Wed Jul 26 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-3mdv2007.0
- rebuild for new vdr

* Tue Jun 20 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-2mdv2007.0
- rebuild for new vdr

* Tue Jun 13 2006 Anssi Hannula <anssi@mandriva.org> 1.0.00-1mdv2007.0
- 1.0.00
- fix URL
- ship ChannelMap.h, don't ship patches
- drop mp1e, it's in a separate package already
- drop patches 1, 2, 3, fixed upstream
- patch4: flood the syslog on debug levels 3+ only
- fixes for better compatibility with Mandriva ffmpeg
- replace 32001 with A0 in README
- x86 only for now (fixing should be trivial, as no functions are asm-only)

* Mon Jun 12 2006 Anssi Hannula <anssi@mandriva.org> 0.9.39-0.20060610.2mdv2007.0
- buildrequires jpeg-devel

* Sun Jun 11 2006 Anssi Hannula <anssi@mandriva.org> 0.9.39-0.20060610.1mdv2007.0
- initial Mandriva release

