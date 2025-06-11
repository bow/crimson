{
  description = "Nix flake for Crimson";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.flake-utils.follows = "flake-utils";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      poetry2nix,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlays.default ];
        };
        overrides = pkgs.poetry2nix.overrides.withDefaults (
          # Using wheel since mypy compilation is too long and it is only a dev/test dependency.
          _final: prev: { mypy = prev.mypy.override { preferWheel = true; }; }
        );
        projectDir = self;
        python = pkgs.python312; # NOTE: Keep in-sync with pyproject.toml.
        app = pkgs.poetry2nix.mkPoetryApplication { inherit overrides projectDir python; };
      in
      {
        apps = {
          default = {
            type = "app";
            program = "${app}/bin/${app.pname}";
          };
        };
        devShells =
          let
            devPackages = with pkgs; [
              # python-only
              (poetry.withPlugins (_ps: [ python.pkgs.poetry-dynamic-versioning ]))
              # nix-only
              deadnix
              nixfmt-rfc-style
              statix
              # others
              curl
              entr
              gnugrep
              pre-commit
              skopeo
            ];
            devNativeBuildInputs = [
              python
              python.pkgs.venvShellHook
              python.pkgs.tox
              pkgs.python311
            ];
            ciEnv = pkgs.poetry2nix.mkPoetryEnv { inherit overrides projectDir python; };
            ciEnvPy311 = pkgs.poetry2nix.mkPoetryEnv {
              inherit overrides projectDir;
              python = pkgs.python311;
            };
          in
          {
            ci = pkgs.mkShellNoCC { packages = devPackages ++ [ ciEnv ]; };
            ciPy311 = pkgs.mkShellNoCC { packages = devPackages ++ [ ciEnvPy311 ]; };
            default = pkgs.mkShellNoCC rec {
              nativeBuildInputs = devNativeBuildInputs;
              packages = devPackages;
              venvDir = "./.venv";
              postVenvCreation = ''
                unset SOURCE_DATE_EPOCH
                poetry env use ${venvDir}/bin/python
                poetry install
              '';
              postShellHook = ''
                unset SOURCE_DATE_EPOCH
              '';
            };
          };
        formatter = pkgs.nixfmt-rfc-style;
        packages =
          let
            readFileOr = (path: default: with builtins; if pathExists path then (readFile path) else default);
            imgTag = if app.version != "0.0.dev0" then app.version else "latest";
            imgAttrs = rec {
              name = "ghcr.io/bow/${app.pname}";
              tag = imgTag;
              contents = [ app ];
              config = {
                Entrypoint = [ "/bin/${app.pname}" ];
                Labels = {
                  "org.opencontainers.image.revision" = readFileOr "${self}/.rev" "";
                  "org.opencontainers.image.source" = "https://github.com/bow/${app.pname}";
                  "org.opencontainers.image.title" = "${app.pname}";
                  "org.opencontainers.image.url" = "https://${name}";
                };
              };
            };
          in
          {
            dockerArchive = pkgs.dockerTools.buildLayeredImage imgAttrs;
            dockerArchiveStreamer = pkgs.dockerTools.streamLayeredImage imgAttrs;
            local = app;
          };
      }
    );
}
