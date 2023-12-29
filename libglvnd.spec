#
# Conditional build:
%bcond_without	default_gl	# build dispatcher as default libGL/libGLX/libGLESv1_CM/libGLESv2 provider
#
Summary:	Vendor-neutral OpenGL dispatch library
Summary(pl.UTF-8):	Niezależna od producenta biblioteka przekazująca wywołania OpenGL
Name:		libglvnd
Version:	1.7.0
Release:	1
License:	MIT-like
Group:		Libraries
Source0:	https://gitlab.freedesktop.org/glvnd/libglvnd/uploads/c24806c283070dc70700234ca8ffacf8/%{name}-%{version}.tar.gz
# Source0-md5:	5cd61ff16ec9732f3bdf5eb46dc93699
URL:		https://gitlab.freedesktop.org/glvnd/libglvnd
BuildRequires:	meson >= 0.48
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-proto-glproto-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{with default_gl}
%define		gl_incdir	%{_includedir}
%define		gl_libdir	%{_libdir}
%define		gl_pcdir	%{_pkgconfigdir}
%define		solink		%ghost
%else
%define		gl_incdir	%{_includedir}/%{name}
%define		gl_libdir	%{_libdir}/%{name}
%define		gl_pcdir	%{_libdir}/%{name}/pkgconfig
%define		solink		%{nil}
%define		noautoprov_files	%{_libdir}/%{name}
%endif
# _glapi_tls_Current symbol
%define		skip_post_check_so	libOpenGL.so.* libGL.so.* libGLESv1_CM.so.* libGLESv2.so.*

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

%package khrplatform-devel
Summary:	Khronos platform header file
Summary(pl.UTF-8):	Plik nagłówkowy platformy Khronos
Group:		Development/Libraries
%if %{with default_gl}
Provides:	khrplatform-devel
Obsoletes:	Mesa-khrplatform-devel < 21.3.1-2
%endif

%description khrplatform-devel
Khronos platform header file.

%description khrplatform-devel -l pl.UTF-8
Plik nagłówkowy platformy Khronos.

%package libEGL
Summary:	EGL interface glvnd libraries
Summary(pl.UTF-8):	Biblioteki glvnd interfejsu EGL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glvnd(EGL)%{?_isa}

%description libEGL
EGL interface glvnd libraries.

%description libEGL -l pl.UTF-8
Biblioteki glvnd interfejsu EGL.

%package libEGL-devel
Summary:	Development files for glvnd EGL interface
Summary(pl.UTF-8):	Pliki programistyczne glvnd interfejsu EGL
Group:		Development/Libraries
Requires:	%{name}-libEGL = %{version}-%{release}
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
%{?with_default_gl:Provides:	EGL-devel = 1.5}

%description libEGL-devel
Development files for glvnd EGL interface.

%description libEGL-devel -l pl.UTF-8
Pliki programistyczne glvnd interfejsu EGL.

%package libGL
Summary:	OpenGL 4.x interface glvnd libraries
Summary(pl.UTF-8):	Biblioteki glvnd interfejsu OpenGL 4.x
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_default_gl:Conflicts:	Mesa-libGL < 21.3.1-2}
Requires:	glvnd(GL)%{?_isa}

%description libGL
OpenGL 4.x interface glvnd libraries.

%description libGL -l pl.UTF-8
Biblioteki glvnd interfejsu OpenGL 4.x.

%package libGL-devel
Summary:	Development files for glvnd OpenGL 4.x interface
Summary(pl.UTF-8):	Pliki programistyczne glvnd interfejsu OpenGL 4.x
Group:		Development/Libraries
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
Requires:	%{name}-libGL = %{version}-%{release}
%if %{with default_gl}
Provides:	OpenGL-devel = 4.6
Provides:	OpenGL-GLX-devel = 1.4
%endif

%description libGL-devel
Development files for glvnd OpenGL 4.x interface.

%description libGL-devel -l pl.UTF-8
Pliki programistyczne glvnd interfejsu OpenGL 4.x.

%package libGLES
Summary:	OpenGL ES 1, 2, 3 interface glvnd libraries
Summary(pl.UTF-8):	Biblioteki glvnd interfejsów OpenGL ES 1, 2, 3
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glvnd(GLES)%{?_isa}
%if %{with default_gl}
Obsoletes:	Mesa-libGLES < 21.3.1-2
%endif

%description libGLES
OpenGL ES 1, 2, 3 interface glvnd libraries.

%description libGLES -l pl.UTF-8
Biblioteki glvnd interfejsów OpenGL ES 1, 2, 3.

