import subprocess
import sys

if len(sys.argv) < 6 or len(sys.argv) > 6:
    print("Arguments are invalid")
else:
    lastname = sys.argv[1]
    firstname = sys.argv[2]
    uidNumber = sys.argv[3]
    uid = sys.argv[4]
    password = sys.argv[5]

    result = subprocess.run(f"slappasswd -s {password}", stdout=subprocess.PIPE, shell=True)
    password = result.stdout.decode().strip()

    with open("global-user.ldif", "w") as file:
        file.write(f"dn: uid={uid},ou=People,dc=localdomain\n")
        file.write("objectClass: top\nobjectClass: inetorgperson\nobjectClass: posixAccount\n")
        file.write(f"cn: {firstname} {lastname.upper()}\n")
        file.write(f"sn: {lastname}\n")
        file.write(f"givenname: {firstname}\n")
        file.write(f"userPassword: {password}\n")
        file.write(f"gidNumber: 100\n")
        file.write(f"uidNumber: {uidNumber}\n")
        file.write(f"homeDirectory: /home/{uid}\n")
        file.write("loginShell: /bin/bash\n")

    subprocess.run("ldapadd -D 'cn=Directory Manager,dc=localdomain' -f global-user.ldif -x -w rootroot",
                   stdout=subprocess.PIPE, shell=True)

    subprocess.run(f"mkhomedir_helper {uid}", stdout=subprocess.PIPE, shell=True)
