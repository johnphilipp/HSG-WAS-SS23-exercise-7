import tsplib95
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
from typing import List, Tuple, Dict


class Environment:
    def __init__(self, rho, ant_population):
        self.rho = rho
        self.ant_population = ant_population

        self.problem = tsplib95.load("att48-specs/att48.tsp")
        self.node_coords: Dict[int, Tuple[float, float]] = self.problem.node_coords
        self.n_nodes: int = len(self.problem.node_coords)
        self.possible_locations: List[int] = list(range(self.n_nodes))

        self.pheromone_map: np.ndarray = self.initialize_pheromone_map()

    def initialize_pheromone_map(self) -> np.ndarray:
        def _calc_distance(coord1, coord2):
            coord_x_1, coord_y_1 = coord1
            coord_x_2, coord_y_2 = coord2
            return math.ceil(
                math.sqrt(
                    (
                        math.pow((coord_x_1 - coord_x_2), 2)
                        + math.pow((coord_y_1 - coord_y_2), 2)
                    )
                    / 10.0
                )
            )

        distance_map = np.zeros((self.n_nodes, self.n_nodes))
        for i in range(self.n_nodes):
            for j in range(i, self.n_nodes):
                dist = _calc_distance(self.node_coords[i + 1], self.node_coords[j + 1])
                distance_map[i][j] = dist
                distance_map[j][i] = dist

        self.distance_map = distance_map

        pheromone_map = np.zeros((self.n_nodes, self.n_nodes))
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                if i != j:
                    pheromone_map[i][j] = self.ant_population / distance_map[i][j]

        np.fill_diagonal(pheromone_map, 0)
        return pheromone_map

    def update_pheromone_map(self, better_solution) -> None:
        self.pheromone_map = self.pheromone_map * self.rho
        self.pheromone_map = self.pheromone_map + better_solution

    def get_pheromone_map(self) -> np.ndarray:
        return self.pheromone_map

    def get_possible_locations(self) -> np.ndarray:
        return self.possible_locations

    def get_locations_count(self) -> int:
        return self.n_nodes

    def get_location(self, location) -> Dict[int, Tuple[float, float]]:
        return self.node_coords[location + 1]
