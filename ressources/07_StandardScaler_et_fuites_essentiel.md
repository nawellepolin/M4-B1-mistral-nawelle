# StandardScaler & fuite de prétraitement — Mini-cours

> Brief associé : M4-B1
> Durée de lecture : ~25 min
> Pré-requis : `Pipeline` scikit-learn vu en M2-B1 ; `cross_val_score` et les
> trois types de fuite vus dans [`02_Split_temporel_vs_stratifie_essentiel.md`](./02_Split_temporel_vs_stratifie_essentiel.md).

## En un mot : le scaler est-il obligatoire ? À faire tout le temps ?

> **Non.** Standardiser n'est **jamais obligatoire en soi** — ça dépend du
> modèle.
>
> - ✅ **Indispensable** pour la régression **linéaire / Ridge / Lasso**, le
>   **SVM**, le **k-NN**, les **réseaux de neurones** (tout ce qui repose sur des
>   distances, des poids ou une descente de gradient).
> - ❌ **Inutile** pour les **arbres**, **Random Forest** et **boosting**
>   (`HistGradientBoosting`) : ils coupent sur des seuils, l'échelle ne change
>   rien. Scaler ne les casse pas, mais ne sert à rien.
>
> Donc **pas de réflexe « je scale toujours »**. On scale **parce qu'un modèle en
> a besoin**, pas par principe. C'est un **critère de décision C4**, pas une case
> à cocher.
>
> ⚠️ En revanche, **quand** on scale, une règle *est* obligatoire : le scaler va
> **dans le `Pipeline`**, jamais `fit` sur tout `X` avant le split (sinon fuite —
> cf. § plus bas).

## Pourquoi cette techno ?

Dans le benchmark M4-B1 tu compares **trois familles de modèles** (linéaire,
arbres, boosting) sur Bike Sharing. Deux d'entre elles n'ont pas les mêmes
besoins de préparation : la **régression linéaire / Ridge** exige des features
**à la même échelle** pour que ses coefficients et sa régularisation aient un
sens, alors que les **arbres et le boosting** s'en moquent (ils coupent sur des
seuils). Le `StandardScaler` est l'outil qui met les colonnes à la même échelle.

Ce n'est donc **pas une étape systématique** qu'on applique « pour faire
propre » : c'est un choix de préparation **piloté par le modèle**. Savoir *quand*
scaler et *quand ne pas* est un critère de décision C4 à part entière.

Alternatives : `MinMaxScaler` (borne dans [0, 1], sensible aux valeurs
extrêmes), `RobustScaler` (basé sur la médiane et l'IQR, résistant aux
outliers). On reste sur `StandardScaler` en M4-B1, standard et suffisant.

## Concepts clés

### 1. Ce que fait la standardisation

Pour chaque colonne, on retranche la moyenne `μ` et on divise par l'écart-type
`σ` :

```
x_scaled = (x - μ) / σ
```

Après transformation, **chaque feature a une moyenne de 0 et un écart-type de
1**. Les colonnes deviennent comparables entre elles, quelle que soit leur unité
d'origine (des km/h, un pourcentage, un compte…).

### 2. `fit` apprend, `transform` applique

C'est le point central pour comprendre la fuite. Le scaler **apprend deux
paramètres** — `μ` et `σ` — au moment du `.fit()`, puis les réutilise à chaque
`.transform()` :

- **`.fit(X_train)`** : calcule `μ` et `σ` **sur les données d'entraînement uniquement**.
- **`.transform(X_train)`** puis **`.transform(X_test)`** : applique les *mêmes*
  `μ` et `σ` aux deux jeux.

Le test est standardisé avec les statistiques du **train**, jamais les siennes.
C'est voulu : en production, tu n'auras pas encore vu les données futures pour
calculer leur moyenne — tu appliques celle que tu connais.

### 3. Quels modèles ont besoin du scaler ?

