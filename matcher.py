import pandas as pd
from utils import normalize


def load_excel(path):
    return pd.read_excel(path)


def words_match(ref_norm, supp_norm):
    ref_words = set(ref_norm.split())
    supp_words = set(supp_norm.split())
    return ref_words.issubset(supp_words)


def find_price(ref_norm, ref_article, supplier_data):
    article_dict = supplier_data["article_dict"]
    name_dict = supplier_data["name_dict"]

    # поиск по артикулу
    if not pd.isna(ref_article):
        supplier_row = article_dict.get(str(ref_article))
        if supplier_row is not None:
            return supplier_row.get("Цена за штуку")

    # поиск по имени
    for supp_norm, supp_row in name_dict.items():
        if words_match(ref_norm, supp_norm):
            return supp_row.get("Цена за штуку")

    return None


def compare(reference_df, supplier_dfs):
    result_rows = []

    supplier_structures = []
    # Подготовка словарей для каждого поставщика
    for supplier_df in supplier_dfs:

        article_dict = {}
        name_dict = {}

        for _, row in supplier_df.iterrows():
            article = row["Артикул"]
            name = row["Наименование"]

            if not pd.isna(article):
                article_dict[str(article)] = row

            normalized_name = normalize(name)
            name_dict[normalized_name] = row

        supplier_structures.append(
            {"article_dict": article_dict, "name_dict": name_dict}
        )

    # Теперь сравнение
    for _, ref_row in reference_df.iterrows():
        ref_name = ref_row["Наименование"]        
        ref_price = ref_row["Цена за штуку"]
        ref_article = ref_row["Артикул"]

        ref_norm = normalize(ref_name)

        result_row = {"Наименование": ref_name, "Эталон цена": ref_price}

        # По каждому поставщику
        for i, supplier_data in enumerate(supplier_structures):
            matched_price = find_price(ref_norm, ref_article, supplier_data)
            result_row[f"Поставщик {i+1}"] = matched_price

        result_rows.append(result_row)

    return pd.DataFrame(result_rows)


def validate_columns(df, file_name):

    if df.empty:
        raise ValueError(f"Файл '{file_name}' не содержит данных")

    required = {"Наименование", "Цена за штуку", "Артикул"}

    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"В файле '{file_name}' отсутствуют столбцы: {', '.join(missing)}"
        )
