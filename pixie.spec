%define	oname Pixie
%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	3D renderer Renderman compliant
Name:		pixie
Version:	2.2.6
Release:3
License:	LGPLv2+
Group:		Graphics
Url:		http://www.renderpixie.com/
Source0:	http://downloads.sourceforge.net/pixie/%{oname}-src-%{version}.tgz
Patch0:	Pixie-src-2.2.6-zlib-fix.patch
BuildRequires:	fltk-devel
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	mesa-common-devel
BuildRequires:	flex
BuildRequires:	bison
Requires:	%{libname} = %{version}-%{release}


%description
Pixie is a RenderMan like photorealistic renderer.
It is being developed in the hope that it will be
useful for graphics research and for people who
can not afford a commercial renderer.

%package -n %{libname}
Summary:	Shared libraries for %{oname}
Group:		System/Libraries

%description -n %{libname}
Shared libraries for %{oname}, a RenderMan 
compiliant renderer.

%package -n %{develname}
Summary:	Development files for %{oname}
Group:		Development/C++
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname %{name} 0 -d} < 2.2.4

%description -n %{develname}
Development files and headers for %{oname}.

%prep
%setup -qn %{oname}
%patch0 -p0

# do not link against static libraries
sed -i.r_static -e 's|--ldstaticflags|--ldflags|' configure

%build
%define Werror_cflags %nil
%configure2_5x \
	--enable-openexr-threads \
	--disable-static-fltk \
	--disable-selfcontained \
	--with-shaderdir=%{_datadir}/Pixie/shaders \
	--with-modeldir=%{_datadir}/Pixie/models \
	--with-texturesdir=%{_datadir}/Pixie/textures \
	--with-displaysdir=%{_libdir}/Pixie/displays \
	--with-modulesdir=%{_libdir}/Pixie/modules

# do not hardcode rpath
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std docdir=%{_docdir}/%{oname}

find %{buildroot} -name '*.la' -exec rm -f {} ';'
mkdir -p %{buildroot}%{_datadir}/Pixie/textures
cp -f textures/*.tif %{buildroot}%{_datadir}/Pixie/textures


%files
%doc %{_datadir}/doc/%{oname}/*
%dir %{_libdir}/%{oname}
%dir %{_libdir}/%{oname}/displays
%dir %{_libdir}/%{oname}/modules
%dir %{_datadir}/%{oname}/shaders
%dir %{_datadir}/%{oname}/textures
%{_bindir}/*
%{_libdir}/%{oname}/displays/*.so
%{_libdir}/%{oname}/modules/*.so
%{_datadir}/%{oname}/shaders/*.sdr
%{_datadir}/%{oname}/shaders/*.sl
%{_datadir}/Pixie/textures/*.tif
%{_mandir}/man1/*.1.*

%files -n %{libname}
%doc DEVNOTES ChangeLog COMPILING.txt COPYING
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc DEVNOTES ChangeLog COMPILING.txt COPYING
%{_includedir}/*h
%{_libdir}/*.so


