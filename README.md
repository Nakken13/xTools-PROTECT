# 💠 xProtect Discord Bot

> **xProtect** est un bot Discord multifonction développé en **Python** avec la librairie `discord.py`.  
Il propose des systèmes de **modération**, **bienvenue / départ**, **tickets**, **giveaways** et bien plus encore.

---

## ⚙️ Fonctionnalités principales

### 👋 Gestion des arrivées et départs
- Envoie un message de **bienvenue** quand un membre rejoint.
- Envoie un message de **départ** quand un membre quitte.
- Possibilité d’ajouter plusieurs salons de **greet** où le bot ping simplement les nouveaux membres.

### 🎫 Système de tickets
- Crée un bouton permettant aux utilisateurs d’ouvrir un **ticket privé**.
- Les tickets sont créés dans une **catégorie** spécifique.
- Le staff (rôles configurés) peut accéder et fermer les tickets.
- Possibilité de configurer le système via une commande `/setup_ticket`.

### 🎉 Giveaways
- Créez un **giveaway** avec `/giveaway`.
- Personnalisez la **durée**, le **nombre de gagnants**, et le **prix**.
- Sélection automatique des gagnants à la fin du timer.
- Suppression possible avec `/delete_giveaway`.

### 🧰 Commandes d’administration
Commandes préfixées avec `+` :
- `+clear` : supprime tous les messages d’un salon (en recréant le canal).
- `+lock` / `+unlock` : verrouille / déverrouille un salon.
- `+hide` / `+show` : rend un salon invisible / visible.
- `+ban`, `+mute`, `+unmute`, `+tempmute` : modération de base.
- `+vip` / `+unvip` : gestion du rôle VIP.
- `+delete <nombre>` : supprime un nombre précis de messages.
- `+help` : affiche la liste complète des commandes administratives.

### ⚡ Slash Commands (`/`)
- `/setup_welcome` : configure les salons de bienvenue et de départ.  
- `/setup_greet` : ajoute un salon à la liste des greet.  
- `/delete_greet` / `/delete_all_greet` : supprime un ou tous les greet configurés.  
- `/show_all_greet` : affiche les salons de greet.  
- `/setup_ticket` : configure le système de tickets.  
- `/say` : fait parler le bot dans le salon actuel.  
- `/help` : affiche toutes les commandes slash disponibles.

---

## 📦 Installation

### 1️⃣ Prérequis
- Python **3.10+**
- Un **token de bot Discord** (disponible sur le [Portail Développeur Discord](https://discord.com/developers/applications))
- Les permissions nécessaires pour le bot :
  - Gérer les messages, rôles, salons
  - Envoyer des messages
  - Ajouter des réactions
  - Utiliser les slash commands

### 2️⃣ Installation des dépendances

Installe les modules requis avec :
```bash
pip install -U discord.py
