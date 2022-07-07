{ lib, buildPythonPackage, cmake, ninja, python39Packages } :

buildPythonPackage rec {
  pname = "TheengsGateway";
  version = "0.2.0";
  format = "pyproject";

  src = python39Packages.fetchPypi {
    inherit pname version;
    sha256 = "sha256-TjQzlXweLL5N0effNUpayxRhVlKoFDw1R5RIb2vuVpI=";
  };

  nativeBuildInputs = [ 
    cmake 
    ninja
    python39Packages.scikit-build
  ];

  # setup.py will always (re-)execute cmake in buildPhase
  dontConfigure = true;

  propagatedBuildInputs = with python39Packages; [
    paho-mqtt
    bleak
  ];

  meta = with lib; {
    homepage = "https://github.com/theengs/gateway";
    description = "BLE to MQTT Gateway";
    license = licenses.gpl3;
  };
}
