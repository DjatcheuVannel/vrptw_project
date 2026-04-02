import matplotlib.pyplot as plt
import os
import shutil

class VisualizationService:

    @staticmethod
    def compute_schedule(route, instance):
        """
        Calcule les heures d'arrivée et de départ pour chaque point de la route
        """
        schedule = []

        current_time = 0
        current_point = route.depot

        # Départ du dépôt
        schedule.append((current_point, 0, 0))

        for customer in route.customers:
            travel_time = instance.distance_matrix[current_point.id][customer.id]

            arrival_time = current_time + travel_time

            # Respect de la fenêtre de temps
            if arrival_time < customer.ready_time:
                arrival_time = customer.ready_time

            departure_time = arrival_time + customer.service_time

            schedule.append((customer, arrival_time, departure_time))

            # Mise à jour
            current_time = departure_time
            current_point = customer

        # Retour au dépôt
        travel_time = instance.distance_matrix[current_point.id][route.depot.id]
        arrival_time = current_time + travel_time

        schedule.append((route.depot, arrival_time, arrival_time))

        return schedule

    @staticmethod
    def clear_plot_folder(folder_path):
        """
        Supprime et recrée le dossier pour éviter les anciennes images
        """
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)

    @staticmethod
    def plot_solution(solution, instance, output_folder="plots"):
        """
        Génère les images des routes
        """
        # ✅ Nettoyage du dossier
        VisualizationService.clear_plot_folder(output_folder)

        for idx, route in enumerate(solution.routes, 1):
            plt.figure(figsize=(12, 8))
            plt.grid(True, linestyle='--', alpha=0.4, zorder=0)

            full_route = [route.depot] + route.customers + [route.depot]
            schedule = VisualizationService.compute_schedule(route, instance)

            # Flèches avec courbure
            for i in range(len(full_route) - 1):
                p1 = full_route[i]
                p2 = full_route[i + 1]

                courbure = 0.15 if i % 2 == 0 else -0.15

                plt.annotate(
                    "",
                    xy=(p2.x, p2.y), xycoords='data',
                    xytext=(p1.x, p1.y), textcoords='data',
                    arrowprops=dict(
                        arrowstyle="-|>",
                        color="dimgray",
                        lw=1.5,
                        shrinkA=15,
                        shrinkB=15,
                        connectionstyle=f"arc3,rad={courbure}"
                    ),
                    zorder=2
                )

            # Clients
            cust_x = [p.x for p in route.customers]
            cust_y = [p.y for p in route.customers]
            plt.scatter(cust_x, cust_y, c='dodgerblue', marker='o', s=80, edgecolors='black', zorder=3)

            # Dépôt
            plt.scatter(route.depot.x, route.depot.y, c='crimson', marker='s', s=120, edgecolors='black', zorder=4)

            # Annotations
            bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="lightgray", lw=1, alpha=0.9)

            plt.text(route.depot.x, route.depot.y - 1.0, "DÉPÔT",
                     fontsize=9, fontweight='bold', color='crimson',
                     ha='center', va='top', bbox=bbox_props, zorder=5)

            for (point, arrival, departure) in schedule:
                if point.id == route.depot.id:
                    label = f"Retour\nA: {round(arrival, 1)}"
                    plt.text(point.x + 1.5, point.y + 0.5, label,
                             fontsize=8, ha='left', va='center',
                             bbox=bbox_props, zorder=5)
                else:
                    label = f"ID: {point.id}\nA: {round(arrival, 1)} | D: {round(departure, 1)}"
                    plt.text(point.x, point.y + 1.2, label,
                             fontsize=8, ha='center', va='bottom',
                             bbox=bbox_props, zorder=5)

            plt.title(f"Route {idx}", fontsize=14, fontweight='bold', pad=15)
            plt.xlabel("Coordonnée X", fontsize=10)
            plt.ylabel("Coordonnée Y", fontsize=10)
            plt.tight_layout()

            filename = f"{output_folder}/route_{idx}.png"
            plt.savefig(filename, dpi=150)
            plt.close()

            print(f"Image sauvegardée : {filename}")