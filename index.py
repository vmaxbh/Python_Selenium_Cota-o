from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from confidencial import YOUR_ACCOUNT_SID, YOUR_AUTH_TOKEN, YOUR_TWILIO_PHONE_NUMBER

# Configuração do Twilio
account_sid = YOUR_ACCOUNT_SID
auth_token = YOUR_AUTH_TOKEN
twilio_phone_number = YOUR_TWILIO_PHONE_NUMBER
to_phone_number = '+5531994947380'

# Função para enviar mensagem SMS usando o Twilio
def enviar_sms(mensagem):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=mensagem,
            from_=twilio_phone_number,
            to=to_phone_number
        )
        print(f"Mensagem enviada com SID: {message.sid}")
    except Exception as e:
        print(f"Erro ao enviar mensagem SMS: {str(e)}")

# Função para extrair a cotação
def auto_extract_moeda(moeda, query):
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")
        textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'q')))
        textarea.send_keys(query)
        textarea.send_keys(Keys.RETURN)
        elemento_moeda = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]')))
        valor_moeda = elemento_moeda.text
        return valor_moeda
    except Exception as e:
        print(f"Erro ao extrair cotação da {moeda}: {str(e)}")
    finally:
        driver.quit()

# Chama a função e armazena os valores retornados
valor_dolar = auto_extract_moeda('Dólar', 'Cotação dólar de hoje!')
valor_euro = auto_extract_moeda('Euro', 'Cotação euro de hoje!')

# Envia as cotações por SMS
mensagem_sms = f"Cotação do Dólar: {valor_dolar}, Cotação do Euro: {valor_euro}"
enviar_sms(mensagem_sms)
