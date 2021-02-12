# SK_P2

#### Vérifier la version de Python installée sur la machine (la gestion des environnements virtuelles est disponible depuis la version 3.3)
`python --version`  

#### Controler le bon fonctionnement de venv qui permet de créer des environnements virtuels
`python -m venv --help`

#### Définir du répertoire actif avec la commande cd suivit du chemin (si besoin vous pouvez changer de disque avec `cd /d d:`)
`cd C:\Users\Luke\projects\OC_P2_venv`

#### Créer de l'environnement virtuel
`python -m venv env`

#### Activer l'environnement virtuel
`call  env/Scripts/activate.bat`

#### Mettre à jour de pip et installer des paquets nécessaires au bon fonctionnement du script (requirements.txt)
`python -m pip install --upgrade pip`  
`pip install requests==2.25.1`  
`pip install beautifulsoup4==4.9.3`

#### Exécution du script
`main_p2.py`

#### Après la fin du traitement. Désactivation environnement à l'aide de la commande
`deactivate`

<!-- Créer le fichier requirements.txt -->
<!-- pip freeze > requirements.txt -->


