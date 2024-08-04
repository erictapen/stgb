{
  description = "Strafgesetzbuch viewer";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    gesetze.url = "github:bundestag/gesetze";
    gesetze.flake = false;
  };

  outputs = { self, nixpkgs, flake-utils, gesetze }:
    flake-utils.lib.eachSystem
      [ "x86_64-linux" "aarch64-linux" ]
      (system:
        let pkgs = nixpkgs.legacyPackages.${system}; in
        {


          packages = {
            default = self.packages.${system}.stgb;
            stgb = pkgs.callPackage ./. {
              inherit gesetze;
              inherit (self.packages.${system}) generate-icons;
            };

            generate-icons = import ./icons.nix pkgs;

          };

        });
}
