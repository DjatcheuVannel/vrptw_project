class Route:
    # Cette classe représente une tournée effectuée par un véhicule
    def __init__(self, vehicle, depot):
        # Véhicule associé à la tournée
        self.vehicle = vehicle

        # Dépôt de départ et de retour
        self.depot = depot

        # Liste des clients visités dans l'ordre
        self.customers = []

        # Charge actuelle transportée
        self.current_load = 0

        # Distance totale de la tournée
        self.total_distance = 0.0

    # Cette méthode ajoute un client à la fin de la route
    def add_customer(self, customer):
        # On ajoute le client dans la liste
        self.customers.append(customer)

        # On met à jour la charge
        self.current_load += customer.demand

    # Cette méthode retourne la liste des identifiants des clients
    def get_customer_ids(self):
        # On extrait seulement les ids pour l'affichage
        return [customer.id for customer in self.customers]

    # Affichage de l'objet
    def __repr__(self):
        return (
            f"Route(vehicle={self.vehicle.id}, customers={self.get_customer_ids()}, "
            f"current_load={self.current_load}, total_distance={self.total_distance})"
        )