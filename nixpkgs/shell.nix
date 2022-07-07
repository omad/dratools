with import <nixpkgs> {};

( let
    TheengsGateway = callPackage ./theengs-gateway.nix {
#      buildPythonPackage = python39Packages.buildPythonPackage;
    };
  in python39.withPackages (ps: [ TheengsGateway ])
).env
