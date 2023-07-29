{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.buildPackages; [
      python37
      python37.pip
      python37.six
    ];
    shellHook = ''
      [ -d .venv ] || python3 -m venv .venv
      source .venv/bin/activate
    '';
}
