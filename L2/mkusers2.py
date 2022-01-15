import subprocess
import re

SOURCE = "./list-login-pass2.csv"

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

            # if int(loginNumber) % 2 == 0:
            #     if currLocalDepartement != departement:
            #         result = subprocess.run(f"groupadd {departement}", stdout=subprocess.PIPE, shell=True)
            #     currLocalDepartement = departement
            # else:
            #     if currGlobalDepartement != departement:
            #         with open(f"createGroup{departement}.ldif", "w") as file:
            #             file.write(f"dn: cn={departement}, ou = Groups, dc = localdomain\n")
            #             file.write(f"description: {departement}\n")
            #             file.write(f"objectClass: top\n")
            #             file.write(f"objectClass: posixGroup\n")
            #             file.write(f"gidNumber: {uidGroupNumber}\n")
            #
            #         subprocess.run(
            #             f"ldapadd -D 'cn=Directory Manager,dc=localdomain' -f createGroup{departement}.ldif -x -w rootroot",
            #             stdout=subprocess.PIPE, shell=True)
            #
            #     currGlobalDepartement = departement

            if int(loginNumber) % 2 == 0:
                subprocess.run(f"useradd -g users -c \"{firstname} {lastname}\" -m {login}", stdout=subprocess.PIPE, shell=True)
                subprocess.run(f"usermod -G {departement} {login}", stdout=subprocess.PIPE, shell=True)
                subprocess.run(f"echo {password} | passwd -f --stdin {login}", stdout=subprocess.PIPE, shell=True)
            else:
                result = subprocess.run(f"slappasswd -s {password}", stdout=subprocess.PIPE, shell=True)
                password = result.stdout.decode().strip()

                subprocess.run(f"python3.9 mkglobal-user.py {lastname} {firstname} {str(uidNumber)} {login} {password}",
                               stdout=subprocess.PIPE, shell=True)

                subprocess.run(f"usermod -G {departement} {login}", stdout=subprocess.PIPE, shell=True)

                # with open(f"addUser{login}ToGroup{departement}.ldif", "w") as file:
                #     file.write(f"dn: cn={departement},ou=Groups,dc=localdomain\n")
                #     file.write("changetype: modify\n")
                #     file.write(f"add: memberuid\n")
                #     file.write(f"memberuid: {login}\n")
                #
                # subprocess.run(
                #     f"ldapadd -D 'cn=Directory Manager,dc=localdomain' -f addUser{login}ToGroup{departement}.ldif -x -w rootroot",
                #     stdout=subprocess.PIPE, shell=True)

                uidNumber += 1
                uidGroupNumber += 1

