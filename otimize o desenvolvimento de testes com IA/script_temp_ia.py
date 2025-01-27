from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configuração do WebDriver
driver = webdriver.Chrome()

try:
    # Cenário 1: Login bem-sucedido com credenciais corretas
    driver.get("https://almsantana.github.io/")
    driver.find_element(By.NAME, "email").send_keys("email@acordelab.com.br")
    driver.find_element(By.NAME, "senha").send_keys("123senha")
    driver.find_element(By.CLASS_NAME, "botao-login").click()
    time.sleep(2)  # Aguardar o carregamento da página
    assert "Página Inicial" in driver.title
    print("Cenário 1: Login realizado com sucesso!")

    # Voltar para a tela de login
    driver.get("https://almsantana.github.io/")

    # Cenário 2: Login com e-mail incorreto
    driver.find_element(By.NAME, "email").send_keys("wrong_email@example.com")
    driver.find_element(By.NAME, "senha").send_keys("senha123")
    driver.find_element(By.NAME, "entrar").click()
    time.sleep(2)  # Aguardar o carregamento da página
    error_message = driver.find_element(By.CLASS_NAME, "error-message").text
    assert "credenciais estão incorretas" in error_message
    print("Cenário 2: Mensagem de erro exibida para e-mail incorreto.")

    # Voltar para a tela de login
    driver.get("URL_DO_APP_ACORDELAB")

    # Cenário 3: Login com senha incorreta
    driver.find_element(By.NAME, "email").send_keys("ana@example.com")
    driver.find_element(By.NAME, "senha").send_keys("wrong_password")
    driver.find_element(By.NAME, "entrar").click()
    time.sleep(2)  # Aguardar o carregamento da página
    error_message = driver.find_element(By.CLASS_NAME, "error-message").text
    assert "credenciais estão incorretas" in error_message
    print("Cenário 3: Mensagem de erro exibida para senha incorreta.")

    # Voltar para a tela de login
    driver.get("URL_DO_APP_ACORDELAB")

    # Cenário 4: Login com campos vazios
    driver.find_element(By.NAME, "email").send_keys("")
    driver.find_element(By.NAME, "senha").send_keys("")
    driver.find_element(By.NAME, "entrar").click()
    time.sleep(2)  # Aguardar o carregamento da página
    error_message = driver.find_element(By.CLASS_NAME, "error-message").text
    assert "não podem estar vazios" in error_message
    print("Cenário 4: Mensagem de erro exibida para campos vazios.")

    # Cenário 5: Redefinição de senha
    driver.get("URL_DO_APP_ACORDELAB")
    driver.find_element(By.NAME, "email").send_keys("wrong_email@example.com")
    driver.find_element(By.NAME, "senha").send_keys("wrong_password")
    driver.find_element(By.NAME, "entrar").click()
    time.sleep(2)  # Aguardar o carregamento da página
    driver.find_element(By.LINK_TEXT, "Esqueci minha senha").click()
    time.sleep(2)  # Aguardar o carregamento da página
    driver.find_element(By.NAME, "email").send_keys("ana@example.com")
    driver.find_element(By.NAME, "enviar").click()
    time.sleep(2)  # Aguardar o carregamento da página
    success_message = driver.find_element(By.CLASS_NAME, "success-message").text
    assert "link de redefinição de senha foi enviado" in success_message
    print("Cenário 5: Mensagem de sucesso para redefinição de senha exibida.")

finally:
    # Pausa de 3 segundos antes de fechar o navegador
    time.sleep(3)
    # Fechar o navegador
    driver.quit()