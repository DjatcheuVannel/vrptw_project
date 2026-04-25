from src.algorithms.base_solver import BaseSolver
from src.models.route import Route
from src.models.solution import Solution
from src.models.vehicle import Vehicle
from src.services.feasibility_service import FeasibilityService
from src.services.distance_service import DistanceService


class SolomonSolver(BaseSolver):

    def __init__(self, instance, candidate_k=20):
        super().__init__(instance)
        self.candidate_k = candidate_k

    # Choix du seed : client le plus éloigné du dépôt
    def select_seed_customer(self, unserved_customers):
        depot = self.instance.depot

        return max(
            unserved_customers,
            key=lambda customer: self.instance.distance_matrix[depot.id][customer.id]
        )

    # Liste des k clients les plus proches
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

    # Coût d’insertion
    def compute_insertion_cost(self, before_point, customer, after_point):
        d_ik = self.instance.distance_matrix[before_point.id][customer.id]
        d_kj = self.instance.distance_matrix[customer.id][after_point.id]
        d_ij = self.instance.distance_matrix[before_point.id][after_point.id]

        return d_ik + d_kj - d_ij

    # Trouver meilleure insertion
    def find_best_insertion(self, route, customers_to_test):
        best_customer = None
        best_position = None
        best_cost = float("inf")
        best_due_time = float("inf")

        full_route = [route.depot] + route.customers + [route.depot]

        for customer in customers_to_test:

            if not FeasibilityService.is_capacity_feasible(route, customer):
                continue

            for position in range(len(route.customers) + 1):
                before_point = full_route[position]
                after_point = full_route[position + 1]

                insertion_cost = self.compute_insertion_cost(
                    before_point, customer, after_point
                )

                if not FeasibilityService.is_insertion_time_feasible(
                    route, customer, position, self.instance
                ):
                    continue

                if insertion_cost < best_cost:
                    best_customer = customer
                    best_position = position
                    best_cost = insertion_cost
                    best_due_time = customer.due_time

                elif insertion_cost == best_cost:
                    if customer.due_time < best_due_time:
                        best_customer = customer
                        best_position = position
                        best_due_time = customer.due_time

        return best_customer, best_position, best_cost

    # ============================
    # SOLVE AMÉLIORÉ
    # ============================
    def solve(self):
        solution = Solution()
        unserved_customers = self.instance.customers[:]
        vehicle_id = 1

        while unserved_customers:

            vehicle = Vehicle(vehicle_id, self.instance.vehicle_capacity)
            route = Route(vehicle, self.instance.depot)

            # Étape A : seed
            seed = self.select_seed_customer(unserved_customers)

            route.customers.append(seed)
            route.current_load += seed.demand
            unserved_customers.remove(seed)

            # Étape B : insertions
            while True:

                # 1️⃣ Essai avec candidate list (rapide)
                candidate_list = self.build_candidate_list(route, unserved_customers)

                best_customer, best_position, _ = self.find_best_insertion(
                    route, candidate_list
                )

                # 2️⃣ 🔥 Si échec → essayer TOUS les clients
                if best_customer is None:
                    best_customer, best_position, _ = self.find_best_insertion(
                        route, unserved_customers
                    )

                # 3️⃣ Si toujours rien → fin de route
                if best_customer is None:
                    break

                route.customers.insert(best_position, best_customer)
                route.current_load += best_customer.demand
                unserved_customers.remove(best_customer)

            # Étape C : finalisation
            route.total_distance = DistanceService.compute_route_distance(
                route, self.instance
            )
            solution.add_route(route)

            vehicle_id += 1

        return solution