| Famille de modèle | Scaler nécessaire ? | Pourquoi |
|---|---|---|
| Régression linéaire, **Ridge**, Lasso | ✅ **Oui** | Les coefficients dépendent de l'échelle ; la régularisation (`alpha`) pénalise injustement une feature à grande amplitude |
| SVM, k-NN, réseaux de neurones | ✅ Oui | Basés sur des **distances** ou une **descente de gradient** |
| Arbres, Random Forest, **HistGradientBoosting** | ❌ **Non** | Un arbre coupe sur des seuils (`temp > 0.5`) ; multiplier une colonne par 1000 ne change pas l'ordre des valeurs, donc pas les coupures |

> C'est exactement pour cette raison que la **solution retenue** de M4-B1 (un
> boosting d'arbres) **n'a pas de scaler**. Le scaler n'apparaît que sur la
> **baseline linéaire** — pour montrer que *ce modèle-là en a besoin, l'autre
> non*. Standardiser un arbre n'est pas faux, c'est juste **inutile**.

### 4. La fuite de prétraitement

Le scaler apprend `μ` et `σ`. Si tu le `fit` sur **tout `X`** *avant* de découper
en folds, ces statistiques intègrent aussi les lignes qui serviront de test :
ton modèle a « respiré » la distribution du test. C'est la **fuite de
prétraitement** — la troisième fuite de [`02_Split`](./02_Split_temporel_vs_stratifie_essentiel.md),
la plus discrète des trois.

**La parade est toujours la même : enfermer le scaler dans le `Pipeline`.**
scikit-learn re-`fit` alors le scaler sur les **seuls** folds d'entraînement, à
chaque pli de la cross-validation.

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score

# ✅ PROPRE — le scaler est re-fitté sur chaque fold d'entraînement
pipe = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
scores = cross_val_score(pipe, X, y, cv=splitter, scoring="r2")

# ❌ FUITE — le scaler a vu tout X (dont les folds de test) avant la CV
# X_scaled = StandardScaler().fit_transform(X)
# scores = cross_val_score(Ridge(), X_scaled, y, cv=splitter, scoring="r2")
```

Règle d'or : **ne passe jamais un `X` déjà transformé à `cross_val_score`**.
Tu passes le `Pipeline` complet, et scikit-learn gère la séparation.

### 5. La fuite la plus dangereuse est celle qui ne se voit pas

Sur Bike Sharing (~17 000 lignes homogènes), l'écart de score entre la version
« fuite de prétraitement » et la version « propre » est **minuscule** : de
l'ordre de **± 0.0005 de R², parfois même négatif**, invisible à l'arrondi. La
raison est structurelle : sur un gros jeu homogène, les `μ`/`σ` d'un fold ≈ les
`μ`/`σ` globaux, donc la fuite ne change presque rien.

Contraste avec les deux autres fuites, mesuré sur le même dataset :

| Version | R² observé | Verdict |
|---|---|---|
| Fuite de **cible** (`casual_riders` + `registered_riders` dans `X`) | **1.0000** | 🚨 le gyrophare — saute aux yeux |
| Fuite de **prétraitement** (scaler fitté sur tout `X`) | ≈ **+0.0000** vs propre | 👻 invisible |
| **Propre** (scaler dans le `Pipeline`) | 0.2591 | ✅ la vraie performance |

**La leçon :** on n'encapsule pas le prétraitement « quand l'écart est visible »,
on l'encapsule **par défaut**. Le danger devient bien réel avec **peu de
données**, une **imputation** par moyenne/médiane, ou un **encodage supervisé**
(`TargetEncoder`) — là, la fuite peut gonfler le score de plusieurs points. La
bonne habitude se prend maintenant, sur un cas où elle ne coûte rien.

## Exemple minimal qui tourne

```python
# scikit-learn >= 1.4, numpy >= 1.26
import numpy as np
from sklearn.preprocessing import StandardScaler

