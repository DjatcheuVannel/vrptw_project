import math


class DistanceService:
    @staticmethod
    def euclidean_distance(point_a, point_b):
        return math.sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)

    @staticmethod
    def build_distance_matrix(instance):
        all_points = [instance.depot] + instance.customers

        for point_i in all_points:
            instance.distance_matrix[point_i.id] = {}

            for point_j in all_points:
                distance = DistanceService.euclidean_distance(point_i, point_j)
                instance.distance_matrix[point_i.id][point_j.id] = distance

    @staticmethod
    def get_distance(instance, from_id, to_id):
        return instance.distance_matrix[from_id][to_id]

    @staticmethod
    def compute_route_distance(route, instance):
        # Si la route est vide, sa distance est nulle
        if not route.customers:
            return 0.0

        total_distance = 0.0

        # Distance dépôt -> premier client
        first_customer = route.customers[0]
        total_distance += instance.distance_matrix[route.depot.id][first_customer.id]

        # Distances entre clients successifs
        for i in range(len(route.customers) - 1):
            current_customer = route.customers[i]
            next_customer = route.customers[i + 1]
            total_distance += instance.distance_matrix[current_customer.id][next_customer.id]

        # Distance dernier client -> dépôt
        last_customer = route.customers[-1]
        total_distance += instance.distance_matrix[last_customer.id][route.depot.id]

        return total_distance