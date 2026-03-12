class BaseSolver:
    # Classe mère de tous les solveurs
    def __init__(self, instance):
        # L'instance du problème à résoudre
        self.instance = instance

    # Méthode générique à redéfinir dans les classes filles
    def solve(self):
        # Si une classe fille n'implémente pas cette méthode, on lève une erreur
        raise NotImplementedError("La méthode solve() doit être implémentée dans la classe fille.")