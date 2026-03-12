class Solution:
    # Cette classe représente la solution complète
    def __init__(self):
        # Une solution contient plusieurs routes
        self.routes = []

    # Cette méthode ajoute une route à la solution
    def add_route(self, route):
        # On ajoute la route à la liste
        self.routes.append(route)

    # Cette méthode calcule la distance totale de la solution
    def total_distance(self):
        # On additionne la distance de chaque route
        return sum(route.total_distance for route in self.routes)

    # Cette méthode retourne le nombre de véhicules utilisés
    def vehicles_used(self):
        # Chaque route correspond à un véhicule utilisé
        return len(self.routes)

    # Affichage de l'objet
    def __repr__(self):
        return (
            f"Solution(routes={len(self.routes)}, "
            f"total_distance={self.total_distance()}, vehicles_used={self.vehicles_used()})"
        )