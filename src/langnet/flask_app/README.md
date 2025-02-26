python api is a [flask server](https://flask-docs.readthedocs.io/en/latest/)

- uses the [app factory pattern](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) for wiring
- uses the [blueprint pattern](https://flask.palletsprojects.com/en/stable/blueprints/) for route management
- uses the [config object pattern](https://flask.palletsprojects.com/en/stable/config/#configuration-best-practices) for configuration
- served as a [wsgi app](https://flask.palletsprojects.com/en/stable/deploying/gunicorn) via [gunicorn](https://docs.gunicorn.org/en/stable/)
- frontend via [svelte single page app](../../../src-web/README.md)