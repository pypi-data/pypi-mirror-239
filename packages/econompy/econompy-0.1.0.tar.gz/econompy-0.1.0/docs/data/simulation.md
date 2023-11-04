# Simulation

You can generate a simulation of data using the `econompy.data.Simulation` class.

> In many cases I experienced that whenever you visually inspect a dataset, you can see patterns that you would like to test and develop theories that you want to analyze.

Mostly from prior knowledge and literature search you already have a good idea how relationships in you data dimensions should look like. In this case you can use the `econompy.data.Simulation` class to generate a dataset that fits your expectations and already start to test your theories. Through that you can already start to develop your analysis. The ideal case is that after obtaining the *real dataset* you can just plug it in and re-run your already implemented analysis.

It also helps to get a better understanding of the data generating process and the underlying assumptions.

## Example Usage

```python
from econompy.data import Simulation

sim = Simulation(name="v001", seed=42)
df = sim.generate(n=10000)
```

::: econompy.data.Simulation
