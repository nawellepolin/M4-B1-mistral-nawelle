# Verdict — Recommandation Mistral Assurances

> **5 lignes maximum.** Document remis à Inès Tabet.
> Auteur : `Nawelle` — Date : `2026-08-19`

**Recommandation** : passer de `mistral-tarif-v1` (régression linéaire) à un modèle **HistGradientBoosting**.

**Raison principale (chiffrée)** : erreur moyenne divisée par deux (51 trajets contre 105 aujourd'hui) et part des variations expliquée qui passe de 39 % à 80 %, sans coût de mémoire ni de vitesse supplémentaire (fichier plus léger que l'actuel, réponse en 2,4 ms pour 1000 prédictions).

**Condition de changement d'avis** : si une justification détaillée du calcul devient une obligation réglementaire pour chaque tarif individuel, alors je proposerais **Ridge** (linéaire) à la place — moins précis, mais dont chaque facteur reste directement lisible.

---

*Verdict produit par Nawelle, 2026-08-19, dans le cadre du brief M4-B1 ATOS.*
