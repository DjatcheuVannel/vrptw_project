from src.services.feasibility_service import FeasibilityService
from src.services.distance_service import DistanceService

class HybridOptimizer:
    def __init__(self, instance):
        self.instance = instance
        self.history = []

    def optimize(self, solution):
        print("\n[HybridOptimizer] Début de l'optimisation (VND : Relocate -> Swap -> 2-Opt)...")
        
        # Nettoyage initial
        solution.routes = [r for r in solution.routes if len(r.customers) > 0]
        self.history = [sum(r.total_distance for r in solution.routes)]
        
        iterations = 0
        improved = True

        # Variable Neighborhood Descent (VND)
        while improved:
            improved = False
            
            # 1. On essore le RELOCATE au maximum (C'est lui qui vide les camions)
            if self._apply_relocate(solution):
                improved = True
                iterations += 1
                self._update_history(solution)
                continue # On recommence la boucle depuis le début
                
            # 2. Si Relocate est bloqué, on tente de débloquer avec un SWAP
            if self._apply_swap(solution):
                improved = True
                iterations += 1
                self._update_history(solution)
                continue # On a débloqué ! On repart sur le Relocate
                
            # 3. Si Swap est bloqué aussi, on lisse avec le 2-OPT
            if self._apply_two_opt(solution):
                improved = True
                iterations += 1
                self._update_history(solution)
                continue

        # Nettoyage final
        solution.routes = [r for r in solution.routes if len(r.customers) > 0]
        solution.total_distance = sum(r.total_distance for r in solution.routes)
        
        print(f"[HybridOptimizer] 🏁 Optimisation terminée. Plus aucune amélioration possible.")
        print(f"   ↳ {iterations} améliorations majeures appliquées.")
        
        return solution, self.history

    def _update_history(self, solution):
        """Met à jour l'historique pour le graphique."""
        current_dist = sum(r.total_distance for r in solution.routes)
        self.history.append(current_dist)

    # ==========================================
    # 1. OPÉRATEUR : RELOCATE SYSTÉMATIQUE
    # ==========================================
    def _apply_relocate(self, solution):
        for r1 in solution.routes:
            for r2 in solution.routes:
                if r1 == r2: continue
                
                # Parcours des clients de r1
                for c_idx, customer in enumerate(r1.customers):
                    
                    # Vérification rapide de capacité
                    if not FeasibilityService.is_capacity_feasible(r2, customer): 
                        continue
                    
                    # Retrait temporaire de r1
                    original_r1_dist = r1.total_distance
                    r1.customers.pop(c_idx)
                    r1.current_load -= customer.demand
                    r1.total_distance = DistanceService.compute_route_distance(r1, self.instance)
                    dist_saved = original_r1_dist - r1.total_distance
                    
                    best_pos, best_saving = None, 0
                    
                    # Test de toutes les positions dans r2
                    for pos in range(len(r2.customers) + 1):
                        if FeasibilityService.is_insertion_time_feasible(r2, customer, pos, self.instance):
                            r2.customers.insert(pos, customer)
                            new_r2_dist = DistanceService.compute_route_distance(r2, self.instance)
                            r2.customers.pop(pos)
                            
                            saving = dist_saved - (new_r2_dist - r2.total_distance)
                            if saving > 0.001 and saving > best_saving:
                                best_saving, best_pos = saving, pos
                                
                    # Application si amélioration
                    if best_pos is not None:
                        r2.customers.insert(best_pos, customer)
                        r2.current_load += customer.demand
                        r2.total_distance = DistanceService.compute_route_distance(r2, self.instance)
                        return True
                    else:
                        # Rollback si aucune position n'est bonne
                        r1.customers.insert(c_idx, customer)
                        r1.current_load += customer.demand
                        r1.total_distance = original_r1_dist
                        
        return False

    # ==========================================
    # 2. OPÉRATEUR : SWAP SYSTÉMATIQUE
    # ==========================================
    def _apply_swap(self, solution):
        for r1 in solution.routes:
            for r2 in solution.routes:
                if r1 == r2: continue
                
                for i, c1 in enumerate(r1.customers):
                    for j, c2 in enumerate(r2.customers):
                        
                        # Vérification des capacités croisées
                        if r1.current_load - c1.demand + c2.demand > self.instance.vehicle_capacity: continue
                        if r2.current_load - c2.demand + c1.demand > self.instance.vehicle_capacity: continue
                        
                        old_dist = r1.total_distance + r2.total_distance
                        
                        # Application du Swap
                        r1.customers[i], r2.customers[j] = c2, c1
                        
                        new_d1 = DistanceService.compute_route_distance(r1, self.instance)
                        new_d2 = DistanceService.compute_route_distance(r2, self.instance)
                        
                        # Vérification de la distance ET des Time Windows
                        if new_d1 + new_d2 < old_dist - 0.001 and self._is_route_time_feasible(r1) and self._is_route_time_feasible(r2):
                            r1.current_load = r1.current_load - c1.demand + c2.demand
                            r2.current_load = r2.current_load - c2.demand + c1.demand
                            r1.total_distance = new_d1
                            r2.total_distance = new_d2
                            return True
                        else:
                            # Rollback
                            r1.customers[i], r2.customers[j] = c1, c2
        return False

    # ==========================================
    # 3. OPÉRATEUR : 2-OPT SYSTÉMATIQUE
    # ==========================================
    def _apply_two_opt(self, solution):
        for route in solution.routes:
            n = len(route.customers)
            if n < 4: continue
            
            for i in range(n - 2):
                for j in range(i + 1, n - 1):
                    old_dist = route.total_distance
                    old_cust = route.customers[:] # Copie de sauvegarde
                    
                    # Inversion du segment
                    route.customers = route.customers[:i] + route.customers[i:j+1][::-1] + route.customers[j+1:]
                    new_dist = DistanceService.compute_route_distance(route, self.instance)
                    
                    # Vérification distance ET Time Windows
                    if new_dist < old_dist - 0.001 and self._is_route_time_feasible(route):
                        route.total_distance = new_dist
                        return True
                    else:
                        # Rollback
                        route.customers = old_cust
        return False

    # --- MÉTHODE DE SÉCURITÉ ---
    def _is_route_time_feasible(self, route):
        """Vérifie l'intégrité absolue des fenêtres de temps après une modification intra/inter-route."""
        current_time = 0
        current_point = route.depot

        for customer in route.customers:
            arrival_time = current_time + self.instance.distance_matrix[current_point.id][customer.id]
            if arrival_time > customer.due_time:
                return False # En retard chez le client
            
            arrival_time = max(arrival_time, customer.ready_time)
            current_time = arrival_time + customer.service_time
            current_point = customer

        # Vérification du retour final
        arrival_time = current_time + self.instance.distance_matrix[current_point.id][route.depot.id]
        if arrival_time > route.depot.due_time:
            return False # En retard au dépôt
            
        return True