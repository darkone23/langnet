# langnet

This project provides software for working with languages.

It requires some dependencies:

1. [d.iogen.es](https://d.iogen.es/web/) server running at `http://localhost:8888`
2. [whitakers words](https://latin-words.com) installed at `~/.local/bin/whitakers-words`
3. [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) installed at `~/cdsl_data/`
4. [CLTK](https://docs.cltk.org/en/latest/about.html) classical language models at `~/cltk_data/`

The included test suite will automate the installation of the CLTK and CDSL data but diogenes and whitakers must be installed manually.

## Running the software

if you have [devenv.sh](https://devenv.sh):

```sh
devenv shell
poe test # this triggers downloading and ToS approval!
poe dev
```

now you can query for some latin terms:

```sh
# assuming you have diogenes available at localhost:8888
curl 'localhost:5000/api/q?l=lat&s=benevolens' | jq .

# compare with diogenes output:
#   http://localhost:8888/Perseus.cgi?do=parse&lang=lat&q=benevolens
```

or greek terms:

```sh
# notice treatment of utf-8 query parameters
curl --data-urlencode 's=οὐσία' --data-urlencode 'l=grk' --get 'http://localhost:5000/api/q' | jq .
```

## other projects:

- lute-v3 / lwt
- lingq
- scaife/perseus
- wisdomlib
- archive.org

