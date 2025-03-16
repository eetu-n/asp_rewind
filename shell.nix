let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/5d7db4668d7a0c6cc5fc8cf6ef33b008b2b1ed8b.tar.gz") {};
in pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages (python-pkgs: with python-pkgs; [
      # select Python packages here
      numpy
      scipy
      matplotlib
      pygobject3
      ipython
      tkinter
      pip
      pyaudio
      pysoundfile
      resampy
    ]))
    gobject-introspection
    gtk3
  ];
}
