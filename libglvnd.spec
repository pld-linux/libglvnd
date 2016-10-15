# TODO:
# - what should provide GL headers when %{with default_gl}? packages with khronos headers alone?
#
# Conditional build:
%bcond_with	default_gl	# build dispatcher as default libGL/libGLX/libGLESv1_CM/libGLESv2 provider
#
Summary:	Vendor-neutral OpenGL dispatch library
Summary(pl.UTF-8):	Niezależna od producenta biblioteka przekazująca wywołania OpenGL
Name:		libglvnd
Version:	0.1.1
Release:	1
License:	MIT-like
Group:		Libraries
#Source0Download: https://github.com/NVIDIA/libglvnd/releases
Source0:	https://github.com/NVIDIA/libglvnd/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	564820301daf6b4c7d80cbfbc04efc8c
URL:		https://github.com/NVIDIA/libglvnd
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	libtool
BuildRequires:	python >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with default_gl}
%define		gl_libdir	%{_libdir}
%else
%define		gl_libdir	%{_libdir}/%{name}
%define		noautoprov_files	%{_libdir}/%{name}
%endif

%description
This is a work-in-progress implementation of the vendor-neutral
dispatch layer for arbitrating OpenGL API calls between multiple
vendors on a per-screen basis, as described by Andy Ritger's OpenGL
ABI proposal:
<https://github.com/aritger/linux-opengl-abi-proposal/blob/master/linux-opengl-abi-proposal.txt>.

Currently, only the GLX window-system API and OpenGL are supported,
but in the future this library may support EGL and OpenGL ES as well.

%description -l pl.UTF-8
Ten pakiet to (będąca w trakcie tworzenia) implementacja warstwy
przekazującej wywołania dowolnych wywołań API OpenGL między różnymi
producentami w zależności od ekranu, zgodnie z propozycją opisaną
przez Andy Ritgera:
<https://github.com/aritger/linux-opengl-abi-proposal/blob/master/linux-opengl-abi-proposal.txt>.

Obecnie obsługiwane jest tylko API systemu okienek GLX oraz OpenGL, w
przyszłości biblioteka może obsługiwać także EGL i OpenGL ES.

%package devel
Summary:	Header files for libglvnd interface
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu libglvnd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
# <GL/gl.h>
Requires:	OpenGL-devel
# <GL/glx.h>
Requires:	OpenGL-GLX-devel

%description devel
Header files for libglvnd interface.

%description devel -l pl.UTF-8
Pliki nagłówkowe interfejsu libglvnd.

%package libGL
Summary:	OpenGL 4.x interface glvnd libraries
Summary(pl.UTF-8):	Biblioteki glvnd interfejsu OpenGL 4.x
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description libGL
OpenGL 4.x interface glvnd libraries.

%description libGL -l pl.UTF-8
Biblioteki glvnd interfejsu OpenGL 4.x.

%package libGL-devel
Summary:	Development files for glvnd OpenGL 4.x interface
Summary(pl.UTF-8):	Pliki programistyczne glvnd interfejsu OpenGL 4.x
Group:		Development/Libraries
Requires:	%{name}-libGL = %{version}-%{release}
#Requires:	khronos-OpenGL-headers(?)
#%{?with_default_gl:Provides:	OpenGL-devel = 4.?}

%description libGL-devel
Development files for glvnd OpenGL 4.x interface.

%description libGL-devel -l pl.UTF-8
Pliki programistyczne glvnd interfejsu OpenGL 4.x.

%package libGLES
Summary:	OpenGL ES 1, 2, 3 interface glvnd libraries
Summary(pl.UTF-8):	Biblioteki glvnd interfejsów OpenGL ES 1, 2, 3
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description libGLES
OpenGL ES 1, 2, 3 interface glvnd libraries.

%description libGLES -l pl.UTF-8
Biblioteki glvnd interfejsów OpenGL ES 1, 2, 3.

%package libGLES-devel
Summary:	Development files for glvnd OpenGL ES 1, 2, 3 interfaces
Summary(pl.UTF-8):	Pliki programistyczne glvnd interfejsów OpenGL ES 1, 2, 3
Group:		Development/Libraries
Requires:	%{name}-libGLES = %{version}-%{release}
#Requires:	khronos-OpenGLES-headers(?)
%if 0 && %{with default_gl}
Provides:	OpenGLES-devel
Provides:	OpenGLESv1-devel = 1.?
Provides:	OpenGLESv2-devel = 2.?
Provides:	OpenGLESv3-devel = 3.?
%endif

%description libGLES-devel
Development files for glvnd OpenGL ES 1, 2, 3 interfaces.

%description libGLES-devel -l pl.UTF-8
Pliki programistyczne glvnd interfejsów OpenGL ES 1, 2, 3.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if %{without default_gl}
install -d $RPM_BUILD_ROOT%{gl_libdir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/lib{GL,GLESv1_CM,GLESv2}.* $RPM_BUILD_ROOT%{gl_libdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	libGL -p /sbin/ldconfig
%postun	libGL -p /sbin/ldconfig

%post	libGLES -p /sbin/ldconfig
%postun	libGLES -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libGLdispatch.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLdispatch.so.0
%if %{without default_gl}
%dir %{_libdir}/%{name}
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLdispatch.so
%{_includedir}/glvnd
%{_pkgconfigdir}/libglvnd.pc

%files libGL
%defattr(644,root,root,755)
%if %{with default_gl}
%attr(755,root,root) %{_libdir}/libGL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGL.so.1
%attr(755,root,root) %{_libdir}/libGL.so
%else
%attr(755,root,root) %{gl_libdir}/libGL.so.*.*.*
%attr(755,root,root) %{gl_libdir}/libGL.so.1
%attr(755,root,root) %{gl_libdir}/libGL.so
%endif

%attr(755,root,root) %{_libdir}/libGLX.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLX.so.0

%attr(755,root,root) %{_libdir}/libOpenGL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenGL.so.0

%files libGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLX.so
%attr(755,root,root) %{_libdir}/libOpenGL.so

%files libGLES
%defattr(644,root,root,755)
%if %{with default_gl}
%attr(755,root,root) %{_libdir}/libGLESv1_CM.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLESv1_CM.so.1
%attr(755,root,root) %{_libdir}/libGLESv2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLESv2.so.2
%else
%attr(755,root,root) %{gl_libdir}/libGLESv1_CM.so.*.*.*
%attr(755,root,root) %{gl_libdir}/libGLESv1_CM.so.1
%attr(755,root,root) %{gl_libdir}/libGLESv2.so.*.*.*
%attr(755,root,root) %{gl_libdir}/libGLESv2.so.2
%endif

%files libGLES-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{gl_libdir}/libGLESv1_CM.so
%attr(755,root,root) %{gl_libdir}/libGLESv2.so
