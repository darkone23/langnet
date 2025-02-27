from pathlib import Path

import cltk.data.fetch as cltk_fetch
import cltk.lexicon.lat as cltk_latlex
import cltk.alphabet.lat as cltk_latchars
import cltk.phonology.lat.transcription as cltk_latscript
import cltk.lemmatize.lat as cltk_latlem

from cltk.languages.utils import get_lang, Language


class ClassicsToolkit:

    # https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes

    LATIN: Language = get_lang("lat")
    GREEK: Language = get_lang("grc")
    SANSKRIT: Language = get_lang("san")

    def __init__(self):

        self.lat_corpus = cltk_fetch.FetchCorpus(self.LATIN.iso_639_3_code)

        self.required_models = [
            "lat_models_cltk",
        ]
        for model in self.required_models:
            model_dir = Path.home() / Path("cltk_data/lat/model") / model
            if not model_dir.exists():
                self.lat_corpus.import_corpus("lat_models_cltk")

        self.latdict = cltk_latlex.LatinLewisLexicon()
        self.jvsub = cltk_latchars.JVReplacer()
        self.latxform = cltk_latscript.Transcriber("Classical", "Allen")
        self.latlemma = cltk_latlem.LatinBackoffLemmatizer()
