import requests
import json
from bs4 import BeautifulSoup


def getAnchorToken(source: str) -> str|None:
    soup = BeautifulSoup(source, "html.parser")
    rawToken = soup.find("input", id="recaptcha-token")
    if rawInput is not None:
        return rawToken["value"]
    

    return None
def getReloadToken(rawResponse: str) -> str:
    responseList: list = json.loads(rawResponse[5:])


    return responseList[1]    


if __name__ == "__main__":
    APIs: dict = {
        "anchor": "https://www.recaptcha.net/recaptcha/api2/anchor",
        "reload": "https://www.recaptcha.net/recaptcha/api2/reload",
    }
    
    
    rawInput: str = str(input("Anchor URL: "))
    assert rawInput.startswith(APIs["anchor"]), "Invalid Input"
    
    session = requests.session()
    rawData: list = [i.split("=") for i in rawInput.split("?")[1].split("&")]
    
    anchorParams: dict = {item[0]:item[1] for item in rawData}
    anchorParams["size"] = "invisible"
    reloadParams: dict = {
        "k": anchorParams["k"]
    }
    
    
    response = session.get(APIs["anchor"], params=anchorParams)
    token: str = getAnchorToken(response.text)
    
    reloadData: dict = {
        "c": token,
        "reason": "q"
    }
    
    response = session.post(APIs["reload"], params=reloadParams, data=reloadData)
    token: str = getReloadToken(response.text)
    
    print(f"\n\nTOKEN: {token}")
