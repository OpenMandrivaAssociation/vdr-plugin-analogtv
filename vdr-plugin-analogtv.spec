
%define plugin	analogtv
%define name	vdr-plugin-%plugin
%define version	1.0.00
%define rel	19

Summary:	VDR plugin: Watch analogue TV
Name:		%name
Version:	%version
Release:	%mkrel %rel
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
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0-7
BuildRequires:	libdvb-devel
BuildRequires:	libalsa-devel
BuildRequires:	libjpeg-devel
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
rm -rf %{buildroot}
%vdr_plugin_install

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README* PROBLEMS HOWTO HISTORY FAQ *.list examples CREDITS ChannelMap.h
%doc channels.conf.analogue.generic


