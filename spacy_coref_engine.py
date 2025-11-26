import spacy
import coreferee
import test_gap
import os

class SpaCyCorefEngine(test_gap.CorefEngine):
    def __init__(self, name="SpaCy", model="en_core_web_sm"):
        self.name=name+"_"+model
        self.nlp = spacy.load(model)
        self.nlp.add_pipe("coreferee")

    def resolve_coref(self, text: str, pronoun: str, p_offset: int, cand_a: str, cand_b: str):
        doc = self.nlp(text)
        chains = doc._.coref_chains

        returnval = (False, False)

        # Look through each chain for the pronoun at the right offset
        for chain in chains:
            for mention in chain:
                if len(str(doc[0:mention[0]])) == p_offset:
                    # Found the pronoun, does the pronoun resolve to cand_a or cand_b?
                    resolved = chains.resolve(mention)
                    if resolved == cand_a:
                        returnval = (True, False)
                    elif resolved == cand_b:
                        returnval = (False, True)
        return returnval


if __name__ == "__main__":
    ce = SpaCyCorefEngine()
    print(test_gap.test_engine(ce, os.getcwd()+"/modules/gap-coreference/gap-development.tsv"))




