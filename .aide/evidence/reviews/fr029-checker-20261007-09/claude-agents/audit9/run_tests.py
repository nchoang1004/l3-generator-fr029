import boot, unittest, sys
import test_checker_counterexamples as t
r = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromModule(t))
