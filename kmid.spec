%define    svn_date 20080213

Name:           kmid
Version:        2.0
Release:        0.14.%{svn_date}svn%{?dist}
Summary:        A midi/karaoke player for KDE

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://extragear.kde.org

# Creation of tarball from svn
#
# Kevin Kofler enhanced the create_tarball.rb script from upstream to also support kmid
# This script also download the translations and docs
# To use it you will need the script itself and a config.ini in the same directory
#
# http://repo.calcforge.org/f9/kde4-tarballs/create_tarball.rb
# http://repo.calcforge.org/f9/kde4-tarballs/config.ini
#
# To create a new checkout use it with anonymous svn access
# ./create_tarball.rb -n
# At the prompt you have to enter "kmid" (without brackets)


# remove content with unknown copyright status
#
# kmid is shipping some non-code content with unknown copyright status
# these files are removed here and the CMakelists.txt is patched for this:
#
# rm -rf kmid-2.0-svn
# tar xjf kmid-2.0-svn.tar.bz2
# rm -rf kmid-2.0-svn/examples
# sed -i -e '/add_subdirectory( examples )/d' kmid-2.0-svn/CMakeLists.txt
# tar cjf kmid-2.0-svn-patched.tar.bz2 kmid-2.0-svn

Source0:        %{name}-%{version}-svn-patched.tar.bz2

# fix CMakeLists.txt so this builds as a standalone directory (without all of extragear-multimedia)
Patch0:         kmid-2.0-svn-cmakelists.patch
Patch1:         kmid-2.0-svn-docsdir.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  kdelibs4-devel >= 4
BuildRequires:  kde-filesystem >= 4
BuildRequires:  cmake
BuildRequires:  alsa-lib-devel
BuildRequires:  gettext
BuildRequires:  desktop-file-utils

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }
Requires:       kdelibs4 >= %{version}
Requires:       oxygen-icon-theme
Requires:       %{name}-common = %{version}-%{release}
Requires(post): /sbin/ldconfig xdg-utils
Requires(postun): /sbin/ldconfig xdg-utils 

%description
KMid is a midi/karaoke file player, with configurable midi mapper, real 
Session Management, drag & drop, customizable fonts, etc. It has a very 
nice interface which let you easily follow the tune while changing the 
color of the lyrics.
It supports output through external synthesizers, AWE, FM and GUS cards.
It also has a keyboard view to see the notes played by each instrument.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for %{name}

%package common
Group:          System Environment/Libraries
Summary:        Common files for kmid
BuildArch:      noarch

%description common
This package includes the common files for kmid.

%prep
%setup -qn %{name}-%{version}-svn
%patch0 -p1 -b .cmakelists
%patch1 -p1 -b .docsdir


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} -D CMAKE_CXX_FLAGS:STRING="${CXXFLAGS} -fno-strict-aliasing" ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
mkdir %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}


desktop-file-install --vendor ""                          \
        --dir %{buildroot}%{_datadir}/applications/kde4   \
        --add-category Midi                               \
        %{buildroot}%{_datadir}/applications/kde4/kmid.desktop


%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig ||:
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :

%postun
/sbin/ldconfig ||:
xdg-icon-resource forceupdate --theme hicolor 2> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING COPYING.DOC COPYING.LIB PEOPLE README
%exclude %{_docdir}/HTML/en/kmid/
%{_kde4_bindir}/kmid
%{_kde4_appsdir}/kmid/
%{_kde4_datadir}/applications/kde4/kmid.desktop
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_datadir}/dbus-1/interfaces/org.kde.KMid.xml
%{_kde4_iconsdir}/hicolor/*/apps/kmid.png
%{_kde4_libdir}/libkmidlib.so.*
%{_kde4_libdir}/liblibkmid.so.*
%{_kde4_libdir}/kde4/*

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/libkmid/
%{_kde4_libdir}/libkmidlib.so
%{_kde4_libdir}/liblibkmid.so

%files common
%defattr(-,root,root,-)
%{_docdir}/HTML/en/kmid/

%changelog
* Fri Jun 18 2010 Lukas Tinkl <ltinkl@redhat.com> - 2.0-0.14.20080213svn
- Resolves: #599387 - RPMdiff run failed for package kmid-2.0-0.10.20080213svn.el6
  (fix strange cmake syntax)

* Thu Jun 17 2010 Lukas Tinkl <ltinkl@redhat.com> - 2.0-0.13.20080213svn
- Resolves: #599387 - RPMdiff run failed for package kmid-2.0-0.10.20080213svn.el6
  (fix aliasing issues the proper way using cmake)

* Thu Jun 17 2010 Lukas Tinkl <ltinkl@redhat.com> - 2.0-0.12.20080213svn
- Resolves: #599387 - RPMdiff run failed for package kmid-2.0-0.10.20080213svn.el6
  (fix aliasing issues)

* Wed Jun 16 2010 Lukas Tinkl <ltinkl@redhat.com> - 2.0-0.11.20080213svn
- Resolves: #599387 - RPMdiff run failed for package kmid-2.0-0.10.20080213svn.el6
  (mark the -common subpackage as noarch)

* Mon May 24 2010 Lukas Tinkl <ltinkl@redhat.com> - 2.0-0.10.20080213svn
- Resolves: #587236 - MultilibConflicts in i686 and x86_64 packages
  (created -common subpackage)

* Wed Sep 23 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 2.0-0.9.20080213svn
- Update desktop file according to F-12 FedoraStudio feature

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.8.20080213svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.7.20080213svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.0-0.6.20080213svn
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.0-0.5.20080213svn
- rebuild for NDEBUG and _kde4_libexecdir

* Mon Mar 03 2008 Sebastian Vahl <fedora@deadbabylon.de> - 2.0-0.4.20080213svn
- add default %%defattr(-,root,root,-) also for devel files
- include "svn" in release tag
- remove non-code content with unknown copyright status from tarball and package
- remove KDE version from summary

* Fri Feb 15 2008 Sebastian Vahl <fedora@deadbabylon.de> - 2.0-0.3.20080213
- Requires: kdelibs4 >= %%{version}
- Requires: oxygen-icon-theme

* Wed Feb 13 2008 Sebastian Vahl <fedora@deadbabylon.de> - 2.0-0.2.20080213
- prepare spec for review
- new svn checkout: 2008-02-13
- license is GPLv2+
- rename patches

* Sun Feb 10 2008 Sebastian Vahl <fedora@deadbabylon.de> - 2.0-0.2.20080203
- use tarball created by Kevin Kofler
- switch to %%{svn_date} instead of svn revision

* Sun Jan 27 2008 Sebastian Vahl <fedora@deadbabylon.de> - 2.0-0.1.767336
- svn revision 767336
- Initial version kmid from extragear for KDE4
