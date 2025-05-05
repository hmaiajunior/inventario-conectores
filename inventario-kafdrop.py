import requests

# Nome do arquivo contendo os endereços Kafdrop
FILE_NAME = "kafdrop"

# Função para carregar os endereços do arquivo
def load_kafdrop_addresses(file_name):
    try:
        with open(file_name, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_name}' não encontrado.")
        return []

# Função para obter informações de um Kafdrop ignorando a validação do certificado
def get_kafdrop_info(url):
    try:
        response = requests.get(f"{url}/api/kafka", verify=False)  # Ignorando certificado SSL
        if response.status_code == 200:
            data = response.json()
            return data.get("totalTopics", 0), data.get("totalPartitions", 0)
        else:
            print(f"Erro ao acessar {url}: HTTP {response.status_code}")
            return 0, 0
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com {url}: {e}")
        return 0, 0

# Executando o script
addresses = load_kafdrop_addresses(FILE_NAME)

if not addresses:
    print("Nenhum endereço encontrado no arquivo. Verifique o arquivo 'kafdrop'.")
else:
    total_topics = 0
    total_partitions = 0

    print("\n📊 **Relatório Kafdrop:**")
    print("-" * 40)

    for address in addresses[:5]:  # Apenas os 5 primeiros endereços
        topics, partitions = get_kafdrop_info(address)
        print(f"🔗 {address}")
        print(f"  ➤ Total Topics: {topics}")
        print(f"  ➤ Total Partitions: {partitions}\n")

        total_topics += topics
        total_partitions += partitions

    print("-" * 40)
    print(f"📢 **Total Geral:**")
    print(f"  ✅ Tópicos: {total_topics}")
    print(f"  ✅ Partições: {total_partitions}")
