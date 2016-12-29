from treedistancegenerator.operations.operations import *


class TreeEditDistanceCost(object):
    def __call__(self, node, operations, last_operation):
        if last_operation == NO_OPERATION:
            return 0
        return 1


class FanoutWeightedTreeEditDistanceCost(object):
    def __call__(self, node, operations, last_operation):
        cost = 0
        if DELETE_OPERATION == last_operation or INSERT_OPERATION == last_operation:
            return 1
        if DELETE_OPERATION in operations or INSERT_OPERATION in operations:
            cost += 1
        if EDIT_OPERATION == last_operation:
            cost += 1
        if MOVE_OPERATION in operations:
            return NotImplemented
        return cost
