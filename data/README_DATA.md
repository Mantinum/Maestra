# Jeu de données d'entraînement (à venir)

Ce dossier accueillera les données d'instruction-tuning dédiées à l'IA corse *A Maestra*.

## Format attendu

Les exemples seront stockés dans un fichier `JSONL`, chaque ligne représentant un couple instruction / réponse, avec des métadonnées permettant de filtrer ou de composer les jeux d'apprentissage.

### Exemple de ligne

```json
{
  "instruction": "Corrige cette phrase en corse : « Iò so contenta di vedeti. »",
  "response": "Sò cuntenta di vedeti. Explication : …",
  "tags": [
    "correction",
    "corse",
    "grammaire",
    "registre:standard"
  ]
}
```

* `instruction` : consigne ou question posée au modèle.
* `response` : réponse attendue (en corse ou bilingue selon le mode).
* `tags` : liste libre pour indiquer la nature de la tâche (correction, traduction, difficulté, registre, etc.).

## Organisation proposée

- `training_examples.jsonl` : corpus principal destiné au fine-tuning LoRA.
- Fichiers supplémentaires optionnels (validation, tests) pourront être ajoutés ultérieurement.

Pour l'instant, ce dossier ne contient que des placeholders afin de préparer l'intégration future des données.
