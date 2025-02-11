{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = [ 
    pkgs.git
    pkgs.black
    pkgs.poetry
    pkgs.pipx
    pkgs.nodejs
    pkgs.python3Packages.python-lsp-server
    pkgs.nodePackages.vscode-langservers-extracted
    pkgs.nil
  ];

  # https://devenv.sh/languages/
  # languages.rust.enable = true;
  languages.python.enable = true;
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

  # https://devenv.sh/tasks/
  tasks = {
    "langnet:setup".exec = "pipx install gunicorn poethepoet flask && ${pkgs.poetry}/bin/poetry install";
    "langnet:dev".exec = "devenv shell poe -- dev";
    "langnet:serve".exec = "devenv shell poe -- serve";
    "langnet:jssetup".exec = ''devenv shell npm -- install --prefix=frontend'';
    "langnet:jsdev".exec = ''devenv shell npm -- run dev --prefix=frontend'';
    "langnet:jsbuild".exec = ''
        devenv shell npm -- run build --prefix=frontend && cp -r frontend/dist/* webroot/
    '';
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
