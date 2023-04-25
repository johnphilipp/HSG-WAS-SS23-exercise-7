import math
import numpy as np
from typing import List, Tuple


class Ant:
    def __init__(self, alpha: float, beta: float, initial_location):
        self.alpha: float = alpha
        self.beta: float = beta
        self.current_location: int = initial_location
        self.travelled_distance: List[float] = [0]
        self.visited_locations: List[int] = [initial_location]

    def run(self) -> None:
        self.possible_locations = self.environment.get_possible_locations().copy()

        while self.possible_locations:
            if self.current_location in self.possible_locations:
                self.possible_locations.remove(self.current_location)

            if self.possible_locations:
                self.select_path()

    def select_path(self) -> None:
        def _calc_distance(location1, location2):
            coord_x_1, coord_y_1 = self.environment.get_location(location1)
            coord_x_2, coord_y_2 = self.environment.get_location(location2)
            return math.ceil(
                math.sqrt(
                    (
                        math.pow((coord_x_1 - coord_x_2), 2)
                        + math.pow((coord_y_1 - coord_y_2), 2)
                    )
                    / 10.0
                )
            )

        self.pheromone_map = self.environment.get_pheromone_map()

        numerators = [
            self.calculate_numerator(possible_location)
            for possible_location in self.possible_locations
        ]
        total_prob = sum(numerators)
        prob_list = [num / total_prob for num in numerators]

        future_location = np.random.choice(self.possible_locations, p=prob_list)

        distance = _calc_distance(self.current_location, future_location)
        self.travelled_distance.append(distance)
        self.current_location = future_location
        self.visited_locations.append(self.current_location)
        self.possible_locations.remove(self.current_location)

    def join(self, environment) -> None:
        self.environment = environment

    def get_ant_data(self) -> Tuple[List[float], float, List[int]]:
        return (
            self.travelled_distance,
            sum(self.travelled_distance),
            self.visited_locations,
        )

    def calculate_numerator(self, possible_location: int) -> float:
        current_to_j = (
            self.pheromone_map[self.current_location][possible_location] ** self.alpha
        ) * (
            self.environment.distance_map[self.current_location][possible_location]
            ** self.beta
        )
        return current_to_j
