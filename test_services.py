from src.services.parser import Parser
from src.services.distance_service import DistanceService


def test_parser():
    # Création du parser
    parser = Parser()

    # Lecture du fichier CSV
    instance = parser.parse("data/dataset.csv", vehicle_capacity=200, max_vehicles=25)

    # Affichage visuel
    print("=== TEST PARSER ===")
    print("Depot :")
    print(instance.depot)

    print("\nNombre de clients :")
    print(len(instance.customers))

    print("\nPremier client :")
    print(instance.customers[0])

    # Vérifications
    assert instance.depot.id == 0
    assert len(instance.customers) > 0
    assert instance.vehicle_capacity == 200
    assert instance.max_vehicles == 25

    print("\ntest_parser OK\n")


def test_distance_service():
    # Création du parser
    parser = Parser()

    # Lecture du fichier CSV
    instance = parser.parse("data/dataset.csv", vehicle_capacity=200, max_vehicles=25)

    # Construction de la matrice des distances
    DistanceService.build_distance_matrix(instance)

    # Affichage visuel
    print("=== TEST DISTANCE SERVICE ===")
    print("Distance depot -> client 1 :")
    print(instance.distance_matrix[0][1])

    print("\nDistance client 1 -> client 2 :")
    print(instance.distance_matrix[1][2])

    # Vérifications
    assert 0 in instance.distance_matrix
    assert 1 in instance.distance_matrix[0]
    assert instance.distance_matrix[0][0] == 0

    print("\ntest_distance_service OK\n")


def main():
    test_parser()
    test_distance_service()


if __name__ == "__main__":
    main()