{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  env.LD_LIBRARY_PATH= "${pkgs.stdenv.cc.cc.lib}/lib/:${pkgs.zlib}/lib";
  env.GREET = "devenv";
  env.TMP = "/tmp";
  env.TMPDIR = "/tmp";
  
  # https://devenv.sh/packages/
  packages = [ 
    pkgs.git
    pkgs.nodejs

    # useful language servers
    pkgs.python3Packages.python-lsp-server
    pkgs.nodePackages.vscode-langservers-extracted
    pkgs.nil

    # some python utilities
    # (pkgs.black.override { python3 = pkgs.python311; })  
    pkgs.black
    pkgs.pipx
    (pkgs.poetry.override { python3 = pkgs.python311; })  
    # (pkgs.pipx.override { python3 = pkgs.python311; })
 
    # some libraries for cltk deps (numpy, scipy)
    pkgs.zlib
    pkgs.gcc
    pkgs.gnumake
  ];

  # https://devenv.sh/languages/
  # languages.rust.enable = true;
  languages.python.enable = true;
  languages.python.package = pkgs.python311; # the version that currently works with CLTK

  languages.python.poetry.enable = true;
  languages.python.poetry.activate.enable = true;

  languages.javascript.enable = true;
  languages.javascript.npm.enable = true;
  languages.typescript.enable = true;

  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  scripts.hello.exec = ''
    echo hello from $GREET
  '';

  enterShell = ''
    hello
    git --version
  '';

  scripts.run-test-suite.exec = ''
    $HOME/.local/bin/poe test
  '';

  scripts.jsinstall.exec = ''
    npm install --prefix=$DEVENV_ROOT/src-web
  '';

  scripts.jsbuild.exec = ''
    npm run build --prefix=$DEVENV_ROOT/src-web && cp -r $DEVENV_ROOT/src-web/dist/* $DEVENV_ROOT/webroot/
  '';

  # https://devenv.sh/tasks/
  tasks = {
    "langnet:setup".exec = "pipx install gunicorn poethepoet flask nose2 && ${pkgs.poetry}/bin/poetry install";

    # http://localhost:5000
    "langnet:dev".exec = "devenv shell $HOME/.local/bin/poe -- dev";

    # http://localhost:8000
    "langnet:serve".exec = "devenv shell $HOME/.local/bin/poe -- serve";

    # http://localhost:5173
    "langnet:jsdev".exec = ''devenv shell npm -- run dev --prefix=$DEVENV_ROOT/src-web'';

    "devenv:enterShell".after = [ "langnet:setup" ];
  };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
  '';

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
