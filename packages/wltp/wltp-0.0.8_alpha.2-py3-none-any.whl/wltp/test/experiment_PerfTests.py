#!/usr/bin/env python
#
# Copyright 2013-2014 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
'''
:created: 5 Jan 2014
'''

from ..experiment import Experiment
from .goodvehicle import goodVehicle
import logging
import unittest
import time


class ExperimentPerf(unittest.TestCase):

    @unittest.SkipTest
    def testPerf(self):
        logging.getLogger().setLevel(logging.WARNING)

        nexp = 100
        start = time.time()
        for _ in range(nexp):
            model = goodVehicle()

            experiment = Experiment(model)

            experiment.run()

        elapsed = (time.time() - start)
        print(">> ELAPSED: %.2fsec, RUN/EXP: %.4fsec"%(elapsed, elapsed/nexp))


if __name__ == "__main__":
    import sys;#sys.argv = ['', 'Test.testName']
    unittest.main(argv = sys.argv[1:])
