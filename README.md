# VRPTW Project - Optimization Solver

Ce projet implémente des algorithmes de résolution pour le **Problème de Tournées de Véhicules avec Fenêtres de Temps (VRPTW)**.

##  Fonctionnalités
- **Modélisation complète** : Gestion des clients, dépôts, véhicules et contraintes de temps.
- **Algorithmes de résolution** : 
  - Heuristiques de construction (Solomon).
  - Optimisation par recherche locale (Relocate, Hybrid Optimizer).
- **Visualisation** : Interface web pour observer les tournées obtenues.

##  Structure du Projet
- `src/algorithms/` : Logique des solveurs (Solomon, Hybrid).
- `src/models/` : Classes de données (Customer, Route, Vehicle).
- `src/services/` : Utilitaires de parsing et de visualisation.

##  Perspectives d'amélioration
- Intégration de métaheuristiques avancées (Algorithmes génétiques, Tabu Search, ALNS).
- Utilisation de l'intelligence artificielle pour guider les décisions d'insertion.
