import paramiko
import logging

# Activer les logs de débogage (optionnel)
# logging.basicConfig(level=logging.DEBUG)

# Détails de connexion
hostname = "127.0.0.1"
port = 22222
username = "jill"
password = "upthehill"

# Créer un client SFTP
try:
    transport = paramiko.Transport((hostname, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Lister les fichiers dans le répertoire racine
    files = sftp.listdir('.')
    print("Fichiers sur le serveur SFTP:", files)

    # Fermer la connexion
    sftp.close()
    transport.close()

except Exception as e:
    print(f"Erreur lors de la connexion ou de l'exécution de la commande : {e}