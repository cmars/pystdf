{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python311;
in
pkgs.mkShell {
  packages = [
    pkgs.uv
    python
  ];

  shellHook = ''
    # Use the Nix-managed interpreter for the uv-managed venv.
    export UV_PYTHON="${python}/bin/python3.11"
    # Create the environment and install the project + dev deps from uv.lock.
    uv venv --python python3.11 .venv
    uv sync
  '';
}
