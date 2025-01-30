from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# Configurando o serviço do ChromeDriver
service = Service(executable_path='../driver/chromedriver.exe')  # Substitua pelo caminho do seu chromedriver

# Inicializando o driver
driver = webdriver.Chrome(service=service)

try:
    # Passo 1: Acessar a Página Inicial
    driver.get("https://almsantana.github.io/")
    assert "Index - AcordeLab" in driver.title  # Verifica se a página carregou corretamente

    # Passo 2: Localizar o Formulário de Login
    form_login = driver.find_element(By.ID, "formulario_login")
    assert form_login is not None  # Confirma se o formulário de login está presente

    # Passo 3: Inserir Credenciais Válidas
    email_input = driver.find_element(By.NAME, "email")
    senha_input = driver.find_element(By.NAME, "senha")
    email_input.send_keys("email@acordelab.com.br")
    senha_input.send_keys("123senha")

    # Passo 4: Submeter o Formulário de Login
    botao_login = driver.find_element(By.CLASS_NAME, "botao-login")
    botao_login.click()

    time.sleep(3)  # Pausa de 3 segundos para garantir o carregamento da próxima página

    # Passo 5: Verificar Redirecionamento
    assert "home.html" in driver.current_url  # Verifica se a página de redirecionamento está correta

    # Passo 6: Verificar Acesso ao Conteúdo
    cursos_card = driver.find_elements(By.CLASS_NAME, "course-card")
    assert len(cursos_card) > 0  # Confirma que Ana tem acesso ao conteúdo dos cursos

finally:
    time.sleep(3)  # Pausa de 3 segundos antes de fechar
    driver.quit()  # Encerra o navegador
