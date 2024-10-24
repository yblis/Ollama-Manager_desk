{pkgs}: {
  deps = [
    pkgs.zstd
    pkgs.freetype
    pkgs.fontconfig
    pkgs.libxkbcommon
    pkgs.libGL
    pkgs.xvfb-run
  ];
}
