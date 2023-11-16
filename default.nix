{ lib
, stdenv
, pandoc
, python3
, gesetze
, vollkorn
}:

stdenv.mkDerivation {
  pname = "stgb";
  version = "0.0.1";

  src = ./.;

  nativeBuildInputs = [ pandoc python3 ];

  buildPhase = ''
    pandoc -t html ${gesetze}/s/stgb/index.md | python3 stgb.py
  '';

  installPhase = ''
    mkdir -p $out/fonts
    cp cover.html index.html index.js stgb.html stgb.json style.css $out/
    cp ${vollkorn}/share/fonts/truetype/* $out/fonts/
  '';
}
