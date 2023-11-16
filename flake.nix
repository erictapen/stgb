{
  description = "Strafgesetzbuch viewer";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.gesetze.url = "github:bundestag/gesetze";
  inputs.gesetze.flake = false;

  outputs = { self, nixpkgs, gesetze }: 
  let
    pkgs = import nixpkgs { system = "x86_64-linux"; };
  in {

    packages.x86_64-linux.stgb = pkgs.callPackage ./. {
      inherit gesetze;
      inherit (self.packages.x86_64-linux) generate-icons;
    };

    packages.x86_64-linux.generate-icons = import ./icons.nix pkgs;

    packages.x86_64-linux.default = self.packages.x86_64-linux.stgb;

  };
}
