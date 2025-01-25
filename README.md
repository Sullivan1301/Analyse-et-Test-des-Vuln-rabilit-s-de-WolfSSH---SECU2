# Documentation Technique : Mise en Place et Test de wolfSSH avec ASAN

## 1. Préparation de l'environnement

### 1.1. Installation des dépendances
Assurez-vous que les outils suivants sont installés sur votre système :

- **Docker** : Pour créer et gérer des conteneurs.
- **Docker Compose** : Pour orchestrer les conteneurs.
- **Python 3** : Pour exécuter les scripts de test.
- **Git** : Pour cloner les dépôts.

#### Sur Ubuntu/Debian :
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose python3 git
```

#### Sur CentOS/Fedora :
```bash
sudo yum install -y docker docker-compose python3 git
```

#### Sur macOS :
- Installez Docker Desktop.
- Installez Python 3 via Homebrew :
```bash
brew install python3 git
```

### 1.2. Configuration de Docker

#### Créer un Dockerfile
Le Dockerfile suivant est utilisé pour configurer l'environnement de travail :

```dockerfile
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    autoconf \
    libtool \
    pkg-config \
    gdb \
    python3 \
    python3-pip \
    python3-venv \
    nano \
    wget

RUN pip3 install paramiko

COPY src/wolfssl-5.7.6-stable /wolfssl-5.7.6-stable
COPY src/wolfssh-1.4.6-stable /wolfssh-1.4.6-stable

WORKDIR /wolfssl-5.7.6-stable
RUN ./autogen.sh && \
    ./configure --enable-ssh && \
    make && \
    make install && \
    ldconfig

WORKDIR /wolfssh-1.4.6-stable
RUN ./autogen.sh && \
    CFLAGS="-fsanitize=address -g -O0" ./configure --enable-sftp && \
    make

WORKDIR /scripts
COPY scripts /scripts

CMD ["/bin/bash"]
```

#### Créer un fichier docker-compose.yml

```yaml
version: '3.8'
services:
  wolfssh:
    build: .
    container_name: wolfssh_container
    ports:
      - "22222:22222"
    volumes:
      - ./logs:/logs
    command: /bin/bash
```

#### Construire et lancer le conteneur

```bash
docker-compose up --build
```

---

## 2. Compilation de wolfSSL et wolfSSH avec ASAN

### 2.1. Télécharger et extraire les sources

Téléchargez les versions stables de wolfSSL et wolfSSH :

```bash
wget https://github.com/wolfSSL/wolfssl/archive/refs/tags/v5.7.6-stable.tar.gz
wget https://github.com/wolfSSL/wolfssh/archive/refs/tags/v1.4.6-stable.tar.gz
```

Extrayez les archives :

```bash
tar -xf v5.7.6-stable.tar.gz
tar -xf v1.4.6-stable.tar.gz
```

### 2.2. Compiler wolfSSL

Accédez au répertoire de wolfSSL et compilez-le :

```bash
cd wolfssl-5.7.6-stable
./autogen.sh
./configure --enable-ssh
make
sudo make install
sudo ldconfig
```

### 2.3. Compiler wolfSSH avec ASAN

Accédez au répertoire de wolfSSH et compilez-le avec ASAN :

```bash
cd ../wolfssh-1.4.6-stable
./autogen.sh
CFLAGS="-fsanitize=address -g -O0" ./configure --enable-sftp
make
```

---

## 3. Lancer le serveur SFTP vulnérable

Une fois wolfSSH compilé, lancez le serveur SFTP en utilisant l'exemple fourni :

```bash
./examples/echoserver/echoserver -f
```

Par défaut, le serveur écoutera sur le port **22222**.

---

## 4. Exécuter les scripts Python de test

### 4.1. Installer les dépendances Python

Assurez-vous que Python 3 et pip sont installés. Ensuite, installez la bibliothèque Paramiko :

```bash
sudo apt install python3-pip
pip install paramiko
```

### 4.2. Exécuter les scripts

- **Script pour wolfSSH_SFTP_RecvWrite :**
```bash
python3 sftp_write_test.py
```

- **Script pour wolfSSH_SFTP_RecvRead :**
```bash
python3 sftp_read_test.py
```

- **Script pour wolfSSH_SFTP_RecvRealPath :**
```bash
python3 sftp_realpath_test.py
```

---

## 5. Capturer les logs ASAN

Les logs ASAN seront générés dans la console où le serveur SFTP est exécuté. Vous pouvez rediriger les logs vers un fichier pour une analyse ultérieure :

```bash
./echoserver -f 2> asan_logs.txt
```

Les logs seront disponibles dans le fichier **asan_logs.txt**.

---

## 6. Attacher GDB pour le débogage (optionnel)

### 6.1. Trouver l'ID du processus (PID)

Utilisez la commande `ps` pour trouver l'identifiant du processus (PID) du serveur SFTP :

```bash
ps aux | grep echoserver
```

### 6.2. Attacher GDB au processus

Une fois que vous avez le PID, attachez GDB au processus avec la commande suivante :

```bash
gdb -p <PID>
```

Remplacez `<PID>` par l'identifiant du processus trouvé à l'étape précédente.

---

## 7. Instructions de reproduction

### 7.1. Compiler wolfSSL et wolfSSH avec ASAN

Suivez les étapes décrites dans la section 2.

### 7.2. Lancer le serveur SFTP vulnérable

Suivez les étapes décrites dans la section 3.

### 7.3. Exécuter les scripts Python

Suivez les étapes décrites dans la section 4.

### 7.4. Capturer les logs ASAN

Suivez les étapes décrites dans la section 5.

### 7.5. (Optionnel) Attacher GDB pour le débogage

Suivez les étapes décrites dans la section 6.

---

## 8. Conclusion

Ces instructions vous permettront de reproduire les erreurs ASAN dans les fonctions **wolfSSH_SFTP_RecvWrite**, **wolfSSH_SFTP_RecvRead**, et **wolfSSH_SFTP_RecvRealPath**. Les logs ASAN générés vous aideront à confirmer la présence des vulnérabilités et à analyser leur impact.

