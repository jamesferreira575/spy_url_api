import re #re é usada para fazer correspondências de padrões e encontrar links que correspondam a determinados padrões,
# como extensões de arquivos ou palavras-chave.
import requests # requests é uma biblioteca em Python usada para enviar solicitações HTTP.
# Ele fornece uma interface simples e conveniente para fazer solicitações HTTP.
from bs4 import BeautifulSoup #A biblioteca BeautifulSoup é usada para analisar e extrair dados de documentos HTML e XML.
# Ela fornece uma maneira fácil de navegar e buscar por elementos em um código HTML/XML.
# No código, o BeautifulSoup é usado para criar um objeto BeautifulSoup a partir do código HTML obtido com o requests,
# permitindo que você procure por elementos específicos, como links, usando métodos e seletores específicos do BeautifulSoup.


print("""

███████╗██████╗ ██╗   ██╗    ██╗   ██╗██████╗ ██╗     
██╔════╝██╔══██╗╚██╗ ██╔╝    ██║   ██║██╔══██╗██║     
███████╗██████╔╝ ╚████╔╝     ██║   ██║██████╔╝██║     
╚════██║██╔═══╝   ╚██╔╝      ██║   ██║██╔══██╗██║     
███████║██║        ██║       ╚██████╔╝██║  ██║███████╗
╚══════╝╚═╝        ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚══════╝
                                                      
 █████╗ ██████╗ ██╗                                   
██╔══██╗██╔══██╗██║                                   
███████║██████╔╝██║                                   
██╔══██║██╔═══╝ ██║                                   
██║  ██║██║     ██║                                   
╚═╝  ╚═╝╚═╝     ╚═╝                                   
                                                                             
                                                      
By: https://www.darede.com.br/
Red-Team darede.

""")


# Função para extrair links de uma página com base em uma expressão regular
def extract_links(url, regex_pattern):
    response = requests.get(url)  # Faz uma solicitação HTTP para obter o código HTML da página
    soup = BeautifulSoup(response.text, 'html.parser')  # Cria um objeto BeautifulSoup para analisar o HTML
    links = soup.find_all(href=re.compile(regex_pattern))  # Encontra todos os links que correspondem ao padrão de expressão regular
    return [link.get('href') for link in links]  # Retorna apenas os atributos 'href' dos links encontrados

# Função para processar os links, removendo caracteres indesejados e removendo duplicatas
def process_links(links):
    processed_links = set()  # Usamos um conjunto para evitar duplicatas
    for link in links:
        link = link.replace("></script>", "").replace('"', "").replace(",", "").replace("'", "")  # Remove caracteres indesejados
        processed_links.add(link)  # Adiciona o link processado ao conjunto
    return processed_links

# Função principal para realizar a varredura dos links
def scan(url):
    # Extração e processamento dos links com extensão .js, .json e /wp
    js_links = extract_links(url, r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:\.js(?:\?\S+)?)?')
    json_links = extract_links(url, r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:\.json(?:\?\S+)?)?')
    wp_links = extract_links(url, r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:/wp(?:\?\S+)?)?')

    # Processamento dos links para remover duplicatas e caracteres indesejados
    full_js_links = process_links(js_links)
    full_json_links = process_links(json_links)
    full_wp_links = process_links(wp_links)

    # Impressão dos links encontrados
    print('★ JS links found:')
    for js_link in full_js_links:
        print(js_link)

    print('\n★ JS links with API word found:')
    for js_link in full_js_links:
        response = requests.get(js_link)
        js_code = response.text
        if not re.search('404', js_code) and re.search('api', js_code):
            print(js_link)

    print('\n★ Found JSON links:')
    for json_link in full_json_links:
        print(json_link)

    print('\n★ Found JSON links with the word API:')
    for json_link in full_json_links:
        response = requests.get(json_link)
        json_code = response.text
        if not re.search('404', json_code) and re.search('api', json_code):
            print(json_link)

    print('\n★ Found WP Links:')
    for wp_link in full_wp_links:
        print(wp_link)

# Menu para escolher a opção de varredura
print("""Choose a scan option:
★ 1 - Scan a single URL
★ 2 - Scan multiple URLs contained in a domains.txt file\n""")

option = int(input("★ Enter the desired option: "))

if option == 1:
    url = input("Enter the URL to be scanned: ")
    print("\n=-=-=-=-=-=-=-=-=-=-=-=-")
    print(f"★ Scanning URL: {url}\n")
    scan(url)

elif option == 2:
    with open('domains.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        url = line.strip()
        print("\n=-=-=-=-=-=-=-=-=-=-=-=-")
        print(f"★ Scanning URL: {url}")
        scan(url)
