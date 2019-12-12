%global srcname keylime

Name:    keylime
Version: 5.4.1
Release: 1%{?dist}
Summary: Open source TPM software for Bootstrapping and Maintaining Trust

BuildArch:      noarch

URL:            https://github.com/keylime/keylime
Source0:        https://github.com/keylime/keylime/archive/%{version}.tar.gz
# Main program: BSD
# Icons: MIT
License: BSD and MIT

BuildRequires: swig
BuildRequires: openssl-devel
BuildRequires: python3-setuptools
BuildRequires: python3-devel
BuildRequires: systemd
BuildRequires: systemd-rpm-macros

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

install -pm 644 %{srcname}.conf \
    %{buildroot}%{_sysconfdir}/%{srcname}.conf

install -pm 644 ./services/%{srcname}_agent.service \
    %{buildroot}%{_unitdir}/%{srcname}_agent.service

install -pm 644 ./services/%{srcname}_verifier.service \
    %{buildroot}%{_unitdir}/%{srcname}_verifier.service

install -pm 644 ./services/%{srcname}_agent.service \
    %{buildroot}%{_unitdir}/%{srcname}_registrar.service

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
%{_bindir}/%{srcname}_provider_platform_init
%{_bindir}/%{srcname}_provider_registrar
%{_bindir}/%{srcname}_provider_vtpm_add
%{_bindir}/%{srcname}_userdata_encrypt
%{_bindir}/%{srcname}_ima_emulator
%{_bindir}/%{srcname}_webapp
%config(noreplace) %{_sysconfdir}/%{srcname}.conf
%{_unitdir}/*

%changelog
* Thu Dec 12 2019 Luke Hinds <lhinds@redhat.com> 5.4.1-1
– Initial Packaging
