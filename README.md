# langnet

This project provides some software for working with languages.

It relies heavily on the perl engine at [d.iogen.es](https://d.iogen.es/web/)

- https://github.com/pjheslin/diogenes

Today this project parses diogenes query results back into structured data.

Because of this design it requires a diogenes server running locally.

## Running the software

if you have [devenv.sh](https://devenv.sh):

```sh
devenv shell
poetry install
poe dev
```

now you can query for some latin terms:

```sh
# assuming you have diogenes available at localhost:8888
curl 'localhost:5000/api/q?l=lat&s=benevolens' | jq .chunks[1].definitions

# compare with diogenes output:
#   http://localhost:8888/Perseus.cgi?do=parse&lang=lat&q=benevolens
```

or greek terms:

```sh
# notice treatment of utf-8 query parameters
curl --data-urlencode 's=οὐσία' --data-urlencode 'l=grk' --get 'http://localhost:5000/api/q' | jq .chunks[0].morphology.morphs
```

## other projects:

- lute-v3 / lwt
- lingq
- scaife/perseus
- wisdomlib
- archive.org

