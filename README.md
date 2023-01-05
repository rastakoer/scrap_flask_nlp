<h1><b><u><i>Contexte du projet</i><u><b></h1>
<h2>
En règle générale, le nombre d'avis sur un film peu être important et par conséquent le temps de lecture de chaque commentaire peut être une tâche lourde. Alors comment déterminer de manière rapide si un film a eu du succès auprès des spectateurs (ou pas) ? Dans ce contexte, l’idée du projet est d’utiliser des algorithmes d'apprentissage automatique pour la tâche d'analyse de sentiment des spectateurs via leur critique.<br><br>

Tout d’abord, il sera question que récupérer les données directement du site d’Allociné. En d’autres termes, nous allons scraper les pages qui nous intéressent sur ce site à savoir les critiques des personnes pour le film Inception et Sonic 2.<br><br>

En navigant sur la page des critiques, vous vous apercevrez que seules deux types d’information ici nous intéresse : la note du spectateur ainsi que son avis. Pourquoi la note ? Parce que nous allons entraîner un modèle de type supervisé et plus précisément un classifieur et donc la note va nous aider à récupérer la classe pour étiqueter le commentaire. Pour cela, nous considérerons qu’une note au-dessus de 3 est considérée comme satisfaisante. Sinon, l’avis est négatif. Ici, nous avons donc réduit le problème à une classification binaire.<br><br>

Voici donc les étapes à réaliser : • Récupération des données • Préparation des données. • Préparation du modèle et des jeux de données (entrainement & test) • Analyse des résultats<h2>