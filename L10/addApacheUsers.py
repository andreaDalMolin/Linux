import subprocess
import re

SOURCE = "./list-login-pass.csv"

with open(SOURCE, "r") as entree:
    for ligne in entree:
        pattern = re.compile(r'^([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)$')
        match = pattern.match(ligne.rstrip())
        if match:
            login = match.group(4)
            password = match.group(5)
            subprocess.run(f"htpasswd -B -b /etc/httpd/admin.passwd {login} {password}", stdout=subprocess.PIPE, shell=True)