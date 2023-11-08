# Copyright: (c) 2023, Michel Padovani <michel.padovani@outlook.com>
# GNU General Public License v3.0 only (see LICENSE or <https://www.gnu.org/licenses/gpl-3.0.txt>)

# library
import io
from pathlib import Path

from loguru import logger
import pandas as pd

# modules
from ecriture_shopify.core_ecriture_comptable import create_dfs_ec
from ecriture_shopify.create_xlsx import generate_xlsx_io
from ecriture_shopify.load_and_clean import load_and_clean
from ecriture_shopify.tools.read_config import get_config_json


# configuration lib
pd.options.mode.copy_on_write = True


# config
ROOT_PATH = Path(__file__).resolve().parent.parent
CONFIG_JSON_PATH = ROOT_PATH / "ecriture_shopify" / "config" / "config_pays_tva.json"

# config qui associe un pays à une tva
DICT_PAYS_TVA = get_config_json(CONFIG_JSON_PATH)["PAYS_TVA"]


# fonction coeur
def shopify_to_ec(input_io: io.BytesIO(), dict_pays_tva: dict = DICT_PAYS_TVA) -> io.BytesIO():
    """Fonction principale de 'ecriture_shopify' qui encapsule le pipeline complet.
       Génération d'une écriture comptable à partir d'un extrait mensuel xlsx de Shopify.
       Si une tva est fournie pour un pays, elle sera appliquée."""

    # start log
    logger.info("Une nouvelle génération Shopify est lancée")

    # load & clean in df if ok. else raise error
    df_ventes = load_and_clean(input_io)

    # ecriture comptable in df.
    df_ecriture, df_pays_bilan = create_dfs_ec(df_ventes, dict_pays_tva)

    # on génère l'écriture comptable en xlsx_io.
    xlsx_io = generate_xlsx_io(df_ecriture, df_pays_bilan)
    logger.success("Fin de la génération Shopify")

    return xlsx_io


# end
