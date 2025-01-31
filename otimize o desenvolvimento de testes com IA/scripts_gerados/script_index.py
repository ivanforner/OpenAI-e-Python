from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# Configuração do WebDriver
chrome_options = Options()
driver_service = Service('../driver/chromedriver.exe')  # Substitua pelo caminho para o ChromeDriver
driver = webdriver.Chrome(service=driver_service)

# Lista de casos de teste
test_cases = [
    {
        "id": "TC_001",
        "description": "Login with valid credentials",
        "steps": [
            {"action": "navigate", "target": "https://almsantana.github.io/"},
            {"action": "input_text", "target": "input#email", "value": "email@acordelab.com.br"},
            {"action": "input_text", "target": "input#senha", "value": "123senha"},
            {"action": "click", "target": "input.botao-login"},
            {"action": "verify_not_present", "target": ".mensagem-erro"},
            {"action": "verify_url", "value": "file:///caminho/para/home.html"},
            {"action": "verify_presence", "target": ".course-grid"}
        ],
        "expected_result": "Aprovado"
    },
    {
        "id": "TC_002",
        "description": "Login with invalid email",
        "steps": [
            {"action": "navigate", "target": "https://almsantana.github.io/"},
            {"action": "input_text", "target": "input#email", "value": "wrong_email@acordelab.com.br"},
            {"action": "input_text", "target": "input#senha", "value": "123senha"},
            {"action": "click", "target": "input.botao-login"},
            {"action": "verify_present", "target": ".mensagem-erro"}
        ],
        "expected_result": "Reprovado"
    },
    {
        "id": "TC_003",
        "description": "Login with invalid password",
        "steps": [
            {"action": "navigate", "target": "https://almsantana.github.io/"},
            {"action": "input_text", "target": "input#email", "value": "email@acordelab.com.br"},
            {"action": "input_text", "target": "input#senha", "value": "wrong_password"},
            {"action": "click", "target": "input.botao-login"},
            {"action": "verify_present", "target": ".mensagem-erro"}
        ],
        "expected_result": "Reprovado"
    },
    {
        "id": "TC_004",
        "description": "Login with blank credentials",
        "steps": [
            {"action": "navigate", "target": "https://almsantana.github.io/"},
            {"action": "input_text", "target": "input#email", "value": ""},
            {"action": "input_text", "target": "input#senha", "value": ""},
            {"action": "click", "target": "input.botao-login"},
            {"action": "verify_present", "target": ".mensagem-erro"}
        ],
        "expected_result": "Reprovado"
    }
]

# Função para executar passos do caso de teste
def execute_step(step):
    if step["action"] == "navigate":
        driver.get(step["target"])
    elif step["action"] == "input_text":
        element = driver.find_element(By.CSS_SELECTOR, step["target"])
        element.clear()
        element.send_keys(step["value"])
    elif step["action"] == "click":
        driver.find_element(By.CSS_SELECTOR, step["target"]).click()
    elif step["action"] == "verify_present":
        assert driver.find_element(By.CSS_SELECTOR, step["target"]).is_displayed()
    elif step["action"] == "verify_not_present":
        assert not driver.find_element(By.CSS_SELECTOR, step["target"]).is_displayed()
    elif step["action"] == "verify_url":
        assert driver.current_url == step["value"]
    elif step["action"] == "verify_presence":
        driver.find_element(By.CSS_SELECTOR, step["target"])

# Execução dos casos de teste
for test in test_cases:
    print(f"Executando {test['id']}: {test['description']}")
    try:
        for step in test["steps"]:
            execute_step(step)
        
        print("Aprovado")
    except AssertionError:
        print("Reprovado")
    except Exception as e:
        print(f"Erro durante o teste: {str(e)}")
    finally:
        time.sleep(3)  # Pausar por 3 segundos antes do próximo teste

# Encerrar o WebDriver
driver.quit()