X = np.array([[10.0], [20.0], [30.0], [40.0]])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("moyenne apprise (μ) :", scaler.mean_)        # [25.]
print("écart-type appris (σ):", np.sqrt(scaler.var_))  # [11.18]
print("données standardisées :\n", X_scaled.ravel())   # [-1.34 -0.45 0.45 1.34]
print("moyenne après scaling :", X_scaled.mean().round(6))  # 0.0
print("écart-type après scaling :", X_scaled.std().round(6)) # 1.0
```

Tu vois concrètement que le scaler **stocke** `μ` et `σ` (dans `mean_` et
`var_`) et que la sortie est centrée-réduite.

## Exercice guidé

Sur `data/bike_sharing.csv`, mesure toi-même l'effet de la fuite de
prétraitement, puis l'effet du scaler selon le modèle.

1. Prépare `X` (sans `casual_riders`/`registered_riders`) et `y = total_rentals`.
2. **Version fuite** : `X_scaled = StandardScaler().fit_transform(X)` puis
   `cross_val_score(Ridge(), X_scaled, y, cv=TimeSeriesSplit(5), scoring="r2")`.
3. **Version propre** : `cross_val_score(make_pipeline(StandardScaler(),
   Ridge()), X, y, cv=TimeSeriesSplit(5), scoring="r2")`.
4. Compare les deux R² moyens. **Puis** relance la version propre en remplaçant
   `Ridge()` par un `HistGradientBoostingRegressor()` **avec et sans** le scaler.

**Questions** : (a) De combien la fuite de prétraitement change-t-elle le R² ?
(b) Le scaler change-t-il quelque chose pour le boosting ?

**Attendu** : (a) un écart de l'ordre de ± 0.001, **invisible** — ce qui doit te
convaincre d'encapsuler *par principe*, pas *par mesure*. (b) **aucune
différence** pour le boosting : le scaler lui est inutile. Tu sais désormais
justifier « je scale pour la régression linéaire, pas pour les arbres ».

## Pièges fréquents

| Piège | Conséquence |
|---|---|
| `StandardScaler().fit_transform(X)` avant la CV | Fuite de prétraitement → scores optimistes (mets le scaler dans le `Pipeline`) |
| `scaler.fit(X_test)` (ou `fit_transform` sur le test) | Le test est standardisé avec ses propres stats → fuite + incohérence prod |
| Scaler un **arbre / boosting** et croire que ça améliore | Inutile ; fausse l'idée que « scaler = toujours mieux » |
| Standardiser des colonnes **one-hot** (0/1) | Inutile, rend les valeurs illisibles ; scale plutôt les seules colonnes continues |
| Oublier le scaler pour la **régression linéaire** | Coefficients ininterprétables, régularisation `alpha` biaisée par l'échelle |
| Refitter un nouveau scaler en production | Les `μ`/`σ` changent → prédictions incohérentes ; on **sauvegarde** le scaler entraîné (dans le `Pipeline` picklé) |

**Symptôme → cause probable** :

| Symptôme | Cause probable |
|---|---|
| Les scores CV sont un peu meilleurs que le test final | Fuite (prétraitement fitté hors Pipeline) ou surapprentissage |
| Scaler ou pas, le boosting donne exactement le même R² | Normal — les arbres sont insensibles à l'échelle |
| La régression linéaire diverge / coefficients énormes | Features non standardisées, échelles très différentes |
| Le scaler « n'a pas d'attribut `mean_` » | `.transform()` appelé avant `.fit()` (ou hors Pipeline) |
| Résultats différents entre notebook et prod | Scaler refitté au lieu d'être rechargé depuis le Pipeline sauvegardé |

## Pour aller plus loin

- Doc officielle — **`StandardScaler`** : <https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html>
- **Comparaison des scalers** (StandardScaler vs MinMax vs Robust) : <https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html>
- **Common pitfalls — data leakage** (scikit-learn) : <https://scikit-learn.org/stable/common_pitfalls.html#data-leakage>
- Source de référence : Aurélien Géron, *ML avec scikit-Learn* (3ᵉ éd.), chap. 2 « Prepare the Data » (feature scaling & pipelines).

## Vérification (checklist apprenant)

- [ ] J'ai fait tourner l'exemple minimal et vu que le scaler stocke `μ` et `σ`
- [ ] Je sais dire **quels modèles** ont besoin du scaler et lesquels non
- [ ] Mon scaler est **dans le `Pipeline`**, jamais appliqué à `X` avant la CV
- [ ] Je peux expliquer à un collègue pourquoi la fuite de prétraitement est
      invisible sur Bike Sharing mais qu'on l'évite quand même par défaut
- [ ] J'ai fait l'exercice guidé (fuite vs propre + scaler sur boosting)