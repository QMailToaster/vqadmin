Name:      vqadmin
Summary:   Web Administration for qmail-toaster
Version:   2.3.7
Release:   0%{?dist}
License:   GPL
Group:     Networking/Other
Vendor:    QmailToaster
Packager:  Eric Shubert <qmt-build@datamatters.us>
URL:       http://inter7.com/index.php?page=vqadmin
Source:    http://inter7.com/vqadmin/%{name}-%{version}.tar.gz
Source1:   vqadmin.module
Patch0:    vqadmin.template.patch
Patch1:    vqadmin.valias.patch
Patch2:    vqadmin.chrome.patch
Patch3:    vqadmin.html.patch
Patch4:    vqadmin.vpopmail.devel.patch
Patch5:    vqadmin.vpopmail.ver.patch
BuildRequires: libvpopmail-static
BuildRequires: mysql-devel >= 5.0.22
BuildRequires: perl
Requires:  control-panel
Requires:  mysql >= 5.0.22
Requires:  vpopmail
Obsoletes: vqadmin-toaster
BuildRoot: %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}

%define apacheuser    apache
%define apachegroup   apache
%define debug_package %{nil}
%define basedir       %{_datadir}/toaster
%define vqadmdir      %{basedir}/vqadmin

#-------------------------------------------------------------------------------
%description
#-------------------------------------------------------------------------------
vqadmin is a web based control panel that allows system administrators
to perform actions which require root access — for example, adding and
deleting domains. The cgi is authenticated using Apache style htpasswd files.
A user based ACL provides control over what actions can be performed,
such as adding/deleting a domain or accessing user email account information
to allow modification of user passwords and quotas.
Account service restrictions include enabling or disabling of pop access,
authentication based smtp relay control, imap server and sqwebmail access. 

#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------

%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch5 -p1

# Patch the templates
#-------------------------------------------------------------------------------
[ -f %{_tmppath}/patch_templates ] && rm -f %{_tmppath}/patch_templates
#
%{__cat} << !EOF! >>%{_tmppath}/patch_templates
#!/bin/sh

