%{!?python_sitelib:%global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Open source Church presentation and lyrics projection application
Name: OpenLP
Version: 1.9.1.1
Release: 1%{?dist}
Source0: http://downloads.sourceforge.net/openlp/openlp/%{version}/%{name}-%{version}.tar.gz
License: GPLv2
Group: Applications/Multimedia
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

URL: http://openlp.org/

BuildRequires:  desktop-file-utils
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       PyQt4
Requires:       phonon
Requires:       python-BeautifulSoup
Requires:       python-chardet
Requires:       python-lxml
Requires:       python-sqlalchemy
Requires:       hicolor-icon-theme

%description
OpenLP is a church presentation software, for lyrics projection software,
used to display slides of Songs, Bible verses, videos, images, and 
presentations (if OpenOffice.org is installed) using a computer and projector.

%prep
%setup -q 

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --skip-build -O1 --root %{buildroot}

install -m644 -p -D resources/images/openlp-logo-16x16.png \
   %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo-32x32.png \
   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo-48x48.png \
   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo.svg \
   %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/openlp.svg

desktop-file-install \
  --dir %{buildroot}/%{_datadir}/applications \
  resources/openlp.desktop 

mv %{buildroot}%{_bindir}/bible-1to2-converter.py \
   %{buildroot}%{_bindir}/bible-1to2-converter
mv %{buildroot}%{_bindir}/openlp-1to2-converter.py \
   %{buildroot}%{_bindir}/openlp-1to2-converter
mv %{buildroot}%{_bindir}/openlp-remoteclient.py \
   %{buildroot}%{_bindir}/openlp-remoteclient
mv %{buildroot}%{_bindir}/openlp.pyw %{buildroot}%{_bindir}/openlp


%post
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:


%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc copyright.txt LICENSE
%{_bindir}/bible-1to2-converter
%{_bindir}/openlp-1to2-converter
%{_bindir}/openlp-remoteclient
%{_bindir}/openlp
%{_datadir}/applications/openlp.desktop
%{_datadir}/icons/hicolor/*/apps/openlp.*
%{python_sitelib}/openlp/
%{python_sitelib}/OpenLP-%{version}*.egg-info
%doc documentation/*.txt

%changelog
* Sun Mar 28 2010 Tim Bentley <timbentley@openlp.org> 1.9.1.1
- Initial build version - Alpha 1 Release
