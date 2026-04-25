from src.services.feasibility_service import FeasibilityService
from src.services.distance_service import DistanceService

class RelocateOptimizer:
    def __init__(self, instance):
        self.instance = instance

    def optimize(self, solution):
        print("\n[RelocateOptimizer] Début de l'optimisation locale...")
        improved = True
        iterations = 0

        # On boucle tant qu'on trouve des améliorations (First-Improvement)
        while improved:
            improved = False
            iterations += 1

            for i, r1 in enumerate(solution.routes):
                for j, r2 in enumerate(solution.routes):
                    if r1 == r2:
                        continue  # On cherche uniquement à déplacer entre des routes différentes

                    c_idx = 0
                    while c_idx < len(r1.customers):
                        customer = r1.customers[c_idx]

                        # 1. Vérification rapide de la capacité de r2
                        if not FeasibilityService.is_capacity_feasible(r2, customer):
                            c_idx += 1
                            continue

                        best_pos = None
                        best_saving = 0

                        # 2. Sauvegarde de la distance originale de r1 et retrait temporaire
                        original_r1_dist = r1.total_distance
                        r1.customers.pop(c_idx)
                        r1.current_load -= customer.demand
                        r1.total_distance = DistanceService.compute_route_distance(r1, self.instance)
                        
                        # Économie réalisée en retirant le client de r1
                        dist_saved_r1 = original_r1_dist - r1.total_distance

                        # 3. Test d'insertion dans r2 à toutes les positions possibles
                        original_r2_dist = r2.total_distance

                        for pos in range(len(r2.customers) + 1):
                            # Vérifier si l'insertion respecte les fenêtres de temps
                            if FeasibilityService.is_insertion_time_feasible(r2, customer, pos, self.instance):
                                # Insertion temporaire pour calculer l'impact sur la distance
                                r2.customers.insert(pos, customer)
                                new_r2_dist = DistanceService.compute_route_distance(r2, self.instance)
                                r2.customers.pop(pos)  # On annule l'insertion temporaire

                                dist_added_r2 = new_r2_dist - original_r2_dist
                                saving = dist_saved_r1 - dist_added_r2

                                # Si on économise plus qu'avant, on retient cette position
                                if saving > best_saving:
                                    best_saving = saving
                                    best_pos = pos

                        # 4. Si une vraie amélioration a été trouvée
                        if best_pos is not None and best_saving > 0.001:
                            # On applique définitivement l'insertion dans r2
                            r2.customers.insert(best_pos, customer)
                            r2.current_load += customer.demand
                            r2.total_distance = DistanceService.compute_route_distance(r2, self.instance)

                            improved = True
                            break  # On stoppe la recherche sur cette route pour recommencer un cycle propre
                        else:
                            # Sinon, on annule le retrait de r1
                            r1.customers.insert(c_idx, customer)
                            r1.current_load += customer.demand
                            r1.total_distance = original_r1_dist
                            c_idx += 1

                    if improved:
                        break
                if improved:
                    break

        # Nettoyage : On supprime les routes devenues vides
        initial_routes_count = len(solution.routes)
        solution.routes = [r for r in solution.routes if len(r.customers) > 0]
        solution.total_distance = sum(r.total_distance for r in solution.routes)

        routes_removed = initial_routes_count - len(solution.routes)
        print(f"[RelocateOptimizer] Terminé en {iterations} itérations.")
        if routes_removed > 0:
            print(f"[RelocateOptimizer]  {routes_removed} véhicule(s) économisé(s) !")
            
        return solution