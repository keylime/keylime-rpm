%global srcname keylime

Name:    keylime
Version: 6.1.0
Release: 1%{?dist}
Summary: Open source TPM software for Bootstrapping and Maintaining Trust

BuildArch:      noarch

URL:            https://github.com/keylime/keylime
Source0:        https://github.com/keylime/keylime/archive/%{version}.tar.gz
# Main program: BSD
# Icons: MIT
License: ASL 2.0 and MIT

BuildRequires: swig
BuildRequires: openssl-devel
BuildRequires: python3-setuptools
BuildRequires: python3-devel
BuildRequires: python3-dbus
BuildRequires: systemd
BuildRequires: systemd-rpm-macros

Requires: procps-ng
Requires: python3-alembic
Requires: python3-pyasn1
Requires: python3-pyyaml
Requires: python3-m2crypto
Requires: python3-cryptography
Requires: python3-tornado
Requires: python3-simplejson
Requires: python3-sqlalchemy
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
mkdir -p %{buildroot}/%{_sharedstatedir}/keylime

install -pm 644 %{srcname}.conf \
    %{buildroot}%{_sysconfdir}/%{srcname}.conf

install -pm 644 ./services/%{srcname}_agent.service \
    %{buildroot}%{_unitdir}/%{srcname}_agent.service

install -pm 644 ./services/%{srcname}_verifier.service \
    %{buildroot}%{_unitdir}/%{srcname}_verifier.service

install -pm 644 ./services/%{srcname}_agent.service \
    %{buildroot}%{_unitdir}/%{srcname}_registrar.service

cp -r ./tpm_cert_store %{buildroot}%{_sharedstatedir}/keylime/

%post
%systemd_post %{srcname}_agent.service
%systemd_post %{srcname}_verifier.service
%systemd_post %{srcname}_registrar.service

%preun
%systemd_preun %{srcname}_agent.service
%systemd_preun %{srcname}_verifier.service
%systemd_preun %{srcname}_registrar.service

%postun
%systemd_postun_with_restart %{srcname}_agent.service
%systemd_postun_with_restart %{srcname}_verifier.service
%systemd_postun_with_restart %{srcname}_registrar.service

%files
%license LICENSE keylime/static/icons/ICON-LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}
%{_bindir}/%{srcname}_verifier
%{_bindir}/%{srcname}_registrar
%{_bindir}/%{srcname}_agent
%{_bindir}/%{srcname}_tenant
%{_bindir}/%{srcname}_ca
%{_bindir}/%{srcname}_migrations_apply
%{_bindir}/%{srcname}_provider_platform_init
%{_bindir}/%{srcname}_provider_registrar
%{_bindir}/%{srcname}_provider_vtpm_add
%{_bindir}/%{srcname}_userdata_encrypt
%{_bindir}/%{srcname}_ima_emulator
%{_bindir}/%{srcname}_webapp
%config(noreplace) %{_sysconfdir}/%{srcname}.conf
%{_unitdir}/*
%{_sharedstatedir}/keylime/tpm_cert_store/*

%changelog
* Wed Feb 24 2021 Luke Hinds <lhinds@redhat.com> 6.0.0-1
- Updating for Keylime release v6.0.0

* Tue Feb 02 2021 Luke Hinds <lhinds@redhat.com> 5.8.1-1
- Updating for Keylime release v5.8.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Luke Hinds <lhinds@redhat.com> 5.8.0-1
- Updating for Keylime release v5.8.0

* Fri Jul 17 2020 Luke Hinds <lhinds@redhat.com> 5.7.2-1
- Updating for Keylime release v5.7.2

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 5.6.2-2
- Rebuilt for Python 3.9

* Fri May 01 2020 Luke Hinds <lhinds@redhat.com> 5.6.2-1
- Updating for Keylime release v5.6.2

* Thu Feb 06 2020 Luke Hinds <lhinds@redhat.com> 5.5.0-1
- Updating for Keylime release v5.5.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 12 2019 Luke Hinds <lhinds@redhat.com> 5.4.1-1
– Initial Packaging
