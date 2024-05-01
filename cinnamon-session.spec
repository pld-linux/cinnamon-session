%define	translations_version	6.2.2

Summary:	Session support tools for the Cinnamon desktop environment
Summary(pl.UTF-8):	Programy obsługujęce sesję dla środowiska graficznego Cinnamon
Name:		cinnamon-session
Version:	6.2.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
#Source0Download: https://github.com/linuxmint/cinnamon-session/tags
Source0:	https://github.com/linuxmint/cinnamon-session/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	952ef43f6cedd8060011ae9ab30f7ef6
#Source1Download: https://github.com/linuxmint/cinnamon-translations/tags
Source1:	https://github.com/linuxmint/cinnamon-translations/archive/%{translations_version}/cinnamon-translations-%{translations_version}.tar.gz
# Source1-md5:	ca66b0eadc9416ef66384b3b278554ad
URL:		https://github.com/linuxmint/cinnamon-session
BuildRequires:	OpenGL-devel
BuildRequires:	cinnamon-desktop-devel >= 6.0.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.37.3
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	libcanberra-devel
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
# or libelogind
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xapps-devel >= 1.0.4
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-xtrans-devel
BuildRequires:	xz
Requires:	glib2 >= 1:2.37.3
Requires:	cinnamon-desktop >= 6.0.0
Requires:	cinnamon-settings-daemon >= 5.8.0
Requires:	gtk+3 >= 3.0.0
Requires:	xapps >= 1.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME (GNU Network Object Model Environment) is a user-friendly set of
applications and desktop tools to be used in conjunction with a window
manager for the X Window System. GNOME is similar in purpose and scope
to CDE and KDE, but GNOME is based completely on free software.

GNOME session provides the session tools for the the GNOME desktop.

%description -l pl.UTF-8
GNOME (GNU Network Object Model Environment) to zestaw przyjaznych dla
użytkownika aplikacji i narzędzi do używania w połączeniu z zarządcą
okien pod X. GNOME ma podobny cel jak CDE i KDE, ale bazuje całkowicie
na wolnym oprogramowaniu.

Pakiet gnome-session zawiera narzędzia do obsługi sesji dla środowiska
graficznego GNOME.

%prep
%setup -q -a1

%build
%meson build

%ninja_build -C build

%{__make} -C cinnamon-translations-%{translations_version}

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

cd cinnamon-translations-%{translations_version}
for f in usr/share/locale/*/LC_MESSAGES/%{name}.mo ; do
	install -D "$f" "$RPM_BUILD_ROOT/$f"
done
cd ..

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{ie,mo,rue,sco}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
if [ "$1" = "0" ]; then
	%glib_compile_schemas
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README README.md
%attr(755,root,root) %{_bindir}/cinnamon-session
%attr(755,root,root) %{_bindir}/cinnamon-session-quit
%attr(755,root,root) %{_libexecdir}/cinnamon-session-binary
%attr(755,root,root) %{_libexecdir}/cinnamon-session-check-accelerated
%attr(755,root,root) %{_libexecdir}/cinnamon-session-check-accelerated-helper
%{_datadir}/glib-2.0/schemas/org.cinnamon.SessionManager.gschema.xml
%{_datadir}/cinnamon-session
%{_iconsdir}/hicolor/*x*/apps/cinnamon-session-properties.png
%{_iconsdir}/hicolor/scalable/apps/cinnamon-session-properties.svg
%{_mandir}/man1/cinnamon-session.1*
%{_mandir}/man1/cinnamon-session-quit.1*
