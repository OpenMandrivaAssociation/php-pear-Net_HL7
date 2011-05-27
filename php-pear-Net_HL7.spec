%define		_class		Net
%define		_subclass	HL7
%define		upstream_name	%{_class}_%{_subclass}

Name:		php-pear-%{upstream_name}
Version:	0.1.0
Release:	%mkrel 12
Summary:	HL7 messaging API
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/Net_HL7/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tar.bz2
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
This package provides an HL7 API for creating, sending and
manipulating HL7 messages. HL7 is a protocol on the 7th OSI layer
(hence the '7' in HL7) for messaging in Health Care environments. HL7
means 'Health Level 7'. HL7 is a protocol with a wealth of semantics
that defines hundreds of different messages and their meaning, but
also defines the syntactics of composing and sending messages. The API
is focused on the syntactic level of HL7, so as to remain as flexible
as possible. The package is a translation of the Perl HL7 Toolkit and
will be kept in sync with this initiative.

%prep
%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%doc %{upstream_name}-%{version}/docs/*
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml
