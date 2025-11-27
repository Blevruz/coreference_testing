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
                # Getting the length of the text before the mention in
                # characters, as give in the dataset, as opposed to the size
                # in words. Note the +1 is to account for the last space
                if int(len(str(doc[0:mention[0]])) + 1) == int(p_offset):
                    # Found the pronoun, does it resolve to cand_a or cand_b?
                    resolved = chains.resolve(doc[mention[0]])
                    if resolved == None:
                        continue
                    # resolved is a list of tokens, which are annoying to convert to string
                    str_resolved = ""
                    for word in resolved:
                        str_resolved += str(word) + " "
                    # Removing trailing space
                    str_resolved = str_resolved[:-1]
                    # referee only returns one word per resolution, so we need to
                    # check if the resolution is a substring of the candidate
                    if str_resolved in str(cand_a):
                        print("[DEBUG] Matched cand_a", cand_a, "to", str_resolved)
                        returnval = (True, False)
                        # only one resolution per call so we can return
                        return returnval
                    elif str_resolved in str(cand_b):
                        print("[DEBUG] Matched cand_b", cand_b, "to", str_resolved)
                        returnval = (False, True)
                        return returnval
                    else:
                        print("[DEBUG] Found no match for", str_resolved, "with candidates", cand_a,",", cand_b)
        return returnval

# function useful for testing
def resolve_string(coref_engine, text: str):
        doc = coref_engine.nlp(text)
        chains = doc._.coref_chains
        for chain in chains:
            for mention in chain:
                for index in mention:
                    print(doc[index],"at index",index,"resolves to", chains.resolve(doc[index]))


if __name__ == "__main__":
    ce = SpaCyCorefEngine(model="en_core_web_sm")
    eval_sm = test_gap.test_engine(ce, os.getcwd()+"/modules/gap-coreference/gap-development.tsv")
    open(os.getcwd()+"/eval_results/"+ce.name+".txt", "w").write(str(eval_sm))
    ce = SpaCyCorefEngine(model="en_core_web_lg")
    eval_lg = test_gap.test_engine(ce, os.getcwd()+"/modules/gap-coreference/gap-development.tsv")
    open(os.getcwd()+"/eval_results/"+ce.name+".txt", "w").write(str(eval_lg))
    ce = SpaCyCorefEngine(model="en_core_web_trf")
    eval_trf = test_gap.test_engine(ce, os.getcwd()+"/modules/gap-coreference/gap-development.tsv")
    open(os.getcwd()+"/eval_results/"+ce.name+".txt", "w").write(str(eval_trf))

    print("Evaluation of en_core_web_sm:", eval_sm)
    print("Evaluation of en_core_web_lg:", eval_lg)
    print("Evaluation of en_core_web_trf:", eval_trf)
