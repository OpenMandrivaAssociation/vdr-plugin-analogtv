
%define plugin	analogtv
%define name	vdr-plugin-%plugin
%define version	1.0.00
%define rel	14

Summary:	VDR plugin: Watch analogue TV
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPL
URL:		http://www.ko0l.de/download/vdr/analogtv/
Source:		http://www.ko0l.de/download/vdr/analogtv/download/vdr-%plugin-%version.tar.bz2
Source2:	channels.conf.analogue.generic
Patch4:		analogtv-displaystatus-loglevel3.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.4.7-9
BuildRequires:	libdvb-devel
BuildRequires:	libalsa-devel
BuildRequires:	libjpeg-devel
Requires:	vdr-abi = %vdr_abi
ExclusiveArch:	%ix86

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
%patch4 -p1 -b .status

cp -a %SOURCE2 .

rm examples/hoerzu2vdr/channelid.Radio.conf

perl -pi -e 's/-hq//' player-analogtv.c
sed -i '/sprintf(cmd, "ffmpeg/s,%%s:%%d,%%s,' player-analogtv.c
sed -i '/-ad/s/s.mixer_line,//' player-analogtv.c

# README confuses too much with the old CA id
perl -pi -e 's/32001/A0/' README*

chmod 0644 examples/*.conf.*

%build
VDR_PLUGIN_FLAGS="%vdr_plugin_flags -fno-PIC"
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


