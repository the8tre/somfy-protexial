# Comment développer cette intégration

## Pré-requis:
- Visual Studio Code
- Docker desktop

## Préparer l'environnement
1. Fork le repository [`somfy-protexial`](https://github.com/the8tre/somfy-protexial)
2. Clone le repository en local
3. Ouvrir le repository avec VSCode
  - Quand le repository est ouvert dans VSCode il propose **Reopen in container**. Cela lance la construction du container.
  - Si cette notification ne s'affiche pas ouvrir la palette de commande et lancer **Dev Containers: Reopen in Container**

Si VSCode n'arrive pas à résoudre les dépendances dans les imports des fichiers Python, ouvrir la paleztte de commande et lancer **Python Debugger: Clear Cache and Reload Window**

## Lancer Home Assistant
1. Ouvrir la palette de commandes et chercher **Tasks: Run Task**
2. Lancer la task **Run Home Assistant on port 8123**

## Debugger l'intégration
1. Home Assistant doit être en train de tourner
2. Exécuter le profile de lancement **debugpy: Attach Local**
