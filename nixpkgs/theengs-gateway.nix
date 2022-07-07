{ lib, pythonPackages, cmake, ninja } :

with pythonPackages;
buildPythonPackage rec {
  pname = "TheengsGateway";
  version = "0.2.0";
  format = "pyproject";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-TjQzlXweLL5N0effNUpayxRhVlKoFDw1R5RIb2vuVpI=";
  };

  nativeBuildInputs = [ 
    cmake 
    ninja
    scikit-build
  ];

  # setup.py will always (re-)execute cmake in buildPhase
  dontConfigure = true;

  propagatedBuildInputs = [
    paho-mqtt
    bleak
  ];

  meta = with lib; {
    homepage = "https://github.com/theengs/gateway";
    description = "BLE to MQTT Gateway";
    license = licenses.gpl3;
  };
}
