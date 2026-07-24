"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    import pandas as pd
    import glob
    import os

    input_path = "files/input/*.csv.zip"
    output_path = "files/output/"

    os.makedirs(output_path, exist_ok=True)


    # Leer archivos comprimidos directamente
    files = glob.glob(input_path)

    data = pd.concat(
        (
            pd.read_csv(file, compression="zip")
            for file in files
        ),
        ignore_index=True
    )


    # Eliminar columna de índice si existe
    data.drop(
        columns=["Unnamed: 0"],
        errors="ignore",
        inplace=True
    )


    # ==========================
    # CLIENT
    # ==========================

    client = data[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage"
        ]
    ].copy()


    client["job"] = (
        client["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )


    client["education"] = (
        client["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )


    client["credit_default"] = (
        client["credit_default"]
        .eq("yes")
        .astype("int8")
    )


    client["mortgage"] = (
        client["mortgage"]
        .eq("yes")
        .astype("int8")
    )


    client.to_csv(
        output_path + "client.csv",
        index=False
    )


    # ==========================
    # CAMPAIGN
    # ==========================

    campaign = data[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "day",
            "month"
        ]
    ].copy()


    campaign["previous_outcome"] = (
        campaign["previous_outcome"]
        .eq("success")
        .astype("int8")
    )


    campaign["campaign_outcome"] = (
        campaign["campaign_outcome"]
        .eq("yes")
        .astype("int8")
    )


    months = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12"
    }


    campaign["last_contact_date"] = pd.to_datetime(
        "2022-"
        + campaign["month"].map(months)
        + "-"
        + campaign["day"].astype(str)
    )


    campaign.drop(
        columns=["day", "month"],
        inplace=True
    )


    campaign.to_csv(
        output_path + "campaign.csv",
        index=False
    )


    # ==========================
    # ECONOMICS
    # ==========================

    economics = data[
        [
            "client_id",
            "cons_price_idx",
            "euribor_three_months"
        ]
    ].copy()


    economics.to_csv(
        output_path + "economics.csv",
        index=False
    )


    return


if __name__ == "__main__":
    clean_campaign_data()
