"""
fichier regroupant les fonctions pour le fichier de sortie xlsx
"""

# library
import io

import pandas as pd
from pandas.io.formats import excel as pd_excel


# dict pour definir les différents formats utilisés
dict_formats = {
    "money_fmt": {"num_format": "### ### ###0.00 €", "align": "center", "valign": "vcenter"},
    "prct_fmt": {"num_format": "0.00%", "align": "center", "valign": "vcenter"},
    "cntr_fmt": {"align": "center", "valign": "vcenter"},
    "ref_fmt": {"num_format": "0000000000000", "align": "center", "valign": "vcenter"},
    "entete_bleu": {
        "bold": True,
        "font_color": "#F6F1F1",
        "fg_color": "#19A7CE",
        "border": 1,
        "border_color": "#F6F1F1",
        "align": "center",
        "valign": "vcenter",
    },
    "entete_orange": {
        "bold": True,
        "font_color": "#FAFAFA",
        "fg_color": "#FF8080",
        "border": 1,
        "border_color": "#F6F1F1",
        "align": "center",
        "valign": "vcenter",
    },
    "bold_fmt": {"bold": True, "align": "center", "valign": "vcenter"},
}


def xlsx_header_format(df_0, h_fmt, wkst):
    """fonction pour appliquer facilement le format sur le header du tableau
    (adaptation de row et de index_title dans le projet emprunt)
    """
    list_col = df_0.columns

    for col_num, data in enumerate(list_col):
        wkst.write(0, col_num, data, h_fmt)


def generate_xlsx_io(df_data: pd.DataFrame, df_groupby: pd.DataFrame) -> io.BytesIO():
    """function to compose the xlsx_generation functions"""
    # on enregistre dans un buffer_io pour simplifier la modification xlsxwrite/pandas
    xlsx_io = io.BytesIO()

    # génération d'un xlsx à partir d'un df classique
    with pd.ExcelWriter(xlsx_io, engine="xlsxwriter") as writer:
        # to remove index and header formatting from pandas
        pd_excel.ExcelFormatter.header_style = None

        # to write df_x in worksheet
        df_data.to_excel(writer, sheet_name="données", index=False)
        df_groupby.to_excel(writer, sheet_name="bilan_par_pays", index=False)

        # format init
        workbook = writer.book

        # format parameters aplication
        dict_added_format = {}
        for key, fmt in dict_formats.items():
            dict_added_format[key] = workbook.add_format(fmt)

        # parameters
        col_size_classic = 18

        # modifiying formats
        worksheet_data = writer.sheets["données"]
        worksheet_data.set_column("A:J", col_size_classic, dict_added_format["cntr_fmt"])
        worksheet_data.set_column("F:F", col_size_classic, dict_added_format["ref_fmt"])
        worksheet_data.set_column("G:G", 31, dict_added_format["cntr_fmt"])
        worksheet_data.set_column("H:I", col_size_classic, dict_added_format["money_fmt"])
        worksheet_data.set_row(0, 21)
        # xlsx_header_format(df_data, bold_fmt, worksheet_data)
        xlsx_header_format(df_data, dict_added_format["entete_orange"], worksheet_data)

        worksheet_bilan = writer.sheets["bilan_par_pays"]
        worksheet_bilan.set_column("A:A", col_size_classic, dict_added_format["cntr_fmt"])
        worksheet_bilan.set_column("B:B", col_size_classic, dict_added_format["money_fmt"])
        worksheet_bilan.set_column("C:C", col_size_classic, dict_added_format["prct_fmt"])
        worksheet_bilan.set_row(0, 21)
        xlsx_header_format(df_groupby, dict_added_format["entete_bleu"], worksheet_bilan)

    return xlsx_io


# end
