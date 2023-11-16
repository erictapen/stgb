{ lib
, stdenv
, pandoc
, python3
, gesetze
, vollkorn
, generate-icons
, imagemagick
}:

stdenv.mkDerivation {
  pname = "stgb";
  version = "0.0.1";

  src = ./.;

  nativeBuildInputs = [ pandoc python3 imagemagick ];

  buildPhase = ''
    pandoc -t html ${gesetze}/s/stgb/index.md | python3 stgb.py
  '';

  installPhase = ''
    mkdir -p $out/fonts
    mkdir -p $out/icons
    cp cover.html index.html index.js stgb.html stgb.json style.css $out/
    cp ${vollkorn}/share/fonts/truetype/* $out/fonts/
    ${generate-icons}/bin/generate-icons.sh favicon.svg $out/icons/
  '';
}
