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
    (pkgs.poetry.override { python3 = pkgs.python311; })
    pkgs.zlib
    pkgs.gcc
    pkgs.gnumake
    pkgs.python3Packages.python-lsp-server
    pkgs.black
    pkgs.pipx
  ];

  # https://devenv.sh/languages/
  # languages.rust.enable = true;
  languages.python.enable = true;
  languages.python.package = pkgs.python311;
  # languages.poetry.enable = true;

  # https://devenv.sh/processes/
  # processes.cargo-watch.exec = "cargo-watch";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  scripts.hello.exec = ''
    echo hello from $greet
  '';

  scripts.run-test-suite.exec = ''
    # echo $PATH
    $HOME/.local/bin/poe test
  '';

  enterShell = ''
    hello
    git --version
  '';

  # https://devenv.sh/tasks/
  tasks = {
    "playground:setup".exec = "pipx install nose2 poethepoet && ${pkgs.poetry}/bin/poetry install --with test"; 
    "devenv:enterShell".after = [ "playground:setup" ];
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
