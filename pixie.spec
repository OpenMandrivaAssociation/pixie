%define	oname Pixie
%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	3D renderer Renderman compliant
Name:		pixie
Version:	2.2.1
Release:	%mkrel 1
License:	LGPL
Group:		Graphics
Source0:	http://downloads.sourceforge.net/pixie/%{oname}-src-%{version}.tgz
Url:		http://www.cs.utexas.edu/~okan/Pixie/pixie.htm
BuildRequires:	libfltk-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	libtiff-devel
BuildRequires:	mesa-common-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Pixie is a RenderMan like photorealistic renderer.
It is being developed in the hope that it will be
useful for graphics research and for people who
can not afford a commercial renderer.

%package -n %{libname}
Summary:	Shared libraries for Pixie
Group:		System/Libraries

%description -n %{libname}
Shared libraries for Pixie, a RenderMan 
compiliant renderer.

%package -n %{develname}
Summary:	Pixie development environment
Group:		Development/C++
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{develname}
Pixie header files.

%prep
%setup -qn %{oname}

%build
%configure2_5x \
	--enable-openexr-threads \
	--with-shaderdir=%{_datadir}/Pixie/shaders \
	--with-modeldir=%{_datadir}/Pixie/models \
	--with-texturesdir=%{_datadir}/Pixie/textures \
	--with-displaysdir=%{_libdir}/Pixie/displays \
	--with-modulesdir=%{_libdir}/Pixie/modules

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std docdir=%{_docdir}/%{oname}

mkdir -p %{buildroot}%{_datadir}/Pixie/textures
cp -f textures/*.tif %{buildroot}%{_datadir}/Pixie/textures

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_datadir}/doc/%{oname}/*
%dir %{_libdir}/%{oname}
%dir %{_libdir}/%{oname}/displays
%dir %{_libdir}/%{oname}/modules
%dir %{_datadir}/%{oname}/shaders
%dir %{_datadir}/%{oname}/textures
#%dir %{_datadir}/%{oname}/procedurals
%{_bindir}/*
%{_libdir}/%{oname}/displays/*.la
%{_libdir}/%{oname}/displays/*.so
%{_libdir}/%{oname}/modules/*.la
%{_libdir}/%{oname}/modules/*.so
%{_datadir}/%{oname}/shaders/*.sdr
%{_datadir}/%{oname}/shaders/*.sl
%{_datadir}/Pixie/textures/*.tif
%{_mandir}/man1/*.1.*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*h
%{_libdir}/*.la
%{_libdir}/*.so
