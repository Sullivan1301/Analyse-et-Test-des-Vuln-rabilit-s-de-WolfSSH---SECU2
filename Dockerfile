# Dockerfile
FROM ubuntu:24.04

# Installer les dépendances
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

# Installer Paramiko pour les scripts Python
RUN pip install paramiko --break-system-packages

# Copier les dépôts wolfSSL et wolfSSH dans le dossier src
COPY src/wolfssl-5.7.6-stable /wolfssl-5.7.6-stable
COPY src/wolfssh-1.4.6-stable /wolfssh-1.4.6-stable

# Compiler wolfSSL
WORKDIR /wolfssl-5.7.6-stable
RUN ./autogen.sh && \
    ./configure --enable-ssh && \
    make && \
    make install && \
    ldconfig

# Compiler wolfSSH avec ASAN
WORKDIR /wolfssh-1.4.6-stable
RUN ./autogen.sh && \
    CFLAGS="-fsanitize=address -g -O0" ./configure --enable-sftp && \
    make

# Créer un répertoire pour les scripts Python
WORKDIR /scripts
COPY scripts /scripts

# Commande par défaut pour lancer un shell interactif
CMD ["/bin/bash"]