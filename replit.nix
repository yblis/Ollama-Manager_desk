{pkgs}: {
  deps = [
    pkgs.fontconfig
    pkgs.libxkbcommon
    pkgs.libGL
    pkgs.xvfb-run
  ];
}
