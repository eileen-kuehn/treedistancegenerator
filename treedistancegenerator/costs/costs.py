from treedistancegenerator.operations.operations import *

from collections import Counter


class EditDistanceCost(object):
    def __call__(self, node, operations, last_operation):
        return NotImplemented


class TreeEditDistanceCost(EditDistanceCost):
    def __call__(self, node, operations, last_operation):
        if last_operation == NO_OPERATION:
            return 0
        return 1


class FanoutWeightedTreeEditDistanceCost(EditDistanceCost):
    def __call__(self, node, operations, last_operation):
        cost = 0
        # if MOVE_OPERATION in operations or MOVE_OPERATION == last_operation:
        #     return NotImplemented
        if NO_OPERATION != last_operation:
            cost += 1
        try:
            if operations[-1] != NO_OPERATION:
                cost += 1
        except IndexError:
            pass
        return cost


class SubtreeWeightedTreeEditDistanceCost(EditDistanceCost):
    def __call__(self, node, operations, last_operation):
        cost = 0
        # if MOVE_OPERATION in operations or MOVE_OPERATION == last_operation:
        #     return NotImplemented
        if NO_OPERATION != last_operation:
            cost += 1
        operations = set(operations)
        minimum_length = 1
        if NO_OPERATION in operations:
            minimum_length += 1
        if len(operations) >= minimum_length:
            cost += 1
        return cost


class SubtreeHeightWeightedTreeEditDistanceCost(EditDistanceCost):
    def __call__(self, node, operations, last_operation):
        cost = 0
        # if MOVE_OPERATION in operations or MOVE_OPERATION == last_operation:
        #     return NotImplemented
        if NO_OPERATION != last_operation:
            cost += 1
        for index, operation in enumerate(operations):
            if operation != NO_OPERATION:
                cost += 1 / float(2**(len(operations) - index))
        return cost
