#!/bin/bash
# Gestion de la version de Python sur environnement Linux
# et création de l'environnement pour SpaCy
pyenv init && pyenv local 3.11.2
pyenv exec python3 -m venv spacy_venv || python3 -m venv spacy_venv
source spacy_venv/bin/activate && python -m pip install -r spacy_requirements.txt

# Gestion des modèles coreferee
python -m coreferee install en
python -m coreferee install fr

# Initialisation des modules git
git submodule update --init --recursive

# Stanza setup. Presumably, should be fine switching pyenv local
# since the other venv's version is already set
# pyenv local 3.13.7
# pyenv exec python3 -m venv stanza_venv || 
python3 -m venv stanza_venv
source stanza_venv/bin/activate && python -m pip install -r stanza_requirements.txt
