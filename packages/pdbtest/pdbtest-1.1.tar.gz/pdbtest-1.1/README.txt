Usage:
python -m pdbtest [module]

(after the pattern of python -m unittest [module])

PDBtest shims the unittest test runner machinery to, when a test fails due to an
exception, print some information about the TestCase and test_method, and then
launch the PDB interactive debugger, affording you the opportunity to easily
examine the failure.

The library also provides a PDBRunnerMixin class that you can mix in to your
test runner to achieve the same effect, and a modified TestProgram that will
automatically shim the runner you provide and can be used in the same way as
unittest.TestProgram.
