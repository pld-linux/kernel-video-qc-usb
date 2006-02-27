#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
Summary:	Kernel module for Logitech QuickCam USB cameras (new)
Summary(pl):	Modu³ j±dra do kamer USB Logitech QuickCam (nowy)
Name:		kernel-video-qc-usb
Version:	0.6.3
%define	_rel	1
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/qce-ga/qc-usb-%{version}.tar.gz
# Source0-md5:	3d33380a29a7f92c4eef1f82d61b4ee0
URL:		http://qce-ga.sourceforge.net/
%{!?_without_dist_kernel:BuildRequires:	kernel-headers >= 2.2.0 }
BuildRequires:	rpmbuild(macros) >= 1.118
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires(post,postun):	modutils >= 2.3.18-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Logitech QuickCam USB cameras driver (a new one).

%description -l pl
Sterownik do kamer USB Logitech QuickCam (nowy).

%package -n kernel-smp-video-qc-usb
Summary:	SMP kernel module for Logitech QuickCam USB cameras
Summary(pl):	Modu³ j±dra SMP do kamer USB Logitech QuickCam
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires(post,postun):	modutils >= 2.3.18-2

%description -n kernel-smp-video-qc-usb
Logitech QuickCam USB cameras driver for SMP kernel (a new one).

%description -n kernel-smp-video-qc-usb -l pl
Sterownik do kamer USB Logitech QuickCam dla j±dra SMP (nowy).

%package -n qc-usb
Summary:	Documentation and test program to Logitech QuickCam USB
Summary(pl):	Dokumentacja i program testuj±cy do kamer Logitech QuickCam USB
Release:	%{_rel}
Group:		Base/Kernel
Requires:	%{name} = %{version}

%description -n qc-usb
Documentation and test program to Logitech QuickCam USB.

%description -n qc-usb -l pl
Dokumentacja i program testuj±cy do kamer Logitech QuickCam USB.

%prep
%setup -q -n qc-usb-%{version}

%build
%{__make} all \
        CC=%{kgcc} \
        INCLUDES="%{rpmcflags} -I. -D__KERNEL_SMP=1 -D__SMP__ -I%{_kernelsrcdir}/include"
mv -f quickcam.ko  quickcam-smp.ko
#%%{__make} clean
%{__make} all \
        CC=%{kgcc} \
        INCLUDES="%{rpmcflags} -I.  -I%{_kernelsrcdir}/include"

cd testquickcam
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -D quickcam-smp.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/video/quickcam.ko
install -D quickcam.ko $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/video/quickcam.ko

install -d $RPM_BUILD_ROOT%{_sbindir}
install testquickcam/testquickcam $RPM_BUILD_ROOT%{_sbindir}

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

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/video/*

%files -n kernel-smp-video-qc-usb
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/video/*

%files -n qc-usb
%defattr(644,root,root,755)
%doc README
%attr(755,root,users) %{_sbindir}/testquickcam
