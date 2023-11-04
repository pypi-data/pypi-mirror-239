from unified_planning.shortcuts import *  # type: ignore
from unified_planning.io import PDDLReader
from collections import namedtuple  # type: ignore
from unified_planning.plans import PlanKind  # type: ignore
import unittest
from unified_planning.engines.results import PlanGenerationResultStatus
import up_bfgp


class BFGPtest(unittest.TestCase):
    def base_bfgp_test(self, domain_file: str, problem_files: List[str], args: dict):
        with up.environment.get_environment().factory.FewshotPlanner(name='bfgp') as bfgp:
            bfgp.set_arguments(**args)
            problems = bfgp.generate_problems(domain_file, problem_files)
            # Compute the generalized plan for these input problems
            result = bfgp.solve(problems, output_stream=sys.stdout)
            # Check whether all generated plans are satisficing
            assert all(r == PlanGenerationResultStatus.SOLVED_SATISFICING for r in result)

    # @unittest.skip
    def test_bfgp_synthesis_gripper(self):
        """Testing the BFGP++ solvers can solve 3 different Gripper instances"""
        domain = 'domains/gripper/domain.pddl'
        problems = [f'domains/gripper/p{i:02}.pddl' for i in range(1, 4)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 10,
                       'program': 'gripper',
                       'translated_problem_dir': 'tmp_gripper/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

    def test_bfgp_repair_gripper(self):
        """Testing the BFGP++ solver can repair 3 Gripper programs for all input instances"""
        domain = 'domains/gripper/domain.pddl'
        problems = [f'domains/gripper/p{i:02}.pddl' for i in range(1, 4)]

        # Test 1: the input program is correct
        kwargs = dict({'mode': 'repair',
                       'theory': 'cpp',
                       'program_lines': 10,
                       'program': 'domains/gripper/program_repair/gripper_cpp_ok',
                       'translated_problem_dir': 'tmp_gripper_ok/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        # Test 2: the input program has some missing loops
        kwargs = dict({'mode': 'repair',
                       'theory': 'cpp',
                       'program_lines': 10,
                       'program': 'domains/gripper/program_repair/gripper_cpp_missing_loops',
                       'translated_problem_dir': 'tmp_gripper_missing_loops/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        # Test 3: the input program has some missing planning action
        kwargs = dict({'mode': 'repair',
                       'theory': 'cpp',
                       'program_lines': 10,
                       'program': 'domains/gripper/program_repair/gripper_cpp_missing_planning_actions',
                       'translated_problem_dir': 'tmp_gripper_missing_planning_actions/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)


    # @unittest.skip
    def test_bfgp_visitall(self):
        """Testing the BFGP++ solver can solve 10 different Visitall instances"""
        domain = 'domains/visitall/synthesis/domain.pddl'
        problems = [f'domains/visitall/synthesis/p{i:02}.pddl' for i in range(1, 11)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 16,
                       'program': 'visitall',
                       'translated_problem_dir': 'tmp_visitall/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        """Testing the BFGP++ solver can validate 10 different and larger Visitall instances"""
        domain = 'domains/visitall/validation/domain.pddl'
        problems = [f'domains/visitall/validation/p{i:02}.pddl' for i in range(1, 11)]
        kwargs = dict({'mode': 'validation-prog',
                       'theory': 'cpp',
                       'program': 'visitall',
                       'translated_problem_dir': 'tmp_visitall/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

    # @unittest.skip
    def test_bfgp_spanner(self):
        """Testing the BFGP++ solver can solve 10 first Spanner instances"""
        domain = 'domains/spanner/domain.pddl'
        problems = [f'domains/spanner/training/easy/p{i:02}.pddl' for i in range(1, 11)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 16,
                       'program': 'spanner',
                       'translated_problem_dir': 'tmp_spanner/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        """Testing the BFGP++ solver can validate 10 last (and larger) Spanner instances"""
        domain = 'domains/spanner/domain.pddl'
        problems = [f'domains/spanner/training/easy/p{i:02}.pddl' for i in range(90, 100)]
        kwargs = dict({'mode': 'validation-prog',
                       'theory': 'cpp',
                       'program': 'spanner',
                       'translated_problem_dir': 'tmp_spanner/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

    # @unittest.skip
    def test_bfgp_miconic(self):
        """Testing the BFGP++ solver can solve 50 first Miconic instances"""
        domain = 'domains/miconic/domain.pddl'
        problems = [f'domains/miconic/training/easy/p{i:02}.pddl' for i in range(1, 51)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 13,
                       'program': 'miconic',
                       'num_extra_pointers': 1,
                       'translated_problem_dir': 'tmp_miconic/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        """Testing the BFGP++ solver can validate 10 last (and larger) Miconic instances"""
        domain = 'domains/miconic/domain.pddl'
        problems = [f'domains/miconic/training/easy/p{i:02}.pddl' for i in range(90, 100)]
        kwargs = dict({'mode': 'validation-prog',
                       'theory': 'cpp',
                       'program': 'miconic',
                       'num_extra_pointers': 1,
                       'translated_problem_dir': 'tmp_miconic/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

    def test_program_synthesis_benchmarks(self):
        """Testing the BFGP++ solvers can solve 6 Program Synthesis benchmarks"""
        # Benchmark 1: Fibonacci
        domain = 'domains/fibonacci/domain.txt'
        problems = [f'domains/fibonacci/{i}.txt' for i in range(1, 11)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 7,
                       'program': 'fibonacci',
                       'translated_problem_dir': 'tmp_fibonacci/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        # Benchmark 2: Find
        domain = 'domains/find/domain.txt'
        problems = [f'domains/find/{i}.txt' for i in range(1, 11)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 4,
                       'program': 'find',
                       'translated_problem_dir': 'tmp_find/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        # Benchmark 3: Reverse
        domain = 'domains/reverse/domain.txt'
        problems = [f'domains/reverse/{i}.txt' for i in range(1, 11)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 7,
                       'program': 'reverse',
                       'translated_problem_dir': 'tmp_reverse/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        # Benchmark 4: Select
        domain = 'domains/select/domain.txt'
        problems = [f'domains/select/{i}.txt' for i in range(1, 11)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 7,
                       'num_extra_pointers': 1,
                       'program': 'select',
                       'translated_problem_dir': 'tmp_select/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        # Benchmark 5: Sorting
        domain = 'domains/sorting/domain.txt'
        problems = [f'domains/sorting/{i}.txt' for i in range(1, 11)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 8,
                       'program': 'sorting',
                       'translated_problem_dir': 'tmp_sorting/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        # Benchmark 6: Triangular Sum
        domain = 'domains/triangular_sum/domain.txt'
        problems = [f'domains/triangular_sum/{i}.txt' for i in range(1, 11)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 5,
                       'program': 'triangular_sum',
                       'translated_problem_dir': 'tmp_triangular_sum/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

    """
    # ToDo: update the theory to capture goals in the initial state
    def test_bfgp_satellite(self):
        # Testing the BFGP++ solver can solve 20 first Satellite instances
        domain = 'domains/satellite/domain.pddl'
        problems = [f'domains/satellite/training/easy/p{i:02}.pddl' for i in range(1, 21)]
        kwargs = dict({'mode': 'synthesis',
                       'theory': 'cpp',
                       'program_lines': 15,
                       'program': 'satellite.prog',
                       'num_extra_pointers': 1,
                       'translated_problem_dir': 'test_satellite/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)

        # Testing the BFGP++ solver can validate 10 last (and larger) Spanner instances
        domain = 'domains/satellite/domain.pddl'
        problems = [f'domains/satellite/training/easy/p{i:02}.pddl' for i in range(90, 100)]
        kwargs = dict({'mode': 'validation-prog',
                       'theory': 'cpp',
                       'program': 'satellite.prog',
                       'num_extra_pointers': 1,
                       'translated_problem_dir': 'test_satellite/'})

        self.base_bfgp_test(domain_file=domain, problem_files=problems, args=kwargs)
    """


if __name__ == "__main__":
    unittest.main()
