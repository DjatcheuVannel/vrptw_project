class Customer:
    # Cette classe représente un client à livrer
    def __init__(self, customer_id, x, y, demand, ready_time, due_time, service_time=2):
        # Identifiant unique du client
        self.id = customer_id

        # Coordonnée x du client
        self.x = x

        # Coordonnée y du client
        self.y = y

        # Quantité demandée par le client
        self.demand = demand

        # Début de la fenêtre de temps
        self.ready_time = ready_time

        # Fin de la fenêtre de temps
        self.due_time = due_time

        # Temps de service chez le client
        self.service_time = service_time

    # Cette méthode permet d'afficher facilement l'objet
    def __repr__(self):
        return (
            f"Customer(id={self.id}, x={self.x}, y={self.y}, demand={self.demand}, "
            f"ready_time={self.ready_time}, due_time={self.due_time}, service_time={self.service_time})"
        )