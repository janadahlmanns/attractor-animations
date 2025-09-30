import numpy as np

def lotka_volterra(t_max=40, dt=0.1, 
                   alpha=0.3,   # rabbit growth rate
                   beta=0.15,  # predation rate
                   delta=0.05,  # growth rate of foxes per eaten rabbit
                   gamma=0.3,  # fox death rate
                   R0=5, F0=3): # initial populations
    """
    Simulate Lotka–Volterra predator-prey dynamics.
    Returns arrays: time, rabbits, foxes for finding good parameters
    """
    steps = int(t_max / dt)
    t = np.linspace(0, t_max, steps)
    R = np.zeros(steps)
    F = np.zeros(steps)

    # initial conditions
    R[0] = R0
    F[0] = F0

    for i in range(steps - 1):
        dR = (alpha * R[i] - beta * R[i] * F[i]) * dt
        dF = (delta * R[i] * F[i] - gamma * F[i]) * dt
        R[i+1] = max(R[i] + dR, 0)
        F[i+1] = max(F[i] + dF, 0)

    return t, R, F

# quick test
if __name__ == "__main__":
    t, rabbits, foxes = lotka_volterra()
    print("Rabbits min/max:", rabbits.min(), rabbits.max())
    print("Foxes min/max:", foxes.min(), foxes.max())
