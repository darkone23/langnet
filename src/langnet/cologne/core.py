import pycdsl
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate


class SanskritCologneLexicon:
    def __init__(self):
        self.CDSL: pycdsl.CDSLCorpus = pycdsl.CDSLCorpus()
        self.CDSL.setup()

        # Sanskrit-English
        self.mw: pycdsl.CDSLDict = self.CDSL["MW"]
        self.ap90: pycdsl.CDSLDict = self.CDSL["AP90"]

        # English-Sanskrit
        self.mwe: pycdsl.CDSLDict = self.CDSL["MWE"]
        self.ae: pycdsl.CDSLDict = self.CDSL["AE"]

    def transliterate(self, data):
        return transliterate(data, sanscript.ITRANS, sanscript.DEVANAGARI)

    def serialize_results(self, results: list[pycdsl.lexicon.Entry]):
        return [
            dict(
                id=result.id,
                term=result.key,
                meaning=result.meaning(),
            )
            for result in results
        ]

    def lookup_ascii(self, data):
        devengari = self.transliterate(data)
        return dict(
            mw=self.serialize_results(self.mw.search(devengari)),
            ap90=self.serialize_results(self.ap90.search(devengari)),
        )
