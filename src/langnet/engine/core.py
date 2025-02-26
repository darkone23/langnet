from langnet.diogenes.core import DiogenesScraper, DiogenesLanguages
from langnet.whitakers_words.core import WhitakersWords
from langnet.classics_toolkit.core import ClassicsToolkit
from langnet.cologne.core import SanskritCologneLexicon


class LanguageEngine:

    def __init__(
        self,
        scraper: DiogenesScraper,
        whitakers: WhitakersWords,
        cltk: ClassicsToolkit,
        cdsl: SanskritCologneLexicon,
    ):
        self.diogenes = scraper
        self.whitakers = whitakers
        self.cltk = cltk
        self.cdsl = cdsl

    def handle_query(self, lang, word):
        print("got query:", word, lang)
        # at this point word and lang are utf-8 characters as presented by the user

        result = dict(diogenes=self.diogenes.parse_word(word, lang))

        if lang == DiogenesLanguages.LATIN:
            result["whitakers"] = self.whitakers.words([word])
            result["lewis1890"] = self.cltk.latdict.lookup(
                # always better to look up a headword in the dictionary
                word
            )  # Charlton T. Lewis's *An Elementary Latin Dictionary* (1890).

        if lang == DiogenesLanguages.GREEK:
            pass

        # TODO: add basic sanskrit lexicon support via CDSL
        # add some basic 'what sort of input is this' mode checking

        return result
