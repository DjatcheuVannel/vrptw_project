class Vehicle:
    # Cette classe représente un véhicule
    def __init__(self, vehicle_id, capacity):
        # Identifiant du véhicule
        self.id = vehicle_id

        # Capacité maximale du véhicule
        self.capacity = capacity

    # Affichage de l'objet
    def __repr__(self):
        return f"Vehicle(id={self.id}, capacity={self.capacity})"