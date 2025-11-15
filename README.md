# A Maestra

*A Maestra* est une application web expérimentale permettant d'interagir avec une professeure virtuelle spécialisée dans la langue corse. Cette première itération fournit l'architecture complète (front-end, back-end, dossiers données et modèle) avec des réponses simulées, en attendant l'intégration du véritable modèle IA.

## Parcours utilisateur

1. L'utilisateur ou l'utilisatrice choisit un mode d'interaction :
   - **talk** : conversation en corse,
   - **translate** : traduction français ↔ corse,
   - **correct** : correction d'une phrase corse avec explication,
   - **explain** : explication d'une règle de langue.
2. Il ou elle saisit son texte dans le champ prévu.
3. Le front-end envoie une requête `POST /api/chat` au backend FastAPI.
4. L'API renvoie pour l'instant une réponse simulée (`"TODO: ..."`). Lorsque le modèle sera entraîné, cette couche restera inchangée.

## État actuel

- **/api** : service FastAPI prêt à être connecté à un modèle IA (simulation statique pour l'instant).
- **/web** : interface React simple permettant de sélectionner un mode, saisir un texte et afficher la réponse renvoyée par l'API.
- **/data** : documentation du futur format `JSONL` pour le fine-tuning et fichier d'exemples (vide).
- **/model** : documentation de la stratégie de fine-tuning LoRA et script placeholder.

L'objectif est de pouvoir lancer `uvicorn api.main:app --reload` d'un côté et `npm install && npm run dev` dans `web/` de l'autre, afin de tester le flux de bout en bout avec les réponses simulées.
