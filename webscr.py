import requests
from bs4 import BeautifulSoup as bs

# Solicita o nome do usuário do GitHub como entrada
nome_usuario = input("Digite o nome de usuário do GitHub: ").strip()

# URL do perfil do GitHub
url = f"https://github.com/{nome_usuario}"

# Envia uma solicitação HTTP GET para a página do perfil
response = requests.get(url)

# Verifica se a solicitação foi bem-sucedida (código de resposta 200)
if response.status_code == 200:
    # Parseia o conteúdo HTML da página (organiza o código da página HTML para ficar mais fácil de ser trabalhada)
    codigo_html = bs(response.text, 'html.parser') # método construtor (retorna um objeto BeautifulSoup). Deixa de ser uma string

    # Encontra o elemento que contém a contagem de repositórios e o link da foto de perfil
    repo_element = codigo_html.find('span', class_='Counter')
    # obs.: para acessar a propriedade 'class' deve ser colocado um '_' depois, pois 'class' é uma palavra reservada no python para a criação de classes.
    
    img = codigo_html.find('img', class_='avatar avatar-user width-full border color-bg-default')
    
    if img:
        print(f"Link da foto de perfil do usuário {nome_usuario}: {img['src']}")
        # os colchetes dizem qual é a propriedade do elemento a ser retornada (caso ele não seja especificado, ele retorna a tag inteira). Eu poderia ter colocado ele no momento da atribuição de 'img'
    else:
        print(f"Não foi possível encontrar a foto de perfil para o usuário {nome_usuario}.")

    # Extrai a contagem de repositórios
    if repo_element:
        repo_count = int(repo_element.get_text().strip())
        # o método 'get_text()' pega o texto dentro do elemento

        print(f"O usuário {nome_usuario} tem {repo_count} repositórios públicos no GitHub.")

        if repo_count >= 1:
        # Acha e printa os nomes dos repos. se possível
            page = 1
            repos_url = f"{url}?page={page}&tab=repositories"
            response = requests.get(repos_url)
            if response.status_code == 200:
                print("São eles:")
                count = 0
                while(True):
                    codigo_html = bs(response.text, 'html.parser')
                    repos_name = codigo_html.find_all('a', {'itemprop': 'name codeRepository'})
                    if len(repos_name) >= 1:
                        for repo in repos_name:
                            count += 1
                            print(f" {count:02}. " + repo.get_text().strip())
                    if count == repo_count:
                        break
                    page += 1
                    repos_url = f"{url}?page={page}&tab=repositories"
                    response = requests.get(repos_url)
                    
            else:
                print("Não foi possível acessar a página com os repositórios.")
    else:
        print(f"Não foi possível encontrar a contagem de repositórios para o usuário {nome_usuario}.")
else:
    print(f"Não foi possível acessar o perfil do usuário {nome_usuario}. Verifique se o nome de usuário está correto ou se o perfil é público.")
