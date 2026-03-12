class OutputService:
    # Cette méthode affiche un résumé complet de la solution
    @staticmethod
    def print_solution(solution):
        # Affichage du nombre de routes
        print("=== SOLUTION ===")
        print(f"Nombre de routes : {len(solution.routes)}")
        print(f"Distance totale : {solution.total_distance():.2f}")

        # Affichage détaillé de chaque route
        for index, route in enumerate(solution.routes, start=1):
            print(f"Route {index} : dépôt -> {route.get_customer_ids()} -> dépôt")
            print(f"  Charge : {route.current_load}")
            print(f"  Distance : {route.total_distance:.2f}")