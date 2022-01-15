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
            loginNumber = match.group(4)[2:].lstrip("0")
            lastname = match.group(1)
            firstname = match.group(2)
            departement = match.group(3)
            login = match.group(4)
            password = match.group(5)

            if currDepartement != departement:
                result = subprocess.run(f"groupadd {departement}", stdout=subprocess.PIPE, shell=True)
                currDepartement = departement

            if int(loginNumber) % 2 == 0:
                subprocess.run(f"useradd -g users -G {departement} -c \"{firstname} {lastname}\" -m {login}", stdout=subprocess.PIPE, shell=True)
                subprocess.run(f"echo {password} | passwd -f --stdin {login}", stdout=subprocess.PIPE, shell=True)
            else:
                result = subprocess.run(f"slappasswd -s {password}", stdout=subprocess.PIPE, shell=True)
                password = result.stdout.decode().strip()

                subprocess.run(f"python3.9 mkglobal-user.py \"{lastname}\" \"{firstname}\" \"{str(uidNumber)}\" \"{login}\" \"{password}\"",
                               stdout=subprocess.PIPE, shell=True)

                subprocess.run(f"usermod -G {departement} {login}", stdout=subprocess.PIPE, shell=True)
                uidNumber += 1
                uidGroupNumber += 1
