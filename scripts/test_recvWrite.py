import paramiko
import logging
from struct import pack

# Activer les logs de débogage
logging.basicConfig(level=logging.DEBUG)

# Détails de connexion
hostname = "127.0.0.1"
port = 22222
username = "jill"
password = "upthehill"

def test_sftp_write():
    try:
        # Créer un client SFTP
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Ouvrir un fichier en mode écriture
        with sftp.open("./test.txt", "w") as f:
            # Manipuler directement le descripteur de fichier (handle)
            # Ici, nous envoyons un handle malformé de 8 bytes
            f.handle = b'\x00\x00\x00\x00\xCA\xFE\xBA\xBE'  # Handle invalide

            # Écrire des données minimales pour provoquer une erreur
            f.write("a" * 2)  # Écrire 2 octets de données

            # Essayer d'écrire à un offset invalide
            f.seek(1000000000)  # Déplacer le curseur à un offset invalide
            f.write("b" * 1000)  # Écrire des données supplémentaires

        print("Écriture réussie dans test.txt")

    except Exception as e:
        print(f"Erreur lors de l'écriture : {e}")

    finally:
        # Fermer la connexion
        if 'sftp' in locals():
            sftp.close()
        if 'transport' in locals():
            transport.close()

if __name__ == "__main__":
    test_sftp_write()