#!/bin/bash
# Gestion de la version de Python sur environnement Linux
# et installation des dépendances
pyenv init && pyenv local 3.11.2
pyenv exec python3 -m venv venv || python3 -m venv venv
source venv/bin/activate && python -m pip install -r requirements.txt

# Gestion des modèles coreferee
python -m coreferee install en
python -m coreferee install fr
