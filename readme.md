# Recupérer version git 
Deux moyen :
-  git clone avec htpps retaper nom d'utilisateur et mdp a chaque fois
- git clone avec ssh : creer une clé ssh ( ssh-keygen) : ajouter une clé ssh dans les setting gitHub :copier l'id_rsa.pub dedans

--- 
# Installation du site

- Cloner le dépot git
- Creer un environnement python : python3 -m venv env
- Mettre a jour pip : python -m pip install --upgrade pip
- Installer la version django : pip install -r requirements.txt