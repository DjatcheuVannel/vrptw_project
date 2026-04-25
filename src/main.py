from src.services.parser import Parser
from src.services.distance_service import DistanceService
from src.services.output_service import OutputService
from src.algorithms.solomon_solver import SolomonSolver
from src.algorithms.relocate_optimizer import RelocateOptimizer
from src.algorithms.hybrid_optimizer import HybridOptimizer  # <-- NOUVEL IMPORT
from src.services.visualization_service import VisualizationService

def ask_optimization():
    """Demande à l'utilisateur quelle méthode d'optimisation utiliser."""
    while True:
        print("\n--- CHOIX DE L'OPTIMISATION ---")
        print("0. Aucune")
        print("1. Relocate (Déplacement stochastique)")
        print("2. Hybride (Relocate + Swap + 2-Opt)")
        choice = input("Votre choix (0, 1 ou 2) : ")
        
        if choice == '0': return 'none'
        elif choice == '1': return 'relocate'
        elif choice == '2': return 'hybrid'
        else: print("Entrée invalide.")

def run_full_dataset(parser, opt_choice):
    print("\n=== MODE : DATASET COMPLETE ===")
    instance = parser.parse("data/dataset_large.csv", vehicle_capacity=200, selected_customer_ids=None)
    DistanceService.build_distance_matrix(instance)

    solver = SolomonSolver(instance, candidate_k=20)
    solution = solver.solve()

    # --- SÉLECTION DE L'OPTIMISEUR ---
    if opt_choice == 'relocate':
        optimizer = RelocateOptimizer(instance)
        result = optimizer.optimize(solution)
        solution = result[0] if isinstance(result, tuple) else result
    elif opt_choice == 'hybrid':
        optimizer = HybridOptimizer(instance)
        result = optimizer.optimize(solution)
        solution = result[0] if isinstance(result, tuple) else result
    else:
        print("\n[Info] Calcul terminé sans optimisation locale.")

    all_expected_ids = [c.id for c in instance.customers]

    print("\n=== SOLUTION FINALE ===")
    OutputService.print_solution(solution, expected_ids=all_expected_ids)
    
    print("\n=== GENERATION DES IMAGES ===")
    VisualizationService.plot_solution(solution, instance)


def run_custom_selection(parser, opt_choice):
    print("\n=== MODE : SELECTION MANUELLE ===")
    
    while True:
        try:
            nb = int(input("Combien de clients souhaitez-vous sélectionner (1-200) ? : "))
            if 1 <= nb <= 200: break
            print("Veuillez entrer un nombre entre 1 et 200.")
        except ValueError: print("Entrée invalide.")

    selected_ids = []
    for i in range(nb):
        while True:
            try:
                cid = int(input(f"ID Client {i+1} : "))
                if 1 <= cid <= 200:
                    if cid not in selected_ids:
                        selected_ids.append(cid)
                        break
                    else: print("ID déjà sélectionné.")
                else: print("L'ID doit être entre 1 et 200.")
            except ValueError: print("Entrée invalide.")

    instance = parser.parse("data/dataset_large.csv", vehicle_capacity=200, selected_customer_ids=selected_ids)
    DistanceService.build_distance_matrix(instance)

    solver = SolomonSolver(instance, candidate_k=20)
    solution = solver.solve()

    # --- SÉLECTION DE L'OPTIMISEUR ---
    if opt_choice == 'relocate':
        optimizer = RelocateOptimizer(instance)
        result = optimizer.optimize(solution)
        solution = result[0] if isinstance(result, tuple) else result
    elif opt_choice == 'hybrid':
        optimizer = HybridOptimizer(instance)
        result = optimizer.optimize(solution)
        solution = result[0] if isinstance(result, tuple) else result
    else:
        print("\n[Info] Calcul terminé sans optimisation locale.")

    print("\n=== SOLUTION FINALE ===")
    OutputService.print_solution(solution, expected_ids=selected_ids)
    
    print("\n=== GENERATION DES IMAGES ===")
    VisualizationService.plot_solution(solution, instance)


def main():
    parser = Parser()
    while True:
        print("\n" + "="*30)
        print("         MENU VRPTW")
        print("="*30)
        print("1. Lancer toute la dataset")
        print("2. Choisir les clients manuellement")
        print("3. Quitter")

        choice = input("\nVotre choix : ")
        if choice in ["1", "2"]:
            opt = ask_optimization()
            if choice == "1": run_full_dataset(parser, opt)
            else: run_custom_selection(parser, opt)
        elif choice == "3":
            print("Fin du programme. Au revoir !")
            break
        else:
            print("Choix invalide, veuillez recommencer.")

if __name__ == "__main__":
    main()