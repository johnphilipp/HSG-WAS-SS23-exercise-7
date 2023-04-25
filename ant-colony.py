import numpy as np
import random
from environment import Environment
from ant import Ant
import matplotlib.pyplot as plt
from typing import List, Tuple


class AntColony:
    def __init__(
        self,
        ant_population: int,
        iterations: int,
        alpha: float,
        beta: float,
        rho: float,
    ):
        self.ant_population: int = ant_population
        self.iterations: int = iterations
        self.alpha: float = alpha
        self.beta: float = beta
        self.rho: float = rho

        self.environment: Environment = Environment(self.rho, self.ant_population)
        self.pheromone_map: np.ndarray = self.environment.get_pheromone_map()
        self.best_solution: np.ndarray = np.zeros(
            (
                self.environment.get_locations_count(),
                self.environment.get_locations_count(),
            )
        )
        self.ants: List[Ant] = []

    def solve(self, debug: bool) -> Tuple[List[int], float]:
        shortest_distance = np.inf
        initial_distance = None
        final_distance = None
        assigned_locations = set()

        for iteration in range(self.iterations):
            ants_data = []
            for ant_number in range(self.ant_population):
                initial_location = self.get_initial_location(assigned_locations)

                ant = Ant(self.alpha, self.beta, initial_location)
                ant.join(self.environment)
                ant.run()
                ant_data = ant.get_ant_data()
                ants_data.append(ant_data)

                sum_distance = ant_data[1]
                ant_visited_locations = ant_data[2]

                if iteration == 0 and ant_number == 0:
                    initial_distance = sum_distance

                if sum_distance < shortest_distance:
                    shortest_distance = sum_distance
                    solution = ant_visited_locations
                    final_distance = sum_distance

                self.update_best_solution(ant_data[0], ant_visited_locations)
                self.ants.append(ant)

            self.environment.update_pheromone_map(self.best_solution)

            # Move printing statements outside the inner loop
            if debug:
                for ant_number, ant_data in enumerate(ants_data):
                    print(f"Iteration: {iteration + 1}")
                    print(f"Ant: {ant_number + 1}")
                    print(f"Traveled: {ant_data[0]}")
                    print(f"Visited: {ant_data[2]}")
                    print(f"Distance: {ant_data[1]}\n")

        distance_reduction = (
            (initial_distance - final_distance) / initial_distance
        ) * 100
        print(f"Initial distance: {initial_distance}")
        print(f"Final distance: {final_distance}")
        print(f"Distance reduction: {distance_reduction:.2f}%\n")

        return solution, shortest_distance

    def get_initial_location(self, assigned_locations) -> int:
        unassigned_locations = (
            set(range(self.environment.get_locations_count())) - assigned_locations
        )
        if unassigned_locations:
            initial_location = random.choice(list(unassigned_locations))
            assigned_locations.add(initial_location)
        else:
            initial_location = random.randint(
                0, self.environment.get_locations_count() - 1
            )
        return initial_location

    def update_best_solution(self, ant_travel_distance, ant_visited_locations) -> None:
        location_pairs = zip(ant_visited_locations[:-1], ant_visited_locations[1:])
        pheromone_updates = [1 / distance for distance in ant_travel_distance[1:]]

        for (location, next_location), pheromone_update in zip(
            location_pairs, pheromone_updates
        ):
            self.best_solution[location][next_location] += pheromone_update
            self.best_solution[next_location][location] += pheromone_update


def plot_solution(solution, environment) -> None:
    x_coords = []
    y_coords = []

    for location in solution:
        x, y = environment.get_location(location)
        x_coords.append(x)
        y_coords.append(y)

    # Add the starting location to close the loop
    start_x, start_y = environment.get_location(solution[0])
    x_coords.append(start_x)
    y_coords.append(start_y)

    plt.plot(x_coords, y_coords, "bo-", linewidth=2, markersize=8)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Ant Colony Optimization Solution")
    plt.grid(True)
    plt.show()


def main() -> None:
    ant_colony = AntColony(ant_population=48, iterations=100, alpha=2, beta=1, rho=0.05)
    print("Solving...\n")
    solution, distance = ant_colony.solve(debug=False)
    print(f"SOLUTION: {solution}")
    print(f"DISTANCE: {distance}")
    plot_solution(solution, ant_colony.environment)


if __name__ == "__main__":
    main()
