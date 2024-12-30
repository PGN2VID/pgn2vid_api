# 🛠️ **API de Génération de Vidéos d'Échecs à partir de PGN**

Cette API permet de générer une vidéo animée représentant les coups d'une partie d'échecs à partir d'un fichier PGN (Portable Game Notation).

---

## 🚀 **Prérequis**

Avant d'installer le projet, assurez-vous d'avoir les éléments suivants :

- **Python 3.x**
- **pip** (gestionnaire de paquets Python)
- **virtualenv** (environnement virtuel Python)

---

## 📦 **Installation**

### 1. **Cloner le dépôt**
```bash
git clone https://github.com/PGN2VID/pgn2vid_api.git
cd pgn2vid_api
```

### 2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

### 3. **Activer l'environnement virtuel**
* **Windows :**
```bash
venv\Scripts\activate
```
* **Linux/MacOS :**
```bash
source venv/bin/activate
```

### 4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## ⚙️ **Configuration**

### 1. **Se placer dans le répertoire pgn2vid_api**   
```bash
cd pgn2vid_api
```
### 2. **Appliquer les migrations**   
```bash
python manage.py makemigrations
python manage.py migrate
```
### 3. **Créer un superutilisateur**
Créez un compte administrateur pour accéder à l'interface d'administration :
```bash
python manage.py createsuperuser
```
### 4. **Lancer le serveur**
Démarrez le serveur Django avec la commande suivante :
```bash
python manage.py runserver
```
L'API sera accessible sur : http://127.0.0.1:8000


## 🧪 **Tester l'API**

Vous pouvez tester l'API directement avec cURL. Par exemple :
* **Endpoint pour générer une vidéo à partir d'un PGN :**
```bash
curl --location --request POST 'http://127.0.0.1:8000/api/generate-chess-video/' \
--header 'Content-Type: application/json' \
--data '{
    "content": "[Event \"Casual Game\"]\n[Site \"Berlin GER\"]\n[Date \"1852.??.??\"]\n[EventDate \"?\"]\n[Round \"?\"]\n[Result \"1-0\"]\n[White \"Adolf Anderssen\"]\n[Black \"Jean Dufresne\"]\n[ECO \"C52\"]\n[WhiteElo \"?\"]\n[BlackElo \"?\"]\n[PlyCount \"47\"]\n\n1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Ba5 6.d4 exd4 7.O-O\nd3 8.Qb3 Qf6 9.e5 Qg6 10.Re1 Nge7 11.Ba3 b5 12.Qxb5 Rb8 13.Qa4\nBb6 14.Nbd2 Bb7 15.Ne4 Qf5 16.Bxd3 Qh5 17.Nf6+ gxf6 18.exf6\nRg8 19.Rad1 Qxf3 20.Rxe7+ Nxe7 21.Qxd7+ Kxd7 22.Bf5+ Ke8\n23.Bd7+ Kf8 24.Bxe7# 1-0"
}' --output immortal_game.mp4
```



