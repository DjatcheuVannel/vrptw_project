import csv
from src.models.customer import Customer
from src.models.depot import Depot
from src.models.instance import VRPTWInstance

class Parser:
    """
    Cette classe lit un fichier CSV et construit une instance VRPTW complète.
    """

    def parse(self, file_path, vehicle_capacity=200, selected_customer_ids=None, default_service_time=2):
        depot = None
        customers = []

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cust_id = int(row["CUST_NO"])
                x = float(row["XCOORD"])
                y = float(row["YCOORD"])
                demand = float(row["DEMAND"])
                ready_time = int(row["READY_TIME_1"])
                due_time = int(row["DUE_TIME_1"])
                service_time = default_service_time

                if cust_id == 0:
                    depot = Depot(
                        x=x,
                        y=y,
                        ready_time=ready_time,
                        due_time=due_time
                    )
                else:
                    customer = Customer(
                        customer_id=cust_id,
                        x=x,
                        y=y,
                        demand=demand,
                        ready_time=ready_time,
                        due_time=due_time,
                        service_time=service_time
                    )
                    customers.append(customer)

        if depot is None:
            raise ValueError("Aucun dépôt trouvé dans le CSV. Il faut une ligne avec CUST_NO = 0.")

        # Filtrage si nécessaire
        if selected_customer_ids is not None:
            customers = [c for c in customers if c.id in selected_customer_ids]

        # Calcul automatique du nombre maximal de véhicules
        total_demand = sum(c.demand for c in customers)
        max_vehicles = int(total_demand / vehicle_capacity) + 1

        instance = VRPTWInstance(
            depot=depot,
            customers=customers,
            vehicle_capacity=vehicle_capacity,
            max_vehicles=max_vehicles
        )

        return instance