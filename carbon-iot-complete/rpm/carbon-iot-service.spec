Name:           carbon-iot-service
Version:        1.0
Release:        1%{?dist}
Summary:        Carbon IoT microservice

License:        MIT
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
A FastAPI-based IoT service packaged as an RPM.

%prep

%build

%install
mkdir -p %{buildroot}/opt/carbon-iot-service
cp -r device-service %{buildroot}/opt/carbon-iot-service/

%files
/opt/carbon-iot-service

%post
echo "carbon-iot-service installed"
