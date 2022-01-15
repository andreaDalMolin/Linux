import subprocess
import re

SOURCE = "./list-login-pass.csv"

with open(SOURCE, "r") as entree:
    currDepartement = ""
    for ligne in entree:
        pattern = re.compile(r'^([^;]+);([^;]+);([^;]+);([^;]+);([^;]+)$')
        match = pattern.match(ligne.rstrip())
        if match:
            currDepartement = match.group(3)
            login = match.group(4)

            if currDepartement == "Compta":
                subprocess.run(f"xfs_quota -x -c 'limit bsoft=100m bhard=130m {login}' /home", stdout=subprocess.PIPE, shell=True)
            elif currDepartement == "Soins":
                subprocess.run(f"xfs_quota -x -c 'limit bsoft=110m bhard=140m {login}' /home", stdout=subprocess.PIPE, shell=True)
            else:
                subprocess.run(f"xfs_quota -x -c 'limit bsoft=180m bhard=200m {login}' /home", stdout=subprocess.PIPE, shell=True)
