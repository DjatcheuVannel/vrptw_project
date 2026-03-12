from src.models.customer import Customer
from src.models.depot import Depot
from src.models.vehicle import Vehicle
from src.models.route import Route
from src.models.solution import Solution
from src.models.instance import VRPTWInstance


def test_customer():
    # Création d'un client
    customer = Customer(1, 45.0, 68.0, 10.0, 690, 750, 0)

    # Vérifications
    assert customer.id == 1
    assert customer.x == 45.0
    assert customer.y == 68.0
    assert customer.demand == 10.0
    assert customer.ready_time == 690
    assert customer.due_time == 750
    assert customer.service_time == 0

    print("test_customer OK")


def test_depot():
    # Création du dépôt
    depot = Depot(40.0, 50.0, 0, 960)

    # Vérifications
    assert depot.id == 0
    assert depot.x == 40.0
    assert depot.y == 50.0
    assert depot.ready_time == 0
    assert depot.due_time == 960
    assert depot.service_time == 0

    print("test_depot OK")


def test_vehicle():
    # Création d'un véhicule
    vehicle = Vehicle(1, 200)

    # Vérifications
    assert vehicle.id == 1
    assert vehicle.capacity == 200

    print("test_vehicle OK")


def test_route():
    # Création des objets nécessaires
    depot = Depot(40.0, 50.0, 0, 960)
    vehicle = Vehicle(1, 200)
    customer1 = Customer(1, 45.0, 68.0, 10.0, 690, 750, 0)
    customer2 = Customer(2, 45.0, 70.0, 30.0, 750, 810, 0)

    # Création de la route
    route = Route(vehicle, depot)

    # Vérification initiale
    assert route.vehicle == vehicle
    assert route.depot == depot
    assert route.customers == []
    assert route.current_load == 0

    # Ajout de clients
    route.add_customer(customer1)
    route.add_customer(customer2)

    # Vérifications après ajout
    assert len(route.customers) == 2
    assert route.customers[0] == customer1
    assert route.customers[1] == customer2
    assert route.current_load == 40.0

    print("test_route OK")


def test_solution():
    # Création des objets nécessaires
    depot = Depot(40.0, 50.0, 0, 960)
    vehicle = Vehicle(1, 200)
    customer = Customer(1, 45.0, 68.0, 10.0, 690, 750, 0)

    route = Route(vehicle, depot)
    route.add_customer(customer)

    solution = Solution()
    solution.add_route(route)

    # Vérifications
    assert len(solution.routes) == 1
    assert solution.routes[0] == route

    print("test_solution OK")


def test_instance():
    # Création des objets nécessaires
    depot = Depot(40.0, 50.0, 0, 960)
    customer1 = Customer(1, 45.0, 68.0, 10.0, 690, 750, 0)
    customer2 = Customer(2, 45.0, 70.0, 30.0, 750, 810, 0)

    customers = [customer1, customer2]

    instance = VRPTWInstance(depot, customers, 200, 25)

    # Vérifications
    assert instance.depot == depot
    assert len(instance.customers) == 2
    assert instance.vehicle_capacity == 200
    assert instance.max_vehicles == 25

    print("test_instance OK")


def main():
    # Exécution de tous les tests
    test_customer()
    test_depot()
    test_vehicle()
    test_route()
    test_solution()
    test_instance()

    print("\nTous les tests des modèles sont passés avec succès.")


if __name__ == "__main__":
    main()