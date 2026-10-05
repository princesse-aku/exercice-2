# Exercice 2 - API RodiumAI sans SDK

Ce projet utilise directement l'API RodiumAI avec Python et la bibliothèque
requests, sans utiliser le SDK RodiumAI.

## Prérequis

- Python 3.13 ou version compatible
- Une clé API RodiumAI

## Installation

Installer les dépendances :

    pip install -r requirements.txt

## Configuration

Copier .env.example vers .env :

    copy .env.example .env

Puis renseigner votre clé API RodiumAI dans .env :

    RODIUMAI_API_KEY=rd_sk_votre_cle

Ne partagez jamais votre fichier .env.

## Lancement

Exécuter :

    python main.py

Le programme propose successivement :
1. une interaction avec le Chat ;
2. une génération d'image ;
3. une génération de vidéo.

Chaque étape permet de refaire l'action ou de passer à l'étape suivante.
