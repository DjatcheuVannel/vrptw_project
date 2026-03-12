from src.algorithms.base_solver import BaseSolver
from src.models.route import Route
from src.models.solution import Solution
from src.models.vehicle import Vehicle
from src.services.feasibility_service import FeasibilityService
from src.services.distance_service import DistanceService


class SolomonSolver(BaseSolver):
    # k = taille de la candidate list
    def __init__(self, instance, candidate_k=20):
        super().__init__(instance)
        self.candidate_k = candidate_k

    # Choix du client seed :
    # on prend ici le client non servi le plus éloigné du dépôt
    def select_seed_customer(self, unserved_customers):
        depot = self.instance.depot

        return max(
            unserved_customers,
            key=lambda customer: self.instance.distance_matrix[depot.id][customer.id]
        )

    # Construit une candidate list de taille k
    # ici : k clients les plus proches du dernier client de la route
    def build_candidate_list(self, route, unserved_customers):
        if not route.customers:
            reference_point = route.depot
        else:
            reference_point = route.customers[-1]

        sorted_customers = sorted(
            unserved_customers,
            key=lambda customer: self.instance.distance_matrix[reference_point.id][customer.id]
        )

        return sorted_customers[:self.candidate_k]

    # Calcule le coût d'insertion de customer entre i et j
    def compute_insertion_cost(self, before_point, customer, after_point):
        d_ik = self.instance.distance_matrix[before_point.id][customer.id]
        d_kj = self.instance.distance_matrix[customer.id][after_point.id]
        d_ij = self.instance.distance_matrix[before_point.id][after_point.id]

        return d_ik + d_kj - d_ij

    # Teste toutes les positions et retourne la meilleure insertion faisable
    def find_best_insertion(self, route, candidate_list):
        best_customer = None
        best_position = None
        best_cost = float("inf")
        best_due_time = float("inf")

        full_route = [route.depot] + route.customers + [route.depot]

        for customer in candidate_list:
            # Vérification capacité
            if not FeasibilityService.is_capacity_feasible(route, customer):
                continue

            # Positions possibles dans route.customers :
            # si route.customers = [a,b,c], alors positions = 0,1,2,3
            # ce qui correspond à :
            # (0,a), (a,b), (b,c), (c,0)
            for position in range(len(route.customers) + 1):
                before_point = full_route[position]
                after_point = full_route[position + 1]

                insertion_cost = self.compute_insertion_cost(before_point, customer, after_point)

                time_feasible = FeasibilityService.is_insertion_time_feasible(
                    route=route,
                    customer=customer,
                    position=position,
                    instance=self.instance
                )

                if not time_feasible:
                    continue

                # Critère principal : plus petit coût
                # Tie-break : plus petit due_time = client plus urgent
                if insertion_cost < best_cost:
                    best_customer = customer
                    best_position = position
                    best_cost = insertion_cost
                    best_due_time = customer.due_time

                elif insertion_cost == best_cost:
                    if customer.due_time < best_due_time:
                        best_customer = customer
                        best_position = position
                        best_cost = insertion_cost
                        best_due_time = customer.due_time

        return best_customer, best_position, best_cost

    def solve(self):
        solution = Solution()
        unserved_customers = self.instance.customers[:]
        vehicle_id = 1

        while unserved_customers and vehicle_id <= self.instance.max_vehicles:
            vehicle = Vehicle(vehicle_id, self.instance.vehicle_capacity)
            route = Route(vehicle, self.instance.depot)

            # Étape A : choix du seed
            seed = self.select_seed_customer(unserved_customers)

            # Vérifie que le seed seul est faisable
            if (
                FeasibilityService.is_capacity_feasible(route, seed)
                and FeasibilityService.is_insertion_time_feasible(route, seed, 0, self.instance)
            ):
                route.customers.insert(0, seed)
                route.current_load += seed.demand
                unserved_customers.remove(seed)
            else:
                # Si même le seed n'est pas faisable, on le retire pour éviter de bloquer
                unserved_customers.remove(seed)
                continue

            # Étape B : insertion progressive
            while True:
                candidate_list = self.build_candidate_list(route, unserved_customers)

                if not candidate_list:
                    break

                best_customer, best_position, best_cost = self.find_best_insertion(route, candidate_list)

                if best_customer is None:
                    break

                route.customers.insert(best_position, best_customer)
                route.current_load += best_customer.demand
                unserved_customers.remove(best_customer)

            # Étape C : fermeture de route
            route.total_distance = DistanceService.compute_route_distance(route, self.instance)
            solution.add_route(route)

            vehicle_id += 1

        return solution