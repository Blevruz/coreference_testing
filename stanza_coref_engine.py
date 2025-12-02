import stanza
import gap_coref_eval
import os








class StanzaCorefEngine(gap_coref_eval.DummyCorefEngine):
    def __init__(self, name="Stanza"):
        self.name = name
        self.pipe = stanza.Pipeline(lang='en', processors='tokenize,coref')

    def process_text(self, text):
        document = self.pipe(text)
        corefs = dict()
        for sentence in document.sentences:
            last_coref = None
            for token in sentence.tokens:
                d = token.to_dict()
                if "coref_chains" in d[0]:
                    for chain in d[0]["coref_chains"]:
                        if chain.chain.representative_text not in corefs:
                            corefs[chain.chain.representative_text] = list()
                        if last_coref is chain.chain.representative_text:
                            corefs[chain.chain.representative_text][-1] += " "+token.text
                        else:
                            corefs[chain.chain.representative_text].append(token.text)
                            last_coref = chain.chain.representative_text
                else:
                    last_coref = None
        print(corefs)

            

    def resolve_coref(self, text: str, pronoun: str, p_offset: int, cand_a: str, cand_b: str, verbose=False):
        self.process_text(text)
        input()
        #document = self.pipe(text)#.to_dict()
        #for sentence in document.sentences:
        #    for token in sentence.tokens:
        #        print(token.text, end="")
        #        try:
        #            d = token.to_dict()
        #            if "coref_chains" in d[0]:
        #                print("[", end='')
        #                for chain in d[0]["coref_chains"]:
        #                    print(chain.chain.representative_text, end=',')
        #                print("]", end='')
        #        except Exception as e:
        #            print(f"[ERROR] {e}")



        #    input()
                #if (token["start_char"] >= p_offset \
                #        and token["text"] == pronoun \
                #        and len(token["coref_chains"]) > 0):
                #    #print("[DEBUG] token "+str(token)+" compared with "+pronoun)
                #    for attachment in token["coref_chains"]:
                #        print("[DEBUG]\tattachment's chain representative text: "+\
                #                str(attachment.chain.representative_text)+\
                #                "\n\tattachment is_representative:"+\
                #                str(attachment.is_representative))
                #        for mention in attachment.chain.mentions:
                #            print("[DEBUG]\tmention's sentence: "+str(mention.sentence)+\
                #                    "\n\tmention's start_token: "+str(mention.start_token)+\
                #                    "\n\tmention's end_token: "+str(mention.end_token))
                #            mentioned = document[int(mention.sentence)-1][int(mention.start_token)-1:int(mention.end_token)-1]
                #            print("[DEBUG]\t\tmentioned's text: "+str(mentioned))



                #        if attachment.chain.representative_text == cand_a:
                #            print("[DEBUG] token "+str(token)+\
                #                    "'s resolution \""+attachment.chain.representative_text+\
                #                    "\" matched with "+cand_a)
                #            return (True, False)
                #        if attachment.chain.representative_text == cand_b:
                #            print("[DEBUG] token "+str(token)+\
                #                    "'s resolution \""+attachment.chain.representative_text+\
                #                    "\" matched with "+cand_b)
                #            return (False, True)
                #        else:
                #            print("[DEBUG] token "+str(token)+\
                #                    "'s resolution \""+attachment.chain.representative_text+\
                #                    "\" not matched with either "+cand_a+" or "+cand_b)
                #        #return (False, False)
        return (False, False)
        #print(dd[1][0]["coref_chains"][0].chain.representative_text)

if __name__ == "__main__":
    ce = StanzaCorefEngine()
    ev = gap_coref_eval.test_engine(ce, os.getcwd()+"/modules/gap-coreference/gap-development.tsv", verbose=True)
    print(ev)
    open(os.getcwd()+"/eval_results/"+ce.name+".txt", "w").write(str(ev))
