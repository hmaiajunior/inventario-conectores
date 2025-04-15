def classify_connectors_by_name(connectors):
    """Função para classificar conectores por tipo com base no nome."""
    connector_types = defaultdict(int)

    for connector in connectors:
        # Classifica por tipo com base no nome do conector
        if "postgres" in connector.lower():
            connector_types["Postgres"] += 1
        elif "mongo" in connector.lower():
            connector_types["Mongo"] += 1
        elif "dynamo" in connector.lower():
            connector_types["Dynamo"] += 1
        elif "sqlserver" in connector.lower():
            connector_types["SQLServer"] += 1
        else:
            connector_types["Outros"] += 1

    return 