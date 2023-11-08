# ecriture-shopify

[![Test CI](https://github.com/michelpado/ecriture-shopify/actions/workflows/test_source_code.yml/badge.svg)](https://github.com/michelpado/ecriture-shopify/actions/workflows/test_source_code.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/ecriture-shopify?label=Latest%20release&color=41B3FF)](https://pypi.org/project/ecriture-shopify/)
[![PyPI - License](https://img.shields.io/pypi/l/ecriture-shopify?color=EEEEEE)](https://github.com/michelpado/ecriture-shopify/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ecriture-shopify?color=F67280)](https://pypi.org/project/ecriture-shopify/)


Génère une écriture comptable à partir d'un extrait mensuel de Shopify.<br>

Le coeur du traitement est en Pandas & XlsxWriter, avec l'aide de Loguru pour la partie log.


## Fonctionnement
La fonction principale du package est `shopify_to_ec`. Cette fonction encapsule le pipeline complet pour créer une écriture comptable à partir du fichier xlsx (ou xls) mensuel de Shopify. Le pipeline est composé de 3 étapes majeures:
* chargement, vérification et nettoyage du fichier d'entrée Shopify
* application de la TVA France et génération de l'écriture comptable
* création du fichier de sortie xlsx avec une mise en forme propre

**Explication de la fonction**<br>
`shopify_to_ec` prend en argument le fichier xlsx/xls de Shopify (en io.Bytes pour simplifier les intégrations dans d'autres outils) et le fichier de configuration de la TVA (optionnel) . La fonction génère le fichier d'écriture comptable en xlsx (aussi en io.Bytes).

**input/output en 'type hints':**<br>
```
shopify_to_ec(input_io: io.BytesIO(), dict_pays_tva: dict = DICT_PAYS_TVA) -> io.BytesIO()
```

**Pour importer:**<br>
```python
from ecriture_shopify import shopify_to_ec
```
<br>

Les problèmes pendant la génération déclencheront des exceptions, situé ici: `/ecriture_shopify/tools/exceptions.py`
<br>


## A propos
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Le projet est mené, entres autres, avec Poetry, Black, isort, Pytest et pre-commit.<br> Voir "pyproject.toml" pour la liste comptète.


## Auteur:
michel padovani


## Licence
License "GNU General Public License v3.0 only".<br>
Voir [LICENSE](https://github.com/michelpado/ecriture-shopify/blob/master/LICENSE)
