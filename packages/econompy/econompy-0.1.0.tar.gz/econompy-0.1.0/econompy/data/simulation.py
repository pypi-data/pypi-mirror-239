import numpy as np
import pandas as pd


class Simulation:
    def __init__(self, name: str = "my_simulation", seed: int = 42) -> None:
        """Create an instance of a simulation object.

        Args:
            name (str, optional): The name of the simulation object, can be used for versioning.
            seed (int, optional): The seed for the random number generator.
        """
        self.name = name
        np.random.seed(seed)

    def generate_data(self, n: int = 1000) -> pd.DataFrame:
        """Generate data for the simulation.

        Args:
            n (int, optional): The number of observations to generate.

        Returns:
            pd.DataFrame: The generated data.
        """
        return pd.DataFrame({"x": np.random.normal(size=n), "y": np.random.normal(size=n)})
