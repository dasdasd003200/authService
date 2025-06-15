
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.virtualenv
  ];

  shellHook = ''
    source venv/bin/activate
    python manage.py runserver
  '';
}
