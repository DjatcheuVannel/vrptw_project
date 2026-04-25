class OutputService:
    @staticmethod
    def verify_clients(solution, expected_ids):
        """
        Vérifie que chaque client demandé est visité exactement une fois.
        """
        all_served_ids = []
        for route in solution.routes:
            all_served_ids.extend(route.get_customer_ids())

        unique_served = set(all_served_ids)
        expected_set = set(expected_ids)

        print("\n" + "="*30)
        print("    RAPPORT DE VÉRIFICATION")
        print("="*30)
        print(f"Visites totales effectuées : {len(all_served_ids)}")
        print(f"Clients uniques servis     : {len(unique_served)} / {len(expected_set)}")

        # Identification des anomalies
        missing = expected_set - unique_served
        extra = unique_served - expected_set
        duplicates = [c for c in unique_served if all_served_ids.count(c) > 1]

        # Affichage des erreurs éventuelles
        if missing:
            print(f"❌ ERREUR : Clients manquants ({len(missing)}) : {sorted(list(missing))}")
        
        if extra:
            print(f"❌ ERREUR : Clients non demandés servis ({len(extra)}) : {sorted(list(extra))}")
            
        if duplicates:
            print(f"❌ ERREUR : Clients en doublon ({len(duplicates)}) : {duplicates}")

        # Conclusion
        if not missing and not extra and not duplicates:
            print("\n✨ SUCCÈS : Tous les clients attendus sont servis correctement !")
        else:
            print("\n⚠️ ALERTE : La structure des tournées est invalide.")

    @staticmethod
    def print_solution(solution, expected_ids=None):
        """
        Affiche un résumé détaillé de la solution trouvée.
        Accepte expected_ids (liste) pour la vérification stricte.
        """
        print("\n" + "█"*40)
        print("         RÉSUMÉ DE LA SOLUTION")
        print("█"*40)
        
        # 1. Gestion robuste de la distance totale
        dist_val = 0
        if hasattr(solution, 'total_distance'):
            val = solution.total_distance
            dist_val = val() if callable(val) else val
        else:
            # Fallback : somme des distances des routes
            dist_val = sum(getattr(r, 'total_distance', 0) for r in solution.routes)

        print(f"Nombre de routes  : {len(solution.routes)}")
        print(f"Distance totale   : {dist_val:.2f}")
        print("-" * 40)

        # 2. Détail par route
        all_ids = []
        for index, route in enumerate(solution.routes, start=1):
            ids = route.get_customer_ids()
            all_ids.extend(ids)
            
            route_str = " -> ".join(map(str, ids))
            print(f"Route {index:02d} : Dépôt -> {route_str if route_str else 'Vide'} -> Dépôt")
            print(f"         [Charge: {route.current_load} | Distance: {route.total_distance:.2f}]")

        # 3. Déclenchement de la vérification
        if expected_ids is not None:
            OutputService.verify_clients(solution, expected_ids)
        else:
            # Si aucune liste n'est fournie, on vérifie au moins les doublons
            OutputService.verify_clients(solution, all_ids)