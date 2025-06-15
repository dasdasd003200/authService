
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.python312Packages.virtualenv
  ];

  shellHook = ''
    if [ ! -d "venv" ]; then
      python -m venv venv
    fi
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel

    # Instala los paquetes del requirements si no están
    if [ -f requirements.txt ]; then
      pip install -r requirements.txt
    fi

    echo "Entorno activado. Puedes usar Django ahora 🚀"
  '';
}
