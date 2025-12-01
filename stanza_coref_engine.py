import stanza
import gap_coref_eval
import os


class StanzaCorefEngine(gap_coref_eval.DummyCorefEngine):
    def __init__(self, name="Stanza"):
        self.name = name
        self.pipe = stanza.Pipeline(lang='en', processors='tokenize,coref')

    def resolve_coref(self, text: str, pronoun: str, p_offset: int, cand_a: str, cand_b: str, verbose=False):
        document = self.pipe(text).to_dict()
        for phrase in document:
            for word in phrase:
                if (word["start_char"] >= p_offset \
                        and word["text"] == pronoun \
                        and len(word["coref_chains"]) > 0):
                    #print("[DEBUG] word "+str(word)+" compared with "+pronoun)
                    if word["coref_chains"][0].chain.representative_text == cand_a:
                        return (True, False)
                    if word["coref_chains"][0].chain.representative_text == cand_b:
                        return (False, True)
                    else:
                        return (False, False)
        return (False, False)
        #print(dd[1][0]["coref_chains"][0].chain.representative_text)

if __name__ == "__main__":
    ce = StanzaCorefEngine()
    ev = gap_coref_eval.test_engine(ce, os.getcwd()+"/modules/gap-coreference/gap-development.tsv", verbose=True)
    print(ev)
    open(os.getcwd()+"/eval_results/"+ce.name+".txt", "w").write(str(ev))
