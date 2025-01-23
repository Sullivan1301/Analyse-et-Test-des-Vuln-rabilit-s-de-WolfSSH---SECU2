# Analyse et Test des Vulnérabilités de WolfSSH

## **Présentation**
Ce dépôt contient les ressources nécessaires pour analyser et reproduire des vulnérabilités dans WolfSSH, en particulier dans le module SFTP. Le projet met en évidence et démontre les problèmes suivants :
- **Stack-buffer-overflow** (exemple : `wolfSSH_SFTP_RecvWrite`)
- **Heap-buffer-overflow** (exemples : `wolfSSH_SFTP_RecvRead` et `wolfSSH_SFTP_RecvRealPath`)

## **Contenu**
1. **Scripts**
   - Scripts Python utilisant `Paramiko` pour déclencher les vulnérabilités du serveur.
   - Scénarios détaillés pour tester les exploits.

2. **Configuration de l'environnement**
   - Fichiers Docker (`Dockerfile` et `docker-compose.yml`) pour créer un environnement de test contrôlé.
   - Instructions pour compiler WolfSSL et WolfSSH avec le support d'AddressSanitizer (ASAN).

3. **Logs ASAN**
   - Exemples de logs ASAN montrant les vulnérabilités et problèmes de mémoire.

4. **Documentation**
   - Rapport détaillé analysant les vulnérabilités, leurs causes et leurs impacts.
   - Recommandations pour corriger et atténuer ces problèmes.

## **Comment Utiliser**

### **1. Prérequis**
- **Dépendances** : Assurez-vous d'avoir installé :
  - Docker et Docker Compose
  - Python 3
  - Pip (`pip install paramiko`)
  - Git

### **2. Configuration**
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre_utilisateur/analyses-vulnerabilites-wolfssh.git
   cd analyses-vulnerabilites-wolfssh
   ```
2. Construisez l'environnement Docker :
   ```bash
   docker-compose up --build
   ```
3. Compilez WolfSSL et WolfSSH avec ASAN (voir `docs/instructions_configuration.md`).

### **3. Lancer les Tests**
- Utilisez les scripts Python dans le dossier `scripts/` pour tester les vulnérabilités :
  ```bash
  python3 scripts/test_***.py
  ```

### **4. Analyser les Logs**
- Les logs ASAN sont générés dans le répertoire `logs/`. Utilisez-les pour identifier et déboguer les vulnérabilités.

