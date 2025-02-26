import pycdsl


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
