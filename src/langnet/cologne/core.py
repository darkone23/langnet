import pycdsl
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

from indic_transliteration.detect import detect


class SanskritCologneLexicon:
    def __init__(self):
        self.CDSL: pycdsl.CDSLCorpus = pycdsl.CDSLCorpus()
        self.CDSL.setup()

        # Sanskrit-English
        self.mw: pycdsl.CDSLDict = self.CDSL["MW"]
        self.ap90: pycdsl.CDSLDict = self.CDSL["AP90"]

        # print()

        # top_terms = self.mw.stats(top=1024 * 8)

        # for term in top_terms["top"]:
        #     (k, v) = term
        #     it = transliterate(k, sanscript.DEVANAGARI, sanscript.ITRANS)
        #     print(SCHEMES[sanscript.OPTITRANS].to_lay_indian(it))

        # English-Sanskrit
        self.mwe: pycdsl.CDSLDict = self.CDSL["MWE"]
        self.ae: pycdsl.CDSLDict = self.CDSL["AE"]

    def transliterate(self, data):
        mode = detect(data)
        # print("using mode", mode)
        return transliterate(data, mode, sanscript.DEVANAGARI)

    def serialize_results(self, results: list[pycdsl.lexicon.Entry]):
        # need to group results by ID
        # rule: if lexicon id contains a dot group on LHS
        return [
            dict(
                id=result.id,
                key=result.key,
                # iast=transliterate(result.key, sanscript.DEVANAGARI, sanscript.IAST),
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
