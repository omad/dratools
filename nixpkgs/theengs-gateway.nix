{ pkgs ? import <nixpkgs> {}
}:

with pkgs; 
python3Packages.buildPythonPackage rec {
  pname = "TheengsGateway";
  version = "0.2.0";
  format = "pyproject";

  src = python3Packages.fetchPypi {
    inherit pname version;
    sha256 = "sha256-TjQzlXweLL5N0effNUpayxRhVlKoFDw1R5RIb2vuVpI=";
  };
  preBuild = ''
    echo ####### PRE BUILD DAMIEN ######
    ls -l
    ls -l TheengsDecoder
    ls -l TheengsDecoder/python/
    ls -l TheengsDecoder/python/TheengsDecoder/
  '';
#  src = fetchFromGitHub {
#    owner = "theengs";
#    repo = "gateway";
#    rev = "v${version}";
#    sha256 = "sha256-mbNZ21hclVqPPqJG6B1HvI8M5Sq5zMVVSx4T6OJaHds=";
#    fetchSubmodules = true;
#  };
  nativeBuildInputs = [ 
    cmake 
    ninja
    python3Packages.scikit-build];

  # setup.py will always (re-)execute cmake in buildPhase
  dontConfigure = true;
  propagatedBuildInputs = [ 
    python3Packages.paho-mqtt
    python3Packages.bleak
  ];
}
