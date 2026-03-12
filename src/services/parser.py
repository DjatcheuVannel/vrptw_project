import csv

from src.models.customer import Customer
from src.models.depot import Depot
from src.models.instance import VRPTWInstance


class Parser:
    # Cette classe lit le fichier CSV et construit les objets du problème
    def parse(self, file_path, vehicle_capacity=200, max_vehicles=25, selected_customer_ids=None):
        depot = None
        customers = []

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cust_id = int(row["CUST_NO"])
                x = float(row["XCOORD"])
                y = float(row["YCOORD"])
                demand = float(row["DEMAND"])

                # Pour l'instant, on utilise seulement la première fenêtre
                ready_time = int(row["READY_TIME_1"])
                due_time = int(row["DUE_TIME_1"])
                service_time = 0

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

        # Si l'utilisateur a choisi certains clients, on filtre
        if selected_customer_ids is not None:
            customers = [customer for customer in customers if customer.id in selected_customer_ids]

        instance = VRPTWInstance(
            depot=depot,
            customers=customers,
            vehicle_capacity=vehicle_capacity,
            max_vehicles=max_vehicles
        )

        return instance