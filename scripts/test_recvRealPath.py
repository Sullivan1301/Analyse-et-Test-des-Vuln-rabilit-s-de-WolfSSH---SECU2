import paramiko
import logging
import socket
# Activer les logs de débogage
logging.basicConfig(level=logging.DEBUG)

# Détails de connexion
hostname = "127.0.0.1"
port = 22222
username = "jill"
password = "upthehill"

def test_sftp_realpath():
    try:
        # Créer un client SFTP
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)

        #Definir un timeout de 10 secondes pour les operations
        transport.sock.settimeout(10)

        sftp = paramiko.SFTPClient.from_transport(transport)

        # Tenter de résoudre un chemin excessivement long
        long_path = "./" + "A" * 254  # Chemin de 1000 caractères
        real_path = sftp.normalize(long_path)

        print(f"Chemin réel résolu : {real_path}")

    except Exception as e:
        print(f"Erreur lors de la résolution du chemin réel : {e}")

    finally:
        # Fermer la connexion
        if 'sftp' in locals():
            sftp.close()
        if 'transport' in locals():
            transport.close()

if __name__ == "__main__":
    test_sftp_realpath()