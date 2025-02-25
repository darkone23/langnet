import unittest
import time
import textwrap

from pathlib import Path

import cltk.data.fetch as cltk_fetch
import cltk.lexicon.lat as cltk_latlex
import cltk.alphabet.lat as cltk_latchars
import cltk.phonology.lat.transcription as cltk_latscript
import cltk.lemmatize.lat as cltk_latlem

import pycdsl


class ClassicsWiring:

    def __init__(self):
        self.start = time.monotonic()
        print("Setting up classics wiring...")

        self.lat_corpus = cltk_fetch.FetchCorpus("lat")

        self.required_models = [
            "lat_models_cltk",
        ]
        for model in self.required_models:
            model_dir = Path.home() / Path("cltk_data/lat/model") / model
            if not model_dir.exists():
                self.lat_corpus.import_corpus("lat_models_cltk")

        # print(self.lat_corpus.all_corpora_for_lang)

        self.CDSL = pycdsl.CDSLCorpus()
        self.CDSL.setup()

        self.latdict = cltk_latlex.LatinLewisLexicon()
        self.replacer = cltk_latchars.JVReplacer()
        self.xr = cltk_latscript.Transcriber("Classical", "Allen")
        self.lemmatizer = cltk_latlem.LatinBackoffLemmatizer()
        print(f"Startup time took {time.monotonic() - self.start}s")


wiring = (
    ClassicsWiring()
)  # this will prompt downloading language data from universities


class TestLatinExamples(unittest.TestCase):

    # import basic latin corpus

    def test_replacer(self):
        replaced = wiring.replacer.replace("justiciar")
        self.assertEqual(replaced, "iusticiar")

    def test_transcriber(self):
        transcribed = wiring.xr.transcribe("iusticiar")
        self.assertEqual(transcribed, "[jʊs.'t̪ɪ.kɪ̣.jar]")

    def test_lemmatizer(self):
        lupus = ["lupi", "luporum", "lupis", "lupos", "lupi", "lupis"]
        lemmas = wiring.lemmatizer.lemmatize(lupus)

        expected = [
            ("lupi", "lupus"),
            ("luporum", "lupus1"),
            ("lupis", "lupus1"),
            ("lupos", "lupus1"),
            ("lupi", "lupus"),
            ("lupis", "lupus1"),
        ]
        self.assertEqual(lemmas, expected)

    def test_lexicon(self):
        result = wiring.latdict.lookup("saga")

        expected = """\
        sāga


         ae, 
        f

        sagus, prophetic; SAG-, 
        a wisewoman, fortune-teller, sooth-sayer, witch
        , H., O."""

        self.assertEqual(result, textwrap.dedent(expected))


class TestCologneDigitalSanskritLexicon(unittest.TestCase):

    def test_basic_dictionary(self):
        results = wiring.CDSL["MW"].search("राम")
        meaning = "राम mf(आ/)n. (prob. ‘causing rest’, and in most meanings fr. √ रम्) dark, dark-coloured, black (cf. रात्रि), AV.; TĀr. (रामः शकुनिः. a black bird, crow, KāṭhGṛ.; Viṣṇ.)"
        self.assertEqual(results[0].meaning(), meaning)


if __name__ == "__main__":
    unittest.main()