ls %{_builddir}/%{name}-%{version}/*.c        >  %{_tmppath}/c.list
ls %{_builddir}/%{name}-%{version}/*.h        >> %{_tmppath}/c.list
ls %{_builddir}/%{name}-%{version}/html/*.html > %{_tmppath}/html.list

# Correggo i path nei riferimenti c
for i in \`cat %{_tmppath}/c.list\`; do
  perl -pi -e 's|html/|%{vqadmdir}/html/|g' \$i
done;

for i in \`cat %{_tmppath}/html.list\`; do
  perl -pi -e 's|/mail/toaster.vqadmin|/mail/vqadmin/toaster.vqadmin|g' \$i
done;

[ -f %{_tmppath}/c.list ] && rm -f %{_tmppath}/c.list
[ -f %{_tmppath}/html.list ] && rm -f %{_tmppath}/html.list
!EOF!

# Setto il piccolo file bash eseguibile, lo eseguo, e lo cancello
chmod u+x %{_tmppath}/patch_templates
%{_tmppath}/patch_templates
[ -f %{_tmppath}/patch_templates ] && rm -f %{_tmppath}/patch_templates

# create vpopmail parameters so we don't need to have vpopmail installed
echo "89"             >vpopmail.uid
echo "89"             >vpopmail.gid
echo "/home/vpopmail" >vpopmail.dir

#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------

# these files are ancient, so get the current ones
cp /usr/lib/rpm/config.guess .
cp /usr/lib/rpm/config.sub   .

%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
      --enable-qmaildir=/var/qmail \
      --enable-vpopuser=vpopmail \
      --enable-vpopgroup=vchkpw \
      --enable-cgibindir=%{basedir}/cgi-bin/ \
      --enable-htmldir=%{vqadmdir}/html

make

#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------
%{__rm} -rf  %{buildroot}
%{__mkdir_p} %{buildroot}%{vqadmdir}
%{__mkdir_p} %{buildroot}%{vqadmdir}/html
%{__mkdir_p} %{buildroot}%{vqadmdir}/docs

%{__install}     html/*   %{buildroot}%{vqadmdir}/html
%{__install}     html/en  %{buildroot}%{vqadmdir}/html/en-us
%{__install} -Dp vqadmin  %{buildroot}%{basedir}/cgi-bin/vqadmin/toaster.vqadmin
%{__install} -Dp vqadmin.acl  %{buildroot}%{basedir}/cgi-bin/vqadmin
%{__install} -Dp %{SOURCE1}   %{buildroot}%{basedir}/include/vqadmin.module

#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------
rm -rf %{buildroot}

#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------
%attr(0755,root,root) %dir %{basedir}
%attr(0755,root,root) %dir %{vqadmdir}
%attr(0755,root,root) %dir %{vqadmdir}/docs
%attr(0755,root,root) %dir %{vqadmdir}/html

%attr(0755,root,root) %dir %{basedir}/cgi-bin/vqadmin

%attr(6755,root,root) %{basedir}/cgi-bin/vqadmin/toaster.vqadmin
%attr(0644,root,root) %{vqadmdir}/html/*
%attr(0644,%{apacheuser},%{apachegroup}) %{basedir}/include/*
%attr(0444,%{apacheuser},%{apachegroup}) %{basedir}/cgi-bin/vqadmin/vqadmin.acl

#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Sat Nov 16 2013 Eric Shubert <eric@datamatters.us> 2.3.7-0.qt
- Migrated to github
- Removed -toaster designation
- Added CentOS 6 support
- Removed unsupported cruft
* Fri Aug 03 2012 Eric Shubert <eric@datamatters.us> 2.3.7-1.4.1
- Added patch to fix language name bug with chrome browsers
* Wed Aug 01 2012 Eric Shubert <eric@datamatters.us> 2.3.7-1.4.0
- Upgraded vqadmin to 2.3.7, in conjunction with vpopmail 5.4.33
* Fri Feb 24 2012 Bharath Chari <qmailtoaster@arachnis.com> 2.3.4-1.4.0
- Changed Build dependencies to >=vpopmail-5.4.33
* Fri Jun 12 2009 Jake Vickers <jake@qmailtoaster.com> 2.3.4-1.3.6
- Added Fedora 11 support
- Added Fedora 11 x86_64 support
* Wed Jun 10 2009 Jake Vickers <jake@qmailtoaster.com> 2.3.4-1.3.6
- Added Mandriva 2009 support
* Thu Apr 23 2009 Jake Vickers <jake@qmailtoaster.com> 2.3.4-1.3.5
- Added Fedora 9 x86_64 and Fedora 10 x86_64 support
- Fixed type in PHP code that could cause a table to display incorrectly
* Mon Feb 16 2009 Jake Vickers <jake@qmailtoaster.com> 2.3.4-1.3.4
- Added Suse 11.1 support
* Mon Feb 09 2009 Jake Vickers <jake@qmailtoaster.com> 2.3.4-1.3.4
- Added Fedora Core 6 support, as well as Fedora 9 and 10 support
* Sat Apr 14 2007 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.3.3
- Add CentOS 5 i386 support
- Add CentOS 5 x86_64 support
* Tue Jul 18 2006 Erik A. Espinoza <espinoza@forcenetworks.com> 2.3.4-1.3.2
- Lame attempt at adding valias support
- Fixed typo in template patch (QVADMIN to VQADMIN)
* Mon Jun 05 2006 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.3.1
- Add SuSE 10.1 support
* Sat May 13 2006 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.13
- Add Fedora Core 5 support
* Sun Nov 20 2005 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.12
- Add SuSE 10.0 and Mandriva 2006.0 support
* Sat Oct 15 2005 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.11
- Add Fedora Core 4 x86_64 support
* Sat Oct 01 2005 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.10
- Add CentOS 4 x86_64 support
* Wed Sep 28 2005 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.9
- Revert back to vqadmin-2.3.4 account stability problems
* Fri Sep 22 2005 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.5a
- Fixed panel scripts to allow mail user account control
* Fri Jul 01 2005 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.5
- Add Fedora Core 4 support
* Fri Jun 03 2005 Torbjorn Turpeinen <tobbe@nyvalls.se> 2.3.4-1.2.4
- Gnu/Linux Mandrake 10.0,10.1,10.2 support
* Sun Feb 27 2005 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.3
- Add Fedora Core 3 support
- Add CentOS support
* Thu Jun 03 2004 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.2
- Add Fedora Core 2 support
* Sun May 09 2004 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.2.1
- Update for qmailtoaster 1.2.1
* Mon Dec 29 2003 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.0.8
- Add Fedora Core 1 support
* Sun Nov 23 2003 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.0.7
- Add Trustix 2.0 support
- Fix images to images-toaster
* Thu May 15 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.3.4-1.0.6
- Red Hat Linux 9.0 support (nick@ndhsoft.com)
- Gnu/Linux Mandrake 9.2 support
- Clean-ups on SPEC: compilation banner, better gcc detects
- Detect gcc-3.2.3
* Mon Mar 31 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.3.4-1.0.5
- Conectiva Linux 7.0 support
- Better managing of apache user (related to distro)
* Sun Feb 15 2003 Nick Hemmesch <nick@ndhsoft.com> 2.3.4-1.0.4
- Support for Red Hat 8.0
* Wed Feb 05 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.3.4-1.0.3
- Support for Red Hat 8.0 thanks to Andrew.J.Kay
* Sat Feb 01 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.3.4-1.0.2
- Redo Macros to prepare supporting larger RPM OS.
  We could be able to compile (and use) packages under every RPM based
  distribution: we just need to write right requirements.
* Sat Jan 25 2003 Miguel Beccari <miguel.beccari@clikka.com> 2.3.4-1.0.1
- Added MDK 9.1 support
- Try to use gcc-3.2.1
- Added very little patch to compile with newest GLIBC
- Support dor new RPM-4.0.4
* Sat Oct 05 2002 Miguel Beccari <miguel.beccari@clikka.com> 2.3.2-0.9.2
- Soft clean-ups
* Sun Sep 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 2.3.2-0.9.1
- RPM macros to detect Mandrake, RedHat, Trustix are OK again. They are
  very basic but they should work.
* Fri Sep 27 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.8.2.3.2-1
- Rebuilded under 0.8 tree.
- Important comments translated from Italian to English.
- Written rpm rebuilds instruction at the top of the file (in english).
- Finished JavaScript controls.
* Sun Sep 22 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.2.3.2-3
- External CSS
- JavaScripts controls (have to finish them)
- Clean-ups
* Thu Aug 29 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.2.3.2-2
- Deleted Mandrake Release Autodetection (creates problems)
* Fri Aug 16 2002 Miguel Beccari <miguel.beccari@clikka.com> 0.7.2.3.2-1
- First RPM release. It comes with toaster templates, toaster layout,
  toaster dependencies: seems to work.

