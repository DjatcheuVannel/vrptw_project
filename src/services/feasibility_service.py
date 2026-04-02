class FeasibilityService:
    # Vérifie uniquement la capacité
    @staticmethod
    def is_capacity_feasible(route, customer):
        return route.current_load + customer.demand <= route.vehicle.capacity

    # Retourne la liste des points de la route sous la forme [depot, clients..., depot]
    @staticmethod
    def build_full_route(route):
        return [route.depot] + route.customers + [route.depot]

    # 🔥 NOUVEAU : gestion des 3 fenêtres de temps
    @staticmethod
    def compute_start_service_multi(arrival_time, time_windows):
        """
        time_windows = [(a1,b1), (a2,b2), (a3,b3)]
        Retourne le meilleur start_service possible ou None si impossible
        """

        best_start = None
        min_wait = float("inf")

        for (start, end) in time_windows:
            if arrival_time <= end:
                wait = max(0, start - arrival_time)

                if wait < min_wait:
                    min_wait = wait
                    best_start = max(arrival_time, start)

        return best_start  # None si aucune fenêtre valide

    # Simule complètement la route et vérifie les fenêtres de temps
    @staticmethod
    def is_sequence_time_feasible(sequence, instance):
        current_time = sequence[0].ready_time

        for i in range(len(sequence) - 1):
            current_point = sequence[i]
            next_point = sequence[i + 1]

            travel_time = instance.distance_matrix[current_point.id][next_point.id]
            arrival_time = current_time + travel_time

            # 🔥 NOUVEAU : gestion multi-fenêtres
            if hasattr(next_point, "time_windows") and next_point.time_windows:
                service_start = FeasibilityService.compute_start_service_multi(
                    arrival_time,
                    sorted(next_point.time_windows, key=lambda x: x[0])
                )

                if service_start is None:
                    return False

            # 🔁 Ancien comportement (fallback)
            else:
                service_start = max(arrival_time, next_point.ready_time)

                if service_start > next_point.due_time:
                    return False

            current_time = service_start + next_point.service_time

        return True

    # Vérifie la faisabilité d'une insertion d'un client à une position donnée
    @staticmethod
    def is_insertion_time_feasible(route, customer, position, instance):
        full_route = FeasibilityService.build_full_route(route)

        insertion_index = position + 1

        new_sequence = full_route[:insertion_index] + [customer] + full_route[insertion_index:]

        return FeasibilityService.is_sequence_time_feasible(new_sequence, instance)

    # Conserve une version simple si tu veux tester juste en fin de route
    @staticmethod
    def is_time_feasible(route, customer, instance):
        return FeasibilityService.is_insertion_time_feasible(
            route=route,
            customer=customer,
            position=len(route.customers),
            instance=instance
        )