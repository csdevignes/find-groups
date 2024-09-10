# find-groups

This program aims to provide visualisation interface from data from poll answerers.
It then focuses on finding groups among the answerers.

Ce programme a pour but de visualiser les informations de répondants à un sondage, dans le but ensuite
de trouver des groupes parmis les répondants.

-- English version --

## Usage

To run in local, use ´streamlit run EDA.py´
To access the streamlit cloud hosted interface, visit [this link](https://find-groups-eda.streamlit.app/)

To preserve answerers confidentiality, Excel file with answers is not provided.

## Anonymisation and dummy file creation

The original data used for the project was anonymized, and a dummy file containing random answers was created.
To repeat these steps using different source data, the following scripts can be used.

### Anonymisation

`python anonymisation.py <path to excel file.xlsx>`

The name of the column to anonymize will be asked. So far only one column can be anonymized.

Anonymized excel files include index column as first column, as this is expected by all the other scripts in this project.

### Dummy file creation

`python dummy_file.py <path to anonymized excel file.xlsx>`

## Data pretreatment

* Lowercase everything
* Conversion of type of string variables to category
* For downstream clustering algorithms only : encode_all() method uses OrdinalEncoding

### Diploma

Matching between diploma and level (numerical), from 
[this ressource](https://www.enseignementsup-recherche.gouv.fr/fr/nomenclature-relative-au-niveau-de-diplome-45785).

## EDA

### Correlation

Between more than 2 variables: calculation of correlation using contingency table of Chi2 to obtain statistics,
then calculation of Cramers V and then obtention of a score between 0 (uncorrelated) and 1 (highly correlated).

## Ongoing Improvements

* Clustering: Optimize hyperparameters (iteration, initialisation, stop condition)
* Streamlit cloud : persistence of dataframe, warning error
* Create dummy excel file with random poll answers
* Anonymization : allow to pick several columns

-- French version --

## Utilisation

Pour utiliser en local, taper dans la console d'un IDE ´streamlit run EDA.py´
Pour accéder à l'interface hébergée sur le cloud streamlit, visiter [ce lien](https://find-groups-eda.streamlit.app/)

Afin de préserver la confidentialité des répondants, le fichier Excel avec les réponses n'est pas fourni.
Dans une mise a jour future, un fichier contenant 100% d'information non-identifiantes sera fourni.

## Prétraitement des données

* Transformation en minuscules
* Conversion des variables textuelles en catégories
* Uniquement pour l'utilisation des algorithms de clustering : la méthode encode_all() utilise OrdinalEncoding

### Diploma

Correspondance entre les diplome et le niveau (numérique), d'après 
[ce lien](https://www.enseignementsup-recherche.gouv.fr/fr/nomenclature-relative-au-niveau-de-diplome-45785).

## EDA

### Correlation

Entre plus de 2 variable: calcul de la corrélation en utilisant la table de contingence du Chi2 pour obtenir
la statistique, puis calculer le Cramers V et ainsi avoir un score entre 0 (non corrélé) et 1 (fortement corrélé).

