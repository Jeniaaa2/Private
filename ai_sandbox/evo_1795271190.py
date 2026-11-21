import math
import random

# Parameters for the quantum superposition engine simulation
num_states = 10          # number of quantum states in the superposition
iterations = 5           # number of parallel cycles
amplitude_scale = 0.1    # scaling factor for amplitude adjustments

# Initialize the state vector with equal superposition amplitudes
state_vector = [1 / math.sqrt(num_states) for _ in range(num_states)]

def apply_gate(state, gate):
    """Simulate a simple unitary gate by rotating amplitudes."""
    new_state = [0] * len(state)
    for i, amp in enumerate(state):
        target = (i + gate) % len(state)
        new_state[target] += amp * amplitude_scale
    # normalize
    norm = math.sqrt(sum(a*a for a in new_state))
    return [a / norm for a in new_state]

def parallel_cycle(state_vector):
    """Run a parallel cycle: apply random gates to subsets of the states."""
    # Split into two halves
    mid = len(state_vector) // 2
    left = apply_gate(state_vector[:mid], random.randint(1,3))
    right = apply_gate(state_vector[mid:], random.randint(1,3))
    # Combine
    return left + right

for _ in range(iterations):
    state_vector = parallel_cycle(state_vector)

# Compute probabilities and determine the most probable state
probabilities = [a*a for a in state_vector]
most_likely = probabilities.index(max(probabilities))

print("Final state vector:", state_vector)
print("Probabilities:", probabilities)
print("Most likely state index:", most_likely)