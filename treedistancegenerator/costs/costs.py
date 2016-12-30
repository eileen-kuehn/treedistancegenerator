from treedistancegenerator.operations.operations import *


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
        if MOVE_OPERATION in operations or MOVE_OPERATION == last_operation:
            return NotImplemented
        if NO_OPERATION != last_operation:
            # FIXME: what if we have delete and insert nested?
            # FIXME: or is this already correct?
            return 1
        try:
            if DELETE_OPERATION == operations[-1] or INSERT_OPERATION == operations[-1] or EDIT_OPERATION == operations[-1]:
                cost += 1
        except IndexError:
            pass
        return cost


class SubtreeWeightedTreeEditDistanceCost(EditDistanceCost):
    def __call__(self, node, operations, last_operation):
        cost = 0
        if MOVE_OPERATION in operations or MOVE_OPERATION == last_operation:
            return NotImplemented
        if NO_OPERATION != last_operation:
            return 1
        if DELETE_OPERATION in operations or INSERT_OPERATION in operations or EDIT_OPERATION in operations:
            cost += 1
        return cost


class SubtreeHeightWeightedTreeEditDistanceCost(EditDistanceCost):
    def __call__(self, node, operations, last_operation):
        cost = 0
        if MOVE_OPERATION in operations or MOVE_OPERATION == last_operation:
            return NotImplemented
        if NO_OPERATION != last_operation:
            return 1
        for index, operation in enumerate(operations):
            if operation != NO_OPERATION:
                cost += 1 / float(2**(len(operations) - index))
        return cost
