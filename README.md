# find-groups

This program aims to provide visualisation interface from data from poll answerers.
It then focuses on finding groups among the answerers.

Ce programme a pour but de visualiser les informations de répondants à un sondage, dans le but ensuite
de trouver des groupes parmis les répondants.

## Usage

To run in local, use ´streamlit run EDA.py´
To access the streamlit cloud hosted interface, visit [this link]()

To preserve answerers confidentiality, Excel file with answers is not provided. In a future improvement,
a dummy file with 100% non-indentifying information will be provided.

Pour utiliser en local, taper dans la console d'un IDE ´streamlit run EDA.py´
Pour accéder à l'interface hébergée sur le cloud streamlit, visiter [ce lien]()

Afin de préserver la confidentialité des répondants, le fichier Excel avec les réponses n'est pas fourni.
Dans une mise a jour future, un fichier contenant 100% d'information non-identifiantes sera fourni.

## Data pretreatment

* Lowercase everything
* Conversion of type of string variables to category

* Transformation en minuscules
* Conversion des variables textuelles en catégories

### Diploma

Matching between diploma and level (numerical), from 
[this ressource](https://www.enseignementsup-recherche.gouv.fr/fr/nomenclature-relative-au-niveau-de-diplome-45785).

Correspondance entre les diplome et le niveau (numérique), d'après 
[ce lien](https://www.enseignementsup-recherche.gouv.fr/fr/nomenclature-relative-au-niveau-de-diplome-45785).

## EDA

### Correlation

Between more than 2 variables: calculation of correlation using contingency table of Chi2 to obtain statistics,
then calculation of Cramers V and then obtention of a score between 0 (uncorrelated) and 1 (highly correlated).

Entre plus de 2 variable: calcul de la corrélation en utilisant la table de contingence du Chi2 pour obtenir
la statistique, puis calculer le Cramers V et ainsi avoir un score entre 0 (non corrélé) et 1 (fortement corrélé).