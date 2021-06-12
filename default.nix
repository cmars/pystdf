{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.buildPackages; [
      python38
      python38Packages.pip
      python38Packages.six
      python38Packages.wxPython_4_1
    ];
    shellHook = ''
      [ -d .venv ] || python3 -m venv .venv
      source .venv/bin/activate
    '';
}
