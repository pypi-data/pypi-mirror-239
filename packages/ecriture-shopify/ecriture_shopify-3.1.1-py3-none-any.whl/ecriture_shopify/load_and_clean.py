"""
fonctions pour vérifier la validité du fichier d'entrée avant de charger
"""
# library
import io
from pathlib import Path

from loguru import logger
import pandas as pd

# modules
from ecriture_shopify.tools.exceptions import ShopifyFileEmptyError, ShopifyFormatError


# constantes
# dictionnaire de colonnes à utiliser pour le fichier shopify + leur renommage
DICT_COLS_SHOPIFY = {
    "Référence de commande": "ref_command",
    "Identifiant de vente": "id_vente",
    "Date": "date",
    "Type de transaction": "type_transaction",
    "Pays de facturation": "pays",
    # "Quantité nette": "quantite_nette",
    "Ventes brutes": "ventes_ht",
    # "Réductions": "reductions",
    # "Retours": "retours",
    # "Ventes nettes": "ventes_nettes",
    "Expédition": "expedition_ht",
    # "Taxes": "taxes",
    "Ventes totales": "ventes_ttc"
}


def load_input(input_io: io.BytesIO()) -> pd.DataFrame:
    """fonction pour charger le fichier et en même temps vérifier la validité avec try/except"""

    # on se sert des checks de read_excel() pour optimiser check & load
    try:
        df_0 = pd.read_excel(
            io=input_io, header=1, usecols=DICT_COLS_SHOPIFY.keys(), parse_dates=["Date"]
        )
        # on check aussi si le df est vide car, contrairement à read_csv, read_excel ne remonte pas
        # d'erreur 'pd.errors.EmptyDataError'...
        if df_0.empty:
            error_msg = "ShopifyFileEmptyError : le fichier est vide"
            logger.error(error_msg)
            raise ShopifyFileEmptyError(error_msg)
        else:
            return df_0

    except ValueError:
        error_msg = "ValueError : le fichier n'est pas conforme au format attendu"
        logger.error(error_msg)
        raise ShopifyFormatError(error_msg)


def clean_df(df_0: pd.DataFrame) -> pd.DataFrame:
    """clean df avant son utilisation"""

    # on essaye de cleaner le fichier
    try:
        df_1 = df_0.copy()
        df_1 = df_1.rename(columns=DICT_COLS_SHOPIFY)
        df_1 = df_1.dropna(axis=0, how="all")
        df_1["date"] = df_1["date"].dt.strftime("%d/%m/%Y")

        return df_1

    # si ça ne fonctionne pas, c'est que le format a un souci
    except KeyError:
        error_msg = "KeyError : le fichier n'est pas conforme au format attendu"
        logger.error(error_msg)
        raise ShopifyFormatError(error_msg)


# composition de fonctions
def load_and_clean(path_xlsx: Path) -> pd.DataFrame:
    """function to compose the try, load and clean functions"""

    df_1 = load_input(path_xlsx)
    df_2 = clean_df(df_1)

    return df_2


# end
