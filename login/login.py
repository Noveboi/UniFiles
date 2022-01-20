import requests
import webbrowser
from conf import username, password

tgt = {
    'service': "https://gunet2.cs.unipi.gr/secure/cas.php"
}

form_data_payload = {
    "username": username,
    "password": password
}

base_url = "https://sso.unipi.gr/login"
target_url = "https://gunet2.cs.unipi.gr/main/portfolio.php"

def main():
    with requests.session() as session:
        #get website status
        request = session.get(base_url, params=tgt, verify="gunet2-cs-unipi-gr-chain.pem")
        if request.ok:
            log_request = session.post(base_url, params=tgt, verify="gunet2-cs-unipi-gr-chain.pem", data=form_data_payload)
            print("POST request passed - Status {}".format(log_request.status_code))
            if(log_request.url != target_url):
                print("No redirect")
            else:
                print("Redirect succesful!")
            with open("rawweb.html", "w") as f:
                f.write(log_request.text)
        else:
            print("Oops! - Status {}".format(request.status_code))

if __name__ == "__main__":
    main()