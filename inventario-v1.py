import requests
from collections import defaultdict

# Lista das URLs do Kafka Connect
kafka_connect_urls = [
    "http://kafka-connect-url-1:8083",
    "http://kafka-connect-url-2:8083",
    "http://kafka-connect-url-3:8083",
    "http://kafka-connect-url-4:8083",
    "http://kafka-connect-url-5:8083",
]

def fetch_connectors(url):
    """Função para obter a lista de conectores de uma URL do Kafka Connect."""
    try:
        response = requests.get(f"{url}/connectors")
        response.raise_for_status()
        connectors = response.json()
        return connectors
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return []

def fetch_connector_details(url, connector_name):
    """Função para obter os detalhes de um conector específico."""
    try:
        response = requests.get(f"{url}/connectors/{connector_name}")
        response.raise_for_status()
        connector_details = response.json()
        return connector_details
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter detalhes do conector {connector_name} em {url}: {e}")
        return {}

def classify_connectors_by_type(url, connectors):
    """Função para classificar conectores por tipo."""
    connector_types = defaultdict(int)

    for connector in connectors:
        details = fetch_connector_details(url, connector)
        connector_class = details.get("config", {}).get("connector.class", "Desconhecido")

        # Classifica por tipo (Postgres, Mongo, etc.)
        if "Postgres" in connector_class:
            connector_types["Postgres"] += 1
        elif "Mongo" in connector_class:
            connector_types["Mongo"] += 1
        elif "Dynamo" in connector_class:
            connector_types["Dynamo"] += 1
        elif "SQLServer" in connector_class:
            connector_types["SQLServer"] += 1
        else:
            connector_types["Outros"] += 1

    return connector_types

def main():
    total_connectors = {}
    type_summary = defaultdict(int)
    global_total_connectors = 0  # Variável para contar o total geral de conectores

    for url in kafka_connect_urls:
        print(f"\nConsultando Kafka Connect em: {url}")
        connectors = fetch_connectors(url)

        if connectors:
            num_connectors = len(connectors)
            print(f"Total de conectores encontrados em {url}: {num_connectors}")
            total_connectors[url] = num_connectors
            global_total_connectors += num_connectors  # Soma ao total geral

            # Classifica os conectores por tipo
            connector_types = classify_connectors_by_type(url, connectors)
            for connector_type, count in connector_types.items():
                type_summary[connector_type] += count
                print(f"  Tipo {connector_type}: {count}")
        else:
            print(f"Nenhum conector encontrado em {url}.")

    print("\nResumo Geral:")
    print("Total de conectores por URL:")
    for url, count in total_connectors.items():
        print(f"  {url}: {count}")
    print(f"Total geral de conectores: {global_total_connectors}")
    print("Total de conectores por tipo:")
    for connector_type, count in type_summary.items():
        print(f"  {connector_type}: {count}")

if __name__ == "__main__":
    main()