%package libGLES-devel
Summary:	Development files for glvnd OpenGL ES 1, 2, 3 interfaces
Summary(pl.UTF-8):	Pliki programistyczne glvnd interfejsów OpenGL ES 1, 2, 3
Group:		Development/Libraries
Requires:	%{name}-khrplatform-devel = %{version}-%{release}
Requires:	%{name}-libGLES = %{version}-%{release}
%if %{with default_gl}
Provides:	OpenGLES-devel = 3.2
Provides:	OpenGLESv1-devel = 1.1
Provides:	OpenGLESv2-devel = 2.0
Provides:	OpenGLESv3-devel = 3.2
Obsoletes:	Mesa-libGLES-devel < 21.3.1-2
%endif

%description libGLES-devel
Development files for glvnd OpenGL ES 1, 2, 3 interfaces.

%description libGLES-devel -l pl.UTF-8
Pliki programistyczne glvnd interfejsów OpenGL ES 1, 2, 3.

%prep
%setup -q

%build
%meson build
%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{without default_gl}
install -d $RPM_BUILD_ROOT{%{gl_libdir},%{gl_incdir},%{gl_pcdir}}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/lib{EGL,GL,GLESv1_CM,GLESv2}.* $RPM_BUILD_ROOT%{gl_libdir}
%{__mv} $RPM_BUILD_ROOT%{_includedir}/{EGL,GL,GLES,GLES2,GLES3,KHR} $RPM_BUILD_ROOT%{gl_incdir}
%{__mv} $RPM_BUILD_ROOT%{_pkgconfigdir}/{egl,gl,glesv1_cm,glesv2}.pc $RPM_BUILD_ROOT%{gl_pcdir}
%endif

install -d $RPM_BUILD_ROOT%{_datadir}/glvnd/egl_vendor.d

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%if %{with default_gl}
%post	libEGL -p /sbin/ldconfig
%postun	libEGL -p /sbin/ldconfig

%post	libGL -p /sbin/ldconfig
%postun	libGL -p /sbin/ldconfig

%post	libGLES -p /sbin/ldconfig
%postun	libGLES -p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libGLdispatch.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLdispatch.so.0
%if %{without default_gl}
%dir %{gl_libdir}
%endif
%dir %{_datadir}/glvnd

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLdispatch.so
%{_includedir}/glvnd
%{_pkgconfigdir}/libglvnd.pc

%files khrplatform-devel
%defattr(644,root,root,755)
%if %{without default_gl}
%dir %{gl_incdir}
%dir %{gl_pcdir}
%endif
%{gl_incdir}/KHR

%files libEGL
%defattr(644,root,root,755)
%attr(755,root,root) %{gl_libdir}/libEGL.so.*.*.*
%attr(755,root,root) %solink %{gl_libdir}/libEGL.so.1
%dir %{_datadir}/glvnd/egl_vendor.d

%files libEGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{gl_libdir}/libEGL.so
%{gl_incdir}/EGL
%{gl_pcdir}/egl.pc

%files libGL
%defattr(644,root,root,755)
%attr(755,root,root) %{gl_libdir}/libGL.so.*.*.*
%attr(755,root,root) %solink %{gl_libdir}/libGL.so.1
%attr(755,root,root) %{gl_libdir}/libGL.so

%attr(755,root,root) %{_libdir}/libGLX.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLX.so.0

%attr(755,root,root) %{_libdir}/libOpenGL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libOpenGL.so.0

%files libGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLX.so
%attr(755,root,root) %{_libdir}/libOpenGL.so
%{gl_incdir}/GL
%{gl_pcdir}/gl.pc
%{_pkgconfigdir}/glx.pc
%{_pkgconfigdir}/opengl.pc

%files libGLES
%defattr(644,root,root,755)
%attr(755,root,root) %{gl_libdir}/libGLESv1_CM.so.*.*.*
%attr(755,root,root) %solink %{gl_libdir}/libGLESv1_CM.so.1
%attr(755,root,root) %{gl_libdir}/libGLESv2.so.*.*.*
%attr(755,root,root) %solink %{gl_libdir}/libGLESv2.so.2

%files libGLES-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{gl_libdir}/libGLESv1_CM.so
%attr(755,root,root) %{gl_libdir}/libGLESv2.so
%{gl_incdir}/GLES
%{gl_incdir}/GLES2
%{gl_incdir}/GLES3
%{gl_pcdir}/glesv1_cm.pc
%{gl_pcdir}/glesv2.pc
