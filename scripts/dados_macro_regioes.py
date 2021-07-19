import csv
import json
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen
import os
from dotenv import load_dotenv, find_dotenv

# lendo o arquivo .env para obter a key
load_dotenv(find_dotenv())
api_key = os.getenv("my_API_key")


class BrasilIO:

    base_url = "https://api.brasil.io/v1/"

    def __init__(self, auth_token):
        self.__auth_token = auth_token

    @property
    def headers(self):
        return {
            "User-Agent": "python-urllib/brasilio-client-0.1.0",
        }

    @property
    def api_headers(self):
        data = self.headers
        data.update({"Authorization": f"Token {self.__auth_token}"})
        return data

    def api_request(self, path, query_string=None):
        url = urljoin(self.base_url, path)
        if query_string:
            url += "?" + urlencode(query_string)
        request = Request(url, headers=self.api_headers)
        response = urlopen(request)
        return json.load(response)

    def data(self, dataset_slug, table_name, filters=None):
        url = f"dataset/{dataset_slug}/{table_name}/data/"
        filters = filters or {}
        filters["page"] = 1

        finished = False
        while not finished:
            response = self.api_request(url, filters)
            next_page = response.get("next", None)
            for row in response["results"]:
                yield row
            filters = {}
            url = next_page
            finished = next_page is None

    def download(self, dataset, table_name):
        url = f"https://data.brasil.io/dataset/{dataset}/{table_name}.csv.gz"
        request = Request(url, headers=self.headers)
        response = urlopen(request)
        return response


if __name__ == "__main__":
    api = BrasilIO(api_key)
    dataset_slug = "covid19"
    table_name = "caso_full"

    # Para navegar pela API:
    # criando o dataset para as  cidades de redenção, Acarape e São Francisco do Conde
    # pegando os dados das cidades do Ceará
    # criando o dataset para as  cidades de redenção, Acarape e São Francisco do Conde
    with open(
        "data/df_dados_macro_regioes.csv", "w", newline="", encoding="utf-8"
    ) as csvDadosAcumulados:
        dadosAcumulados = csv.writer(csvDadosAcumulados)
        dadosAcumulados.writerow(
            [
                "city",
                "city_ibge_code",
                "date",
                "last_available_confirmed",
                "last_available_confirmed_per_100k_inhabitants",
                "last_available_deaths_per_100k_inhabitants",
                "estimated_population_2019",
                "last_available_deaths",
                "state",
                "new_confirmed",
                "new_deaths",
            ]
        )

        codigosIBG_CE = [
            2309458,
            2301950,
            2300150,
            2301406,
            2304954,
            2307650,
            2307700,
            2309706,
            2310100,
            2311603,
            2310100,
            2301208,
            2302107,
            2305100,
            2309805,
            2302909,
            2309102,
            2306504,
            2301000,
            2304285,
            2304400,
            2306256,
            2303709,
            2306306,
            2300903,
            2304608,
            2310209,
            2310258,
            2312403,
            2312601,
            2313351,
        ]

        codigosIBG_BA = [
            2906501,
            2916104,
            2919207,
            2919926,
            2927408,
            2928604,
            2929206,
            2929503,
            2929750,
        ]

        # pegando os dados acumulados das cidades do Ceará
        filters_CE_acumulados = {"state": "CE", "is_last": True}
        data_CE_acumlados = api.data(dataset_slug, table_name, filters_CE_acumulados)
        for row in data_CE_acumlados:
            for cod in codigosIBG_CE:
                if row["city_ibge_code"] == cod:
                    city = row["city"]
                    city_ibge_code = row["city_ibge_code"]
                    date = row["date"]
                    last_available_confirmed = row["last_available_confirmed"]
                    last_available_confirmed_per_100k_inhabitants = row[
                        "last_available_confirmed_per_100k_inhabitants"
                    ]
                    estimated_population_2019 = row["estimated_population_2019"]
                    last_available_deaths = row["last_available_deaths"]
                    state = row["state"]
                    new_confirmed = row["new_confirmed"]
                    new_deaths = row["new_deaths"]
                    last_available_deaths_per_100k_inhabitants = round(
                        (last_available_deaths / estimated_population_2019 * 100000), 4
                    )
                    dadosAcumulados.writerow(
                        [
                            city,
                            city_ibge_code,
                            date,
                            last_available_confirmed,
                            last_available_confirmed_per_100k_inhabitants,
                            last_available_deaths_per_100k_inhabitants,
                            estimated_population_2019,
                            last_available_deaths,
                            state,
                            new_confirmed,
                            new_deaths,
                        ]
                    )

        # pegando os dados acumulados das cidades da Bahia
        filters_Baiha = {"state": "BA", "is_last": True}
        data_BA = api.data(dataset_slug, table_name, filters_Baiha)
        for row in data_BA:
            for cod in codigosIBG_BA:
                if row["city_ibge_code"] == cod:
                    city = row["city"]
                    city_ibge_code = row["city_ibge_code"]
                    date = row["date"]
                    last_available_confirmed = row["last_available_confirmed"]
                    last_available_confirmed_per_100k_inhabitants = row[
                        "last_available_confirmed_per_100k_inhabitants"
                    ]
                    estimated_population_2019 = row["estimated_population_2019"]
                    last_available_deaths = row["last_available_deaths"]
                    state = row["state"]
                    new_confirmed = row["new_confirmed"]
                    new_deaths = row["new_deaths"]
                    last_available_deaths_per_100k_inhabitants = round(
                        (last_available_deaths / estimated_population_2019 * 100000), 4
                    )
                    dadosAcumulados.writerow(
                        [
                            city,
                            city_ibge_code,
                            date,
                            last_available_confirmed,
                            last_available_confirmed_per_100k_inhabitants,
                            last_available_deaths_per_100k_inhabitants,
                            estimated_population_2019,
                            last_available_deaths,
                            state,
                            new_confirmed,
                            new_deaths,
                        ]
                    )
