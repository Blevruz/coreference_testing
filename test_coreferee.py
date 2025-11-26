import spacy
import coreferee
import test_gap

# Load a spaCy model — you can choose a transformer or a smaller model
nlp = spacy.load("en_core_web_sm")  # or “fr_core_news_lg” etc.

# Add coreferee to the pipeline
nlp.add_pipe("coreferee")

# Coreference enginer using SpaCy coreferee
class SpaCyCorefEngine(CorefEngine):
    def __init__(self, name="prototype"):
        self.name=name

    def resolve_coref(self, text: str):
        doc = nlp(text)
        chains = doc._.coref_chains

        print("Coreference chains:")
        chains.print()

        # Example: resolve for each mention
        for chain in chains:
            mentions = [span for span in chain]
            print("Chain mentions:", mentions)
            # chain.resolve returns representative mentions (by head)
            for m in mentions:
                resolved = chains.resolve(m)
                print(" → For mention", m, "resolved to", resolved)

        # You could also build a “resolved” text by replacing mentions:
        # (very naive strategy shown in some gists)
        tokens = [token.text for token in doc]
        offset = 0
        for chain in chains:
            main = chain.main  # the main mention
            for mention in chain:
                # here mention is a Span, you could replace token by token
                start, end = mention.start, mention.end
                rep = main.text
                tokens[start+offset] = rep
                # if replacement is longer than original, insert
                if len(rep.split()) > (end - start):
                    for i in range(len(rep.split())-1):
                        tokens.insert(end+i, '')
                    offset += len(rep.split())-1
                # if replacement is shorter than original, remove
                if len(rep.split()) < (end - start):
                    for i in range(end - start - len(rep.split())):
                        del tokens[end+i]



def resolve_coref(text: str):
    doc = nlp(text)
    chains = doc._.coref_chains

    print("Coreference chains:")
    chains.print()

    # Example: resolve for each mention
    for chain in chains:
        mentions = [span for span in chain]
        print("Chain mentions:", mentions)
        # chain.resolve returns representative mentions (by head)
        for m in mentions:
            resolved = chains.resolve(m)
            print(" → For mention", m, "resolved to", resolved)

    # You could also build a “resolved” text by replacing mentions:
    # (very naive strategy shown in some gists)
    tokens = [token.text for token in doc]
    offset = 0
    for chain in chains:
        main = chain.main  # the main mention
        for mention in chain:
            # here mention is a Span, you could replace token by token
            start, end = mention.start, mention.end
            rep = main.text
            tokens[start+offset] = rep
            # if replacement is longer than original, insert
            if len(rep.split()) > (end - start):
                for i in range(len(rep.split()) - (end - start)):
                    tokens.insert(start + offset + 1 + i, "")
                offset += len(rep.split()) - (end - start)
    resolved_text = " ".join(tokens)
    return resolved_text

if __name__ == "__main__":
    text = "My colleague lives in Paris. She loves the city."
    print("Original:", text)
    print("Resolved:", resolve_coref(text))

