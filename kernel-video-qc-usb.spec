# TODO: make qc-usb main package and kernel-* subpackages
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace utility
#
%ifarch sparc
%undefine with_smp
%endif
%define	_rel	1
Summary:	Kernel module for Logitech QuickCam USB cameras (new)
Summary(pl.UTF-8):   Moduł jądra do kamer USB Logitech QuickCam (nowy)
Name:		kernel-video-qc-usb
Version:	0.6.3
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/qce-ga/qc-usb-%{version}.tar.gz
# Source0-md5:	3d33380a29a7f92c4eef1f82d61b4ee0
URL:		http://qce-ga.sourceforge.net/
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel-module-build >= 3:2.6}
%endif
BuildRequires:	rpmbuild(macros) >= 1.118
%if %{with kernel} && %{with dist_kernel}
%requires_releq_kernel_up
%endif
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Logitech QuickCam USB cameras driver (a new one).

%description -l pl.UTF-8
Sterownik do kamer USB Logitech QuickCam (nowy).

%package -n kernel-smp-video-qc-usb
Summary:	SMP kernel module for Logitech QuickCam USB cameras
Summary(pl.UTF-8):   Moduł jądra SMP do kamer USB Logitech QuickCam
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with kernel} && %{with dist_kernel}
%requires_releq_kernel_smp
%endif
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-video-qc-usb
Logitech QuickCam USB cameras driver for SMP kernel (a new one).

%description -n kernel-smp-video-qc-usb -l pl.UTF-8
Sterownik do kamer USB Logitech QuickCam dla jądra SMP (nowy).

%package -n qc-usb
Summary:	Documentation and test program to Logitech QuickCam USB
Summary(pl.UTF-8):   Dokumentacja i program testujący do kamer Logitech QuickCam USB
Release:	%{_rel}
Group:		Base/Kernel

%description -n qc-usb
Documentation and test program to Logitech QuickCam USB.

%description -n qc-usb -l pl.UTF-8
Dokumentacja i program testujący do kamer Logitech QuickCam USB.

%prep
%setup -q -n qc-usb-%{version}

%build
%if %{with kernel}
%if %{with dist_kernel} && %{with smp}
%{__make} all \
		CC="%{kgcc}" \
		INCLUDES="%{rpmcflags} -I. -D__KERNEL_SMP=1 -D__SMP__ -I%{_kernelsrcdir}/include"
mv -f quickcam.ko  quickcam-smp.ko
#%%{__make} clean
%endif
%{__make} all \
		CC="%{kgcc}" \
		INCLUDES="%{rpmcflags} -I.  -I%{_kernelsrcdir}/include"
%endif

%if %{with userspace}
%{__make} -C testquickcam
# TODO: %{__cc}, %{rpmcflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%if %{with dist_kernel} && %{with smp}
install -D quickcam-smp.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video/quickcam.ko
%endif
install -D quickcam.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video/quickcam.ko
%endif

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

%post	-n kernel-smp-video-qc-usb
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-video-qc-usb
%depmod %{_kernel_ver}smp

%if %{with kernel}
%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/video/*

%if %{with dist_kernel} && %{with smp}
%files -n kernel-smp-video-qc-usb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/video/*
%endif
%endif

%if %{with userspace}
%files -n qc-usb
%defattr(644,root,root,755)
%doc README
%attr(755,root,users) %{_sbindir}/testquickcam
%endif
