class VRPTWInstance:
    # Cette classe représente toute l'instance du problème
    def __init__(self, depot, customers, vehicle_capacity, max_vehicles):
        # Dépôt principal
        self.depot = depot

        # Liste des clients
        self.customers = customers

        # Capacité maximale des véhicules
        self.vehicle_capacity = vehicle_capacity

        # Nombre maximal de véhicules
        self.max_vehicles = max_vehicles

        # Matrice de distances entre points
        self.distance_matrix = {}

    # Cette méthode retourne le nombre de clients
    def customer_count(self):
        # On retourne la taille de la liste
        return len(self.customers)

    # Affichage de l'objet
    def __repr__(self):
        return (
            f"VRPTWInstance(customers={len(self.customers)}, "
            f"vehicle_capacity={self.vehicle_capacity}, max_vehicles={self.max_vehicles})"
        )