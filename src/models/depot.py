class Depot:
    # Cette classe représente le dépôt
    def __init__(self, x, y, ready_time, due_time):
        # Par convention, le dépôt a l'identifiant 0
        self.id = 0

        # Coordonnée x du dépôt
        self.x = x

        # Coordonnée y du dépôt
        self.y = y

        # Début de disponibilité du dépôt
        self.ready_time = ready_time

        # Fin de disponibilité du dépôt
        self.due_time = due_time

        # Pas de temps de service au dépôt dans cette version
        self.service_time = 0

    # Affichage de l'objet
    def __repr__(self):
        return (
            f"Depot(id={self.id}, x={self.x}, y={self.y}, "
            f"ready_time={self.ready_time}, due_time={self.due_time})"
        )