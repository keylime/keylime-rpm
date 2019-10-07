%global srcname keylime
%define name keylime
%define version 5.1.0
%define release 5

Name:    %{name}
Version: %{version}
Release: %{release}
Summary: Open source TPM software for Bootstrapping and Maintaining Trust

BuildArch:      noarch

Group: Development/Libraries
Vendor: Keylime Developers
URL:            https://github.com/keylime/keylime
Source0:        https://github.com/keylime/keylime/archive/%{version}.tar.gz
License: MIT

AutoReq: no

BuildRequires: swig
BuildRequires: openssl-devel
BuildRequires: python3-setuptools
BuildRequires: python3-devel
BuildRequires: systemd

Requires: procps-ng
Requires: python3-pyyaml
Requires: python3-m2crypto
Requires: python3-cryptography
Requires: python3-tornado
Requires: python3-simplejson
Requires: python3-requests
Requires: python3-zmq
Requires: tpm2-tss
Requires: tpm2-tools
Requires: tpm2-abrmd

%description
Keylime is a TPM based highly scalable remote boot attestation
and runtime integrity measurement solution.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install
mkdir -p %{buildroot}%{_unitdir}

rm %{buildroot}%{_prefix}/package_default/%{srcname}.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/%{srcname}.conf

install -m 644 ./services/%{srcname}_agent.service \
    %{buildroot}%{_unitdir}/%{srcname}_agent.service

install -m 644 ./services/%{srcname}_verifier.service \
    %{buildroot}%{_unitdir}/%{srcname}_verifier.service

install -m 644 ./services/%{srcname}_agent.service \
    %{buildroot}%{_unitdir}/%{srcname}_registrar.service

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}
%{_bindir}/%{srcname}_verifier
%{_bindir}/%{srcname}_registrar
%{_bindir}/%{srcname}_agent
%{_bindir}/%{srcname}_tenant
%{_bindir}/%{srcname}_ca
%{_bindir}/%{srcname}_provider_platform_init
%{_bindir}/%{srcname}_provider_registrar
%{_bindir}/%{srcname}_provider_vtpm_add
%{_bindir}/%{srcname}_userdata_encrypt
%{_bindir}/%{srcname}_ima_emulator
%{_bindir}/%{srcname}_webapp
%{_prefix}/%{srcname}/static/*
%{_sysconfdir}/%{srcname}.conf
%config(noreplace) %{_sysconfdir}/%{srcname}.conf
%{_unitdir}/*

%defattr(755,root,root)
%{python3_sitelib}/%{srcname}/ca_util.py
%{python3_sitelib}/%{srcname}/cloud_agent.py
%{python3_sitelib}/%{srcname}/cloud_verifier_common.py
%{python3_sitelib}/%{srcname}/cloud_verifier_tornado.py
%{python3_sitelib}/%{srcname}/ima_emulator_adapter.py
%{python3_sitelib}/%{srcname}/provider_platform_init.py
%{python3_sitelib}/%{srcname}/provider_registrar.py
%{python3_sitelib}/%{srcname}/provider_vtpm_add.py
%{python3_sitelib}/%{srcname}/registrar.py
%{python3_sitelib}/%{srcname}/tenant.py
%{python3_sitelib}/%{srcname}/tenant_webapp.py
%{python3_sitelib}/%{srcname}/user_data_encrypt.py

%changelog
* Mon Sep 30 2019 Luke Hinds <lhinds@redhat.com> 5.1.0-5
– Initial Packaging
