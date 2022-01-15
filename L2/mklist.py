import re
import secrets
import subprocess

SOURCE = "./liste-utilisateurs.csv"

with open(SOURCE, "r") as entree:
    counter = 0
    currDepartement = ""
    for ligne in entree:
        pattern = re.compile(r'^([^;]+);([^;]+);([^;]+)$')
        match = pattern.match(ligne.rstrip())
        if match:
            nom = match.group(1)
            prenom = match.group(2)
            departement = match.group(3)
            if currDepartement != departement:
                counter = 0
            currDepartement = departement
            counter += 1

            login = departement[0:1].lower() + departement[-1].lower() + str(counter).zfill(4)

            password = ""
            if counter == 1:
                password = "Passw0rd"
            else:
                if secrets.randbelow(2) == 0:
                    uppercaseNb = secrets.randbelow(9) + 3
                    digitNb - secrets.randbelow(15 - 3 - uppercaseNb) + 3
                else:
                    digitNb = secrets.randbelow(9) + 3
                    uppercaseNb - secrets.randbelow(15 - 3 - digitNb) + 3
                result = subprocess.run(f"mkpasswd -l 15 -C {uppercaseNb} -s 0 -d {digitNb} -c 1", stdout=subprocess.PIPE,
                                        shell=True)
                password = result.stdout.decode().rstrip()

            print(f"{nom};{prenom};{departement};{login};{password}")
