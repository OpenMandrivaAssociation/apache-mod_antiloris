#Module-Specific definitions
%define mod_name mod_antiloris
%define mod_conf B53_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Protect apache against the slowloris attack
Name:		apache-%{mod_name}
Version:	0.4
Release: 	%mkrel 4
Group:		System/Servers
License:	Apache License
URL:		ftp://ftp.monshouwer.eu/pub/linux/mod_antiloris/
Source0:	ftp://ftp.monshouwer.eu/pub/linux/mod_antiloris/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Source2:	README
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
With this module, apache is protected against the slowloris attack. The module
limits the number of threads in READ state on a per IP basis. 

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}
cp %{SOURCE2} README

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README ChangeLog	
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
