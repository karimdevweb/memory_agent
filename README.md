# memory_agent
le contenu du module 2 - Init agent Ydays



Ce projet contient des scripts Python pour créer et tester des agents conversationnels avec mémoire.
L’objectif est d’expérimenter différents types de mémoire et de mesurer leur efficacité dans des interactions avec un utilisateur.

Les laboratoires inclus sont :

Mémoire courte : l’agent ne garde que les derniers messages pour répondre.

Mémoire avec résumé (summary) : l’agent résume la conversation pour garder l’essentiel et répondre de manière cohérente.

Mémoire longue / persistante : l’agent sauvegarde sa mémoire dans un fichier JSON pour se rappeler des informations entre plusieurs exécutions.



Conclusion observée

La mémoire avec résumé est très efficace, l’agent s’adapte et utilise les nouvelles informations.

Le modèle peut être lent à charger, surtout sur des modèles lourds.

Des erreurs mineures sont observées : confusions dans les phrases ou erreurs de grammaire, l’agent parle parfois de son “ami” au lieu de celui de l’utilisateur.
