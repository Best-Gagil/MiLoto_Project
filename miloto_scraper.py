import requests
import smtplib
from bs4 import BeautifulSoup


def check_url(url, headers):
    page = requests.get(url, headers=headers)
    status_code = page.status_code

    if status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        # Extraer el número de sorteo
        numero_sorteo = soup.find('div', class_='container-contest').strong.text.strip().split("#")[1]

        # Extraer la fecha
        fecha = soup.find('div', class_='fs-5').strong.text.strip()

        # Extraer los números dentro de <div class="yellow-ball">
        numeros = [numero.text.strip() for numero in soup.find_all('div', class_='yellow-ball')]

        # Imprimir los resultados
        print(f"Número de Sorteo: {numero_sorteo}")
        print(f"Fecha: {fecha}")
        print(f"Números: {', '.join(numeros)}")


    return status_code


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
url = 'https://baloto.com/miloto/resultados-miloto/'
sorteo = '1'
url_full = url + sorteo

check_url(url_full, headers)



