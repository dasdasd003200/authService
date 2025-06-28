
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.virtualenv
  ];

  shellHook = ''
    source venv/bin/activate
    uvicorn config.asgi:application --reload --port 8000
  '';
}
