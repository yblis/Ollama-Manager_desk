{pkgs}: {
  deps = [
    pkgs.freetype
    pkgs.fontconfig
    pkgs.libxkbcommon
    pkgs.libGL
    pkgs.xvfb-run
  ];
}
