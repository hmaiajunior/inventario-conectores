import requests

url = "https://kafkadrop-pd.cb.uat.core.local"  # Mude para o outro URL para testar
try:
    response = requests.get(url, verify=False)  # Ignorando validação SSL
    print("Status Code:", response.status_code)
    print("Response Content:", response.text[:500])  # Mostra um trecho da resposta
except requests.exceptions.RequestException as e:
    print(f"Erro ao conectar com {url}: {e}")
