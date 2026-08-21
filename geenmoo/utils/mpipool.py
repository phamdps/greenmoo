# Copyright 2015-2024 David Hadka
#
# This file is part of Platypus, a Python module for designing and using
# evolutionary algorithms (EAs) and multiobjective evolutionary algorithms
# (MOEAs).
#
# Platypus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Platypus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Platypus.  If not, see <http://www.gnu.org/licenses/>.

import sys
import traceback


class MPIPoolException(Exception):
    """Exception raised by MPIPool when an error occurs on a worker process."""

    def __init__(self, tb):
        self.tb = tb
        super().__init__(self.tb)

    def __str__(self):
        return self.tb


def _error_function(task):
    raise NotImplementedError("MPIPool worker function not initialized.")


class MPIPool:
    """A pool that distributes tasks over a set of MPI processes using mpi4py.

    MPI is an API for distributed memory parallelism, used by large cluster
    computers. This class provides a similar interface to Python's
    multiprocessing Pool, but currently only supports the map() method.
    """

    def __init__(self, comm=None, debug=False, loadbalance=False):
        # LAZY IMPORT: mpi4py is imported ONLY when MPIPool is instantiated.
        # This prevents normal scripts from hanging or crashing on import.
        try:
            from mpi4py import MPI
        except (ImportError, RuntimeError) as e:
            raise RuntimeError(
                "mpi4py is not installed or the underlying MPI library (libmpi.so) "
                "is missing. Install openmpi and mpi4py, or use MapEvaluator for "
                "sequential/local execution."
            ) from e

        self.MPI = MPI
        self.comm = self.MPI.COMM_WORLD if comm is None else comm
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size() - 1
        self.debug = debug
        self.function = _error_function
        self.loadbalance = loadbalance

        if self.size == 0:
            raise ValueError(
                "Tried to create an MPI pool, but there was only one MPI process available. "
                "Did you forget to launch your script with 'mpiexec -n <N> python ...'?"
            )

    def is_master(self):
        """Returns True if the current process is the master process."""
        return self.rank == 0

    def bcast(self, *args, **kwargs):
        """Equivalent to mpi4py bcast() collective operation."""
        return self.comm.bcast(*args, **kwargs)

    def map(self, function, tasks, callback=None):
        """Like the built-in map() function, apply a function to all values

        in a list and return the list of results.
        """
        task_list = list(tasks)

        if not self.is_master():
            raise RuntimeError("Only the master process can call map().")

        if self.debug:
            print(f"Master distributing {len(task_list)} tasks to {self.size} workers.")

        # Broadcast the function and tasks to workers
        self.comm.bcast((function, task_list), root=0)

        results = []
        for _ in range(len(task_list)):
            result = self.comm.recv(source=self.MPI.ANY_SOURCE)
            if isinstance(result, MPIPoolException):
                raise result
            results.append(result)
            if callback:
                callback(result)

        return results

    def wait(self):
        """If this isn't the master process, wait for instructions."""
        if self.is_master():
            return

        while True:
            msg = self.comm.bcast(None, root=0)
            if msg is None:
                break

            function, task_list = msg
            for task in task_list:
                try:
                    res = function(task)
                    self.comm.send(res, dest=0)
                except Exception:
                    tb = traceback.format_exc()
                    self.comm.send(MPIPoolException(tb), dest=0)

    def close(self):
        """Close the pool and notify workers to exit."""
        if self.is_master():
            self.comm.bcast(None, root=0)