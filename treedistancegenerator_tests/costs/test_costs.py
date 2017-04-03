import unittest

from treedistancegenerator.costs.costs import *


class TestCosts(unittest.TestCase):
    def setUp(self):
        """
        deletion_tree is build on the following tree:
        root(deleted(child, child, child, child, deleted(child, child, child)))

        insertion_deletion_tree is build on the following tree:
        root(inserted(child, child, child, deleted(child, child, child)))

        insertion_insertion_tree is build on the following tree:
        root(inserted(child, child, child, child(inserted(child, child, child))))

        move_tree is build on the following tree:
        root(child(child, child, moved, moved(child(child, moved, moved))

        :return:
        """
        self.deletion_tree = [
            ([], NO_OPERATION),                                                  # root
            ([NO_OPERATION], DELETE_OPERATION),                                  # deleted
            ([NO_OPERATION, DELETE_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, DELETE_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, DELETE_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, DELETE_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, DELETE_OPERATION], DELETE_OPERATION),                # deleted
            ([NO_OPERATION, DELETE_OPERATION, DELETE_OPERATION], NO_OPERATION),  # child
            ([NO_OPERATION, DELETE_OPERATION, DELETE_OPERATION], NO_OPERATION),  # child
            ([NO_OPERATION, DELETE_OPERATION, DELETE_OPERATION], NO_OPERATION)   # child
        ]
        self.insertion_deletion_tree = [
            ([], NO_OPERATION),                                                  # root
            ([NO_OPERATION], INSERT_OPERATION),                                  # inserted
            ([NO_OPERATION, INSERT_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, INSERT_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, INSERT_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, INSERT_OPERATION], DELETE_OPERATION),                # deleted
            ([NO_OPERATION, INSERT_OPERATION, DELETE_OPERATION], NO_OPERATION),  # child
            ([NO_OPERATION, INSERT_OPERATION, DELETE_OPERATION], NO_OPERATION),  # child
            ([NO_OPERATION, INSERT_OPERATION, DELETE_OPERATION], NO_OPERATION)   # child
        ]
        self.insertion_insertion_tree = [
            ([], NO_OPERATION),                                                  # root
            ([NO_OPERATION], INSERT_OPERATION),                                  # inserted
            ([NO_OPERATION, INSERT_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, INSERT_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, INSERT_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, INSERT_OPERATION], NO_OPERATION),                    # child
            ([NO_OPERATION, INSERT_OPERATION, NO_OPERATION], INSERT_OPERATION),  # inserted
            ([NO_OPERATION, INSERT_OPERATION, NO_OPERATION, INSERT_OPERATION], NO_OPERATION),  # child
            ([NO_OPERATION, INSERT_OPERATION, NO_OPERATION, INSERT_OPERATION], NO_OPERATION),  # child
            ([NO_OPERATION, INSERT_OPERATION, NO_OPERATION, INSERT_OPERATION], NO_OPERATION)   # child
        ]
        self.move_tree = [
            ([], NO_OPERATION),                                                  # root
            ([NO_OPERATION], NO_OPERATION),                                      # child
            ([NO_OPERATION, NO_OPERATION], NO_OPERATION),                        # child
            ([NO_OPERATION, NO_OPERATION], NO_OPERATION),                        # child
            ([NO_OPERATION, NO_OPERATION], MOVE_OPERATION),                      # moved
            ([NO_OPERATION, NO_OPERATION], MOVE_OPERATION),                      # moved
            ([NO_OPERATION, NO_OPERATION, MOVE_OPERATION], NO_OPERATION),        # child
            ([NO_OPERATION, NO_OPERATION, MOVE_OPERATION, NO_OPERATION], MOVE_OPERATION),      # moved
            ([NO_OPERATION, NO_OPERATION, MOVE_OPERATION, NO_OPERATION], MOVE_OPERATION)       # moved
        ]

    def test_ted(self):
        ted_cost = TreeEditDistanceCost()
        deletion_cost = 0
        for operations, last_operation in self.deletion_tree:
            deletion_cost += ted_cost(None, operations, last_operation)
        self.assertEqual(2, deletion_cost)

        insertion_deletion_cost = 0
        for operations, last_operation in self.insertion_deletion_tree:
            insertion_deletion_cost += ted_cost(None, operations, last_operation)
        self.assertEqual(2, insertion_deletion_cost)

        insertion_insertion_cost = 0
        for operations, last_operation in self.insertion_insertion_tree:
            insertion_insertion_cost += ted_cost(None, operations, last_operation)
        self.assertEqual(2, insertion_insertion_cost)

        move_cost = 0
        for operations, last_operation in self.move_tree:
            move_cost += ted_cost(None, operations, last_operation)
        self.assertEqual(4, move_cost)

    def test_fted(self):
        fted_cost = FanoutWeightedTreeEditDistanceCost()
        deletion_cost = 0
        for operations, last_operation in self.deletion_tree:
            deletion_cost += fted_cost(None, operations, last_operation)
        self.assertEqual(10, deletion_cost)

        insertion_deletion_cost = 0
        for operations, last_operation in self.insertion_deletion_tree:
            insertion_deletion_cost += fted_cost(None, operations, last_operation)
        self.assertEqual(9, insertion_deletion_cost)

        insertion_insertion_cost = 0
        for operations, last_operation in self.insertion_insertion_tree:
            insertion_insertion_cost += fted_cost(None, operations, last_operation)
        self.assertEqual(9, insertion_insertion_cost)

        move_cost = 0
        for operations, last_operation in self.move_tree:
            move_cost += fted_cost(None, operations, last_operation)
        self.assertEqual(5, move_cost)

    def test_sted(self):
        sted_cost = SubtreeWeightedTreeEditDistanceCost()
        deletion_cost = 0
        for operations, last_operation in self.deletion_tree:
            deletion_cost += sted_cost(None, operations, last_operation)
        self.assertEqual(10, deletion_cost)

        insertion_deletion_cost = 0
        for operations, last_operation in self.insertion_deletion_tree:
            insertion_deletion_cost += sted_cost(None, operations, last_operation)
        self.assertEqual(9, insertion_deletion_cost)

        insertion_insertion_cost = 0
        for operations, last_operation in self.insertion_insertion_tree:
            insertion_insertion_cost += sted_cost(None, operations, last_operation)
        self.assertEqual(10, insertion_insertion_cost)

        move_cost = 0
        for operations, last_operation in self.move_tree:
            move_cost += sted_cost(None, operations, last_operation)
        self.assertEqual(4, move_cost)

    def test_weignted_sted(self):
        wsted_cost = SubtreeHeightWeightedTreeEditDistanceCost()
        deletion_cost = 0
        for operations, last_operation in self.deletion_tree:
            deletion_cost += wsted_cost(None, operations, last_operation)
        self.assertEqual(6.75, deletion_cost)

        insertion_deletion_cost = 0
        for operations, last_operation in self.insertion_deletion_tree:
            insertion_deletion_cost += wsted_cost(None, operations, last_operation)
        self.assertEqual(6.25, insertion_deletion_cost)

        insertion_insertion_cost = 0
        for operations, last_operation in self.insertion_insertion_tree:
            insertion_insertion_cost += wsted_cost(None, operations, last_operation)
        self.assertEqual(6.125, insertion_insertion_cost)

        move_cost = 0
        for operations, last_operation in self.move_tree:
            move_cost += wsted_cost(None, operations, last_operation)
        self.assertEqual(4, move_cost)

        move_cost = 0
        for operations, last_operation in self.move_tree:
            move_cost += wsted_cost(None, operations, last_operation)
        self.assertEqual(4, move_cost)
