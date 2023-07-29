{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.buildPackages; [
      python310
      python310Packages.pip
      python310Packages.poetry
      python310Packages.black
    ];
    shellHook = ''
      [ -d .venv ] || python3 -m venv .venv
      source .venv/bin/activate
    '';
}
