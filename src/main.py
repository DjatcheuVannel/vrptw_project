from src.services.parser import Parser
from src.services.distance_service import DistanceService
from src.services.output_service import OutputService
from src.algorithms.solomon_solver import SolomonSolver
from src.services.visualization_service import VisualizationService


def run_full_dataset(parser):
    print("\n=== MODE : DATASET COMPLETE ===")

    instance = parser.parse(
        "data/dataset_large.csv",
        vehicle_capacity=200,
        max_vehicles=25,
        selected_customer_ids=None  # tous les clients
    )

    DistanceService.build_distance_matrix(instance)

    print(f"\nNombre total de clients : {len(instance.customers)}")

    solver = SolomonSolver(instance, candidate_k=20)
    solution = solver.solve()

    # Affichage solution
    print("\n=== SOLUTION TROUVÉE ===")
    OutputService.print_solution(solution)

    # Génération images
    print("\n=== GENERATION DES IMAGES ===")
    VisualizationService.plot_solution(solution, instance)


def run_custom_selection(parser):
    print("\n=== MODE : SELECTION MANUELLE ===")

    # Demande du nombre de clients
    while True:
        try:
            number_of_customers = int(input("Nombre de clients : "))
            if 1 <= number_of_customers <= 100:
                break
            else:
                print("Entre 1 et 100.")
        except ValueError:
            print("Entrée invalide.")

    selected_customer_ids = []

    for i in range(number_of_customers):
        while True:
            try:
                customer_id = int(input(f"Client {i+1} : "))
                if 1 <= customer_id <= 100:
                    if customer_id not in selected_customer_ids:
                        selected_customer_ids.append(customer_id)
                        break
                    else:
                        print("Déjà sélectionné.")
                else:
                    print("ID entre 1 et 100.")
            except ValueError:
                print("Entrée invalide.")

    instance = parser.parse(
        "data/RC201_MTW.csv",
        vehicle_capacity=200,
        max_vehicles=25,
        selected_customer_ids=selected_customer_ids
    )

    DistanceService.build_distance_matrix(instance)

    print("\n=== RÉSUMÉ ===")
    print(f"Clients retenus : {[c.id for c in instance.customers]}")

    solver = SolomonSolver(instance, candidate_k=20)
    solution = solver.solve()

    # Affichage solution
    print("\n=== SOLUTION TROUVÉE ===")
    OutputService.print_solution(solution)

    # Génération images
    print("\n=== GENERATION DES IMAGES ===")
    VisualizationService.plot_solution(solution, instance)


def main():
    parser = Parser()

    while True:
        print("\n==============================")
        print("         MENU VRPTW")
        print("==============================")
        print("1. Lancer toute la dataset")
        print("2. Choisir les clients")
        print("3. Quitter")

        choice = input("Choix : ")

        if choice == "1":
            run_full_dataset(parser)
        elif choice == "2":
            run_custom_selection(parser)
        elif choice == "3":
            print("Fin du programme.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main()