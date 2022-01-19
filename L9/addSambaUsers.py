import subprocess
import re

SOURCE = "./list-login-pass.csv"

with open(SOURCE, "r") as entree:
    currDepartement = ""
    uidNumber = 20501
    uidGroupNumber = 30000
    for ligne in entree:
        pattern = re.compile(r'^([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)$')
        match = pattern.match(ligne.rstrip())
        if match:
            login = match.group(4)
            password = match.group(5)
            subprocess.run(f"(echo {password}; echo {password}) | smbpasswd -a {login}", stdout=subprocess.PIPE, shell=True)
