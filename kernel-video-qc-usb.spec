# TODO: make qc-usb main package and kernel-* subpackages
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace utility
#
%define	_rel	1
Summary:	Kernel module for Logitech QuickCam USB cameras (new)
Summary(pl.UTF-8):	Moduł jądra do kamer USB Logitech QuickCam (nowy)
Name:		kernel-video-qc-usb
Version:	0.6.5
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/qce-ga/qc-usb-%{version}.tar.gz
# Source0-md5:	6f6787e1dda11ca3b936ad434154f426
URL:		http://qce-ga.sourceforge.net/
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel-module-build >= 3:2.6
%endif
BuildRequires:	rpmbuild(macros) >= 1.118
%if %{with kernel} && %{with dist_kernel}
%requires_releq_kernel
%endif
Requires(post,postun):	/sbin/depmod
# XXX: ?
#Obsoletes:	kernel-smp-video-qc-usb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Logitech QuickCam USB cameras driver (a new one).

%description -l pl.UTF-8
Sterownik do kamer USB Logitech QuickCam (nowy).

%package -n qc-usb
Summary:	Documentation and test program to Logitech QuickCam USB
Summary(pl.UTF-8):	Dokumentacja i program testujący do kamer Logitech QuickCam USB
Release:	%{_rel}
Group:		Base/Kernel

%description -n qc-usb
Documentation and test program to Logitech QuickCam USB.

%description -n qc-usb -l pl.UTF-8
Dokumentacja i program testujący do kamer Logitech QuickCam USB.

%prep
%setup -q -n qc-usb-%{version}

%build
#%%if %{with kernel}
#%{__make} all \
#		CC="%{kgcc}" \
#		INCLUDES="%{rpmcflags} -I. -D__KERNEL_SMP=1 -D__SMP__ -I%{_kernelsrcdir}/include"
#%%endif
%build_kernel_modules -m quickcam

%if %{with userspace}
%{__make} -C testquickcam
# TODO: %{__cc}, %{rpmcflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m quickcam -d misc

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_sbindir}
install testquickcam/testquickcam $RPM_BUILD_ROOT%{_sbindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%if %{with kernel}
%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*
%endif

%if %{with userspace}
%files -n qc-usb
%defattr(644,root,root,755)
%doc *.txt APPLICATIONS CREDITS FAQ README* TODO
%attr(755,root,users) %{_sbindir}/testquickcam
%endif
