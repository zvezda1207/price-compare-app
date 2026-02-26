from matcher import load_excel, compare, validate_columns
from excel_writer import save_to_excel
import pandas as pd


def run(reference_path, supplier_paths, output_path):

    reference_df = load_excel(reference_path)
    validate_columns(reference_df, reference_path)

    # приведение цены эталона к числу
    reference_df["Цена за штуку"] = pd.to_numeric(
        reference_df["Цена за штуку"],
        errors="coerce"
    )    

    supplier_dfs = []

    for path in supplier_paths:
        df = load_excel(path)
        validate_columns(df, path)

        # приведение цены поставщика к числу
        df["Цена за штуку"] = pd.to_numeric(
            df["Цена за штуку"],
            errors="coerce"
        )

        supplier_dfs.append(df)    

    result_df = compare(reference_df, supplier_dfs)

    save_to_excel(result_df, output_path)


def main():
    run("reference.xlsx", ["supplier1.xlsx", "supplier2.xlsx"])


if __name__ == "__main__":
    main()
