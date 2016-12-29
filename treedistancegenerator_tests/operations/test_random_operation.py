import unittest

from treedistancegenerator.operations.random_operation import RandomOperation
from treedistancegenerator.operations.operations import *


class TestRandomOperation(unittest.TestCase):
    def test_creation(self):
        random_op = RandomOperation(move_probability=1)
        self.assertIsNotNone(random_op)
        self.assertEqual(MOVE_OPERATION, random_op().type())

    def test_randomness(self):
        random_op = RandomOperation(insert_probability=.5, delete_probability=.5)
        result_dict = {
            INSERT_OPERATION: 0,
            DELETE_OPERATION: 0
        }
        for i in range(1000):
            result_dict[random_op().type()] += 1
        self.assertAlmostEqual(.5, result_dict[INSERT_OPERATION]/1000.0, 1)
        self.assertAlmostEqual(.5, result_dict[DELETE_OPERATION]/1000.0, 1)
