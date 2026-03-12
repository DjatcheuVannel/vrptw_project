from src.services.parser import Parser
from src.services.distance_service import DistanceService
from src.services.output_service import OutputService
from src.algorithms.solomon_solver import SolomonSolver


def main():
    parser = Parser()

    print("=== SELECTION DES CLIENTS A LIVRER ===")

    # Demande du nombre de clients
    while True:
        try:
            number_of_customers = int(input("Entrer le nombre de clients à vouloir être livrés : "))

            if 1 <= number_of_customers <= 100:
                break
            else:
                print("Erreur : le nombre de clients doit être compris entre 1 et 100.")
        except ValueError:
            print("Erreur : veuillez entrer un nombre entier valide.")

    # Saisie des IDs clients un par un
    selected_customer_ids = []

    for i in range(number_of_customers):
        while True:
            try:
                customer_id = int(input(f"Entrer le client {i + 1} : "))

                if 1 <= customer_id <= 100:
                    if customer_id not in selected_customer_ids:
                        selected_customer_ids.append(customer_id)
                        break
                    else:
                        print("Erreur : ce client a déjà été choisi.")
                else:
                    print("Erreur : l'identifiant du client doit être compris entre 1 et 100.")
            except ValueError:
                print("Erreur : veuillez entrer un identifiant entier valide.")

    # Lecture du dataset avec seulement les clients choisis
    instance = parser.parse(
        "data/dataset.csv",
        vehicle_capacity=200,
        max_vehicles=25,
        selected_customer_ids=selected_customer_ids
    )

    # Construction de la matrice des distances
    DistanceService.build_distance_matrix(instance)

    # Affichage résumé
    print("\n=== RÉSUMÉ DE L'INSTANCE ===")
    print(f"Nombre de clients retenus : {len(instance.customers)}")
    print(f"Clients retenus : {[customer.id for customer in instance.customers]}")

    # Lancement du solveur
    solver = SolomonSolver(instance, candidate_k=20)
    solution = solver.solve()

    # Affichage de la solution
    print("\n=== SOLUTION TROUVÉE ===")
    OutputService.print_solution(solution)


if __name__ == "__main__":
    main()