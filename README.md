# COREF TEST

Part of the COMMEDIA Navel project

Attempt at answering the question "is it better to use a discrete coreference evaluation library or can an LLM handle it all"

## HOW TO RUN

### LINUX

```bash
./prepare_repo.sh
source spacy_venv/bin/activate
python spacy_coref_engine.py
python llm_coref_engine.py

source stanza_venv/bin/activate
python stanza_coref_engine.py
```
