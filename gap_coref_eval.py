# Make sure you've used `git submodule --init --recursive`!
import sys
import os
import csv
import time
sys.path.append(os.getcwd()+"/modules/gap-coreference")
import gap_scorer
from constants import Gender
from constants import GOLD_FIELDNAMES
from constants import PRONOUNS
from constants import SYSTEM_FIELDNAMES

# Generic coreference engine
class DummyCorefEngine:
    def __init__(self, name="dummy"):
        self.name=name

    def resolve_coref(self, text: str, pronoun: str, p_offset: int, cand_a: str, cand_b: str, verbose=False):
        assert isinstance(text, str), f"text input should be a string, but was instead {type(text)}"
        assert isinstance(pronoun, str), f"pronoun input should be a string, but was instead {type(pronoun)}"
        assert isinstance(p_offset, int), f"p_offset input should be an integer, but was instead {type(p_offset)}"
        # Check that pronoun is at p_offset in the text
        assert text[p_offset:p_offset+len(pronoun)] == pronoun, "Pronoun is not at p_offset in the text"
        assert isinstance(cand_a, str), f"cand_a input should be a string, but was instead {type(cand_a)}"
        assert isinstance(cand_b, str), f"cand_b input should be a string, but was instead {type(cand_b)}"
        return (False, False)

def outname(ce, file):
    return file+"."+ce.name+".out"

def resolve_file(coref_engine, file, verbose = False):
    startstring = "Progress: ["
    if verbose:
        print("Resolving file "+file)
        # dont be afraid of the funny ansi escape sequences
        print(f"{startstring}\033[{80-len(startstring)}C]\033[{80-len(startstring)}D")
        #then getting the cursor back to the start
    with open(file, "r") as f:
        if verbose:
            # get number of lines in the file
            nb_lines = sum(1 for line in f) - 1 
            index = 0
            f.seek(0)
        # opening development, which is a "gold" (reference) file
        reader = csv.DictReader(f, fieldnames=GOLD_FIELDNAMES, delimiter='\t')
        next(reader, None)  # first line explains which fields are which

        output_file = open(outname(coref_engine, file), "w")
        writer = csv.DictWriter(output_file, fieldnames=SYSTEM_FIELDNAMES, delimiter='\t')
        for row in reader:
            result = coref_engine.resolve_coref(row['Text'], row['Pronoun'], int(row['Pronoun-offset']), row['A'], row['B'], verbose=False)
            writer.writerow({"ID": row['ID'], "A-coref": result[0], "B-coref": result[1]})
            if verbose:
                index += 1
                if int(index/nb_lines*(80-len(startstring))) % 1 == 0:
                    print(f"\033[1A\033[{int(index/nb_lines*(80-len(startstring)))+len(startstring)}C=")
                    time.sleep(0.1)
        output_file.close()
        f.close()


def test_engine(coref_engine, file, verbose = False):
    if verbose:
        print("Testing engine "+coref_engine.name+" on file "+file)
    timestart = time.time()
    resolve_file(coref_engine, file, verbose)
    duration = time.time() - timestart
    score = "Coreference engine "+coref_engine.name+" on file "+file+" scored: "
    score += gap_scorer.run_scorer(file, outname(coref_engine, file))
    score += "Whole run time: "+str(duration)+" seconds"
    return score

if __name__ == '__main__':
    ce = DummyCorefEngine()
    print(test_engine(ce, os.getcwd()+"/modules/gap-coreference/gap-development.tsv", verbose=True))

