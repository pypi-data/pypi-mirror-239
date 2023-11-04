import bloqade.ir.location as location
from bloqade import start, load, save

from bloqade.ir import Linear, Constant
import numpy as np


prog = (
    location.Square(6)
    .rydberg.detuning.uniform.apply(
        Constant("initial_detuning", "up_time")
        .append(Linear("initial_detuning", "final_detuning", "anneal_time"))
        .append(Constant("final_detuning", "up_time"))
    )
    .rabi.amplitude.uniform.apply(
        Linear(0.0, "rabi_amplitude_max", "up_time")
        .append(Constant("rabi_amplitude_max", "anneal_time"))
        .append(Linear("rabi_amplitude_max", 0.0, "up_time"))
    )
    .assign(initial_detuning=-10, up_time=0.1, anneal_time=3.8, rabi_amplitude_max=15)
    .batch_assign(final_detuning=np.linspace(0, 10, 5))
)
task = prog.quera.mock()


# future = task.run_async(shots=100)  ## non0-blk

# future.fetch()

# assert len(future.tasks) == 5

# print(future.report())


def test_serializer():
    batch = (
        start.add_position((0, 0))
        .rydberg.detuning.uniform.piecewise_linear(
            [0.1, 0.5, 0.1], [1.0, 2.0, 3.0, 4.0]
        )
        .constant(4.0, 1)
        .braket.local_emulator()
        .run(1)
    )

    save(batch, "test.json")
    new_batch = load("test.json")
    assert batch.tasks == new_batch.tasks
