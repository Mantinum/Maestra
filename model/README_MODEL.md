# Fine-tuning LoRA pour *A Maestra*

Ce dossier regroupe les ressources nécessaires pour adapter un modèle de langue généraliste en professeure de corse.

## Modèle de base

Nous partons d'un modèle open source de type *instruct* (ex. `mistralai/Mistral-7B-Instruct-v0.2`). Il doit impérativement être distribué sous licence permissive pour permettre la publication du résultat.

## Données

Le script `finetune.py` consomme les exemples d'instruction-tuning stockés dans `../data/training_examples.jsonl`. Chaque entrée contient :

- `instruction` : consigne utilisateur,
- `response` : réponse attendue de Maestra,
- `tags` : métadonnées (registre, niveau, etc.).

Les prompts sont reformattés sous la forme :

```
<s>Instruction: …
Réponse: …</s>
```

## Stratégie LoRA

1. Chargement du modèle de base et du tokenizer Hugging Face.
2. Application d'un adaptateur LoRA léger (`r=16`, `alpha=32`, `dropout=0.05`).
3. Entraînement 3 époques sur notre dataset corse.
4. Sauvegarde de l'adapter dans `model/checkpoints/adapter/` (poids LoRA + tokenizer).

Les hyperparamètres (batch size, accumulation, précision `fp16`/`bf16`) sont volontairement modérés pour tenir sur un GPU unique.

## Tester le modèle

La fonction `generate_demo()` du script :

- recharge le modèle de base,
- applique l'adapter LoRA sauvegardé,
- formate une instruction au même format que l'entraînement,
- génère une réponse (ex. `model.generate()`),
- renvoie le texte produit.

Cela permet de valider rapidement la qualité du modèle fine-tuné avant intégration dans l'API.

## Installation des dépendances

Les bibliothèques nécessaires à l'entraînement sont listées dans `model/requirements.txt`. Elles ne sont pas indispensables pour lancer l'API FastAPI ou le frontend React : installez-les uniquement sur l'environnement GPU dédié à l'entraînement.
