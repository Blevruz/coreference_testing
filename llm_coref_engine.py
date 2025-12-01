

import gap_coref_eval
import os
import json
import requests

# We assume a llama.cpp server is running at the given address
# But since it uses the openai api, it should be generalizable
class LLMCorefEngine(gap_coref_eval.DummyCorefEngine):
    def __init__(self, name="LLM", model_rq="", 
                 address="http://localhost:8000",
                 temperature=0.3,
                 max_tokens_per_call=512):

        # getting the list of models at the given address
        response = requests.get(address + "/v1/models")
        models = json.loads(response.text)["data"]
        models = [model["id"] for model in models]
        if model_rq in str(models):
            for m in models:
                if model_rq in m:
                    self.model = m
                    break
            #self.model = model_rq
            self.address = address
        else:
            print(f"Model {model_rq} not found")
            print("Available models: ")
            print(models)
            exit(1)
        self.name=name
        self.temperature=temperature
        self.max_tokens=max_tokens_per_call

    def prompt(self, text, pronoun, p_offset, verbose=False):

        boilerplate_headers = {
            "Content-Type": "application/json"
        }

        prompt = f"""
        ```
        {text}
        ```
        In the previous text, to whom or what does the pronoun \"{pronoun}\" (at offset {p_offset}) refer?
        Your answer should end with a colon and the name of the entity.
        """
        if verbose:
            print(f"[DEBUG] Sending prompt: {prompt}")
            print(f"[DEBUG] Sending request to {self.address}/v1/chat/completions")

        req = requests.post(self.address + "/v1/chat/completions", 
                            headers=boilerplate_headers, 
                            json={
                                "model": self.model, 
                                "messages": [{"role": "user", "content": prompt}],
                                "max_tokens": self.max_tokens,
                                "temperature": self.temperature,
                            },
                            timeout=60)
        if verbose:
            print(f"[DEBUG] Received response: {req.text}")
        return req.json()["choices"][0]["message"]["content"].split(":")[-1].strip()

        

    # LLM-based coreference resolution approach: question-answering approach
    def resolve_coref(self, text: str, pronoun: str, p_offset: int, cand_a: str, cand_b: str, verbose=False):
        reply = self.prompt(text, pronoun, p_offset, verbose)
        return (reply in cand_a or cand_a in reply, 
                reply in cand_b or cand_b in reply)



if __name__ == "__main__":
    secrets = json.load(open("secrets.json"))
    evals = []
    for setup in secrets:
        lce = LLMCorefEngine(setup["name"], setup["model"], setup["address"])
        evals.append(gap_coref_eval.test_engine(lce, os.getcwd()+"/modules/gap-coreference/gap-development.tsv", verbose=True))
        open(os.getcwd()+"/eval_results/"+lce.name+".txt", "w").write(str(evals[-1]))
