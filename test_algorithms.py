from src.services.parser import Parser
from src.services.distance_service import DistanceService
from src.algorithms.base_solver import BaseSolver
from src.algorithms.solomon_solver import SolomonSolver
from src.models.solution import Solution


def test_base_solver():
    parser = Parser()
    instance = parser.parse("data/R101.csv.csv", vehicle_capacity=200, max_vehicles=25)

    solver = BaseSolver(instance)

    print("=== TEST BASE SOLVER ===")
    print("Instance dans BaseSolver :")
    print(solver.instance)

    assert solver.instance == instance

    try:
        solver.solve()
    except NotImplementedError:
        print("La méthode solve() de BaseSolver lève bien NotImplementedError")
        print("test_base_solver OK\n")
        return

    assert False, "BaseSolver.solve() aurait dû lever NotImplementedError"


def test_solomon_solver():
    parser = Parser()
    instance = parser.parse("data/R101.csv", vehicle_capacity=200, max_vehicles=25)

    DistanceService.build_distance_matrix(instance)

    solver = SolomonSolver(instance, candidate_k=20)
    solution = solver.solve()

    print("=== TEST SOLOMON SOLVER ===")
    print("Solution obtenue :")
    print(solution)

    assert isinstance(solution, Solution)
    assert len(solution.routes) > 0
    assert len(solution.routes) <= instance.max_vehicles
    assert solution.total_distance() > 0

    served_customers = set()

    for route in solution.routes:
        print(route)
        assert len(route.customers) > 0
        assert route.total_distance > 0
        assert route.current_load <= route.vehicle.capacity

        for customer in route.customers:
            served_customers.add(customer.id)

    # Vérifie que tous les clients sont servis une seule fois au total
    assert len(served_customers) == len(instance.customers)

    print("test_solomon_solver OK\n")


def main():
    test_base_solver()
    test_solomon_solver()


if __name__ == "__main__":
    main()