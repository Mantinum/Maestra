# Feuille de route fine-tuning

Ce dossier contiendra les scripts nécessaires pour adapter un modèle de langage au rôle de professeure de corse.

## Modèle de base

Nous visons un modèle open source de type instruct, par exemple **Mixtral 8x7B Instruct** ou tout équivalent sous licence permissive, garantissant la possibilité de redistribution après fine-tuning.

## Stratégie d'adaptation

1. Préparation des données depuis `../data/training_examples.jsonl`.
2. Application d'un fine-tuning **LoRA** pour limiter les coûts d'entraînement et de stockage.
3. Évaluation qualitative et quantitative des réponses (correction linguistique, justesse culturelle, ton professoral).

L'objectif est de produire un modèle qui :

- répond naturellement en corse,
- sait expliquer les règles linguistiques en français,
- corrige les erreurs en corse en explicitant les corrections,
- traduit efficacement entre le français et le corse.

## État actuel

Le script `finetune.py` est un simple placeholder. Les étapes de préparation des données, de configuration du modèle et de lancement de l'entraînement seront implémentées ultérieurement.
