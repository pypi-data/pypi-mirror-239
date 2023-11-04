from collections import OrderedDict
from bloqade.ir.routine.base import RoutineBase, __pydantic_dataclass_config__
from bloqade.builder.typing import LiteralType
from bloqade.task.batch import LocalBatch
from beartype import beartype
from beartype.typing import Optional, Tuple
from pydantic.dataclasses import dataclass


@dataclass(frozen=True, config=__pydantic_dataclass_config__)
class BloqadeServiceOptions(RoutineBase):
    def python(self):
        return BloqadePythonRoutine(self.source, self.circuit, self.params)


@dataclass(frozen=True, config=__pydantic_dataclass_config__)
class BloqadePythonRoutine(RoutineBase):
    def _compile(
        self,
        shots: int,
        args: Tuple[LiteralType, ...] = (),
        name: Optional[str] = None,
        blockade_radius: LiteralType = 0.0,
        cache_matrices: bool = False,
    ) -> LocalBatch:
        from bloqade.ir.analysis.assignment_scan import AssignmentScan
        from bloqade.codegen.common.assign_variables import AssignAnalogCircuit
        from bloqade.codegen.emulator_ir import EmulatorProgramCodeGen
        from bloqade.emulate.codegen.hamiltonian import CompileCache
        from bloqade.task.bloqade import BloqadeTask

        circuit, params = self.circuit, self.params

        circuit = AssignAnalogCircuit(params.static_params).visit(circuit)

        if cache_matrices:
            matrix_cache = CompileCache()
        else:
            matrix_cache = None

        tasks = OrderedDict()
        for task_number, batch_param in enumerate(params.batch_assignments(*args)):
            record_params = AssignmentScan(batch_param).emit(circuit)
            final_circuit = AssignAnalogCircuit(record_params).visit(circuit)
            emulator_ir = EmulatorProgramCodeGen(blockade_radius=blockade_radius).emit(
                final_circuit
            )
            metadata = {**params.static_params, **record_params}
            tasks[task_number] = BloqadeTask(shots, emulator_ir, metadata, matrix_cache)

        return LocalBatch(self.source, tasks, name)

    @beartype
    def run(
        self,
        shots: int,
        args: Tuple[LiteralType, ...] = (),
        name: Optional[str] = None,
        blockade_radius: float = 0.0,
        interaction_picture: bool = False,
        cache_matrices: bool = False,
        multiprocessing: bool = False,
        num_workers: Optional[int] = None,
        solver_name: str = "dop853",
        atol: float = 1e-14,
        rtol: float = 1e-7,
        nsteps: int = 2_147_483_647,
    ) -> LocalBatch:
        """Run the current program using bloqade python backend

        Args:
            shots (int): number of shots after running state vector simulation
            args (Tuple[Real, ...], optional): The values for parameters defined
            in `args`. Defaults to ().
            name (Optional[str], optional): Name to give this run. Defaults to None.
            blockade_radius (float, optional): Use the Blockade subspace given a
            particular radius. Defaults to 0.0.
            interaction_picture (bool, optional): Use the interaction picture when
            solving schrodinger equation. Defaults to False.
            cache_matrices (bool, optional): Reuse previously evaluated matrcies when
            possible. Defaults to False.
            multiprocessing (bool, optional): Use multiple processes to process the
            batches. Defaults to False.
            num_workers (Optional[int], optional): Number of processes to run with
            multiprocessing. Defaults to None.
            solver_name (str, optional): Which SciPy Solver to use. Defaults to
            "dop853".
            atol (float, optional): Absolute tolerance for ODE solver. Defaults to
            1e-14.
            rtol (float, optional): Relative tolerance for adaptive step in ODE solver.
            Defaults to 1e-7.
            nsteps (int, optional): Maximum number of steps allowed per integration
            step. Defaults to 2_147_483_647, the maximum value.

        Raises:
            ValueError: Cannot use multiprocessing and cache_matrices at the same time.

        Returns:
            LocalBatch: Batch of local tasks that have been executed.
        """
        if multiprocessing and cache_matrices:
            raise ValueError(
                "Cannot use multiprocessing and cache_matrices at the same time."
            )

        compile_options = dict(
            shots=shots,
            args=args,
            name=name,
            blockade_radius=blockade_radius,
            cache_matrices=cache_matrices,
        )

        solver_options = dict(
            multiprocessing=multiprocessing,
            num_workers=num_workers,
            solver_name=solver_name,
            atol=atol,
            rtol=rtol,
            nsteps=nsteps,
            interaction_picture=interaction_picture,
        )

        batch = self._compile(**compile_options)
        batch._run(**solver_options)

        return batch

    @beartype
    def __call__(
        self,
        *args: LiteralType,
        shots: int = 1,
        name: Optional[str] = None,
        blockade_radius: float = 0.0,
        interaction_picture: bool = False,
        multiprocessing: bool = False,
        num_workers: Optional[int] = None,
        cache_matrices: bool = False,
        solver_name: str = "dop853",
        atol: float = 1e-7,
        rtol: float = 1e-14,
        nsteps: int = 2_147_483_647,
    ):
        options = dict(
            shots=shots,
            args=args,
            name=name,
            blockade_radius=blockade_radius,
            multiprocessing=multiprocessing,
            num_workers=num_workers,
            cache_matrices=cache_matrices,
            solver_name=solver_name,
            atol=atol,
            rtol=rtol,
            nsteps=nsteps,
            interaction_picture=interaction_picture,
        )
        return self.run(**options)
