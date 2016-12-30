import random

from operations.operations import *
from costs.costs import TreeEditDistanceCost


class TEDGenerator(object):
    def __init__(self, costs, operation_generator, probability=.5):
        self._costs = costs or [TreeEditDistanceCost()]
        self._probability = probability
        self._operation_generator = operation_generator

    def generate(self, tree):
        result_tree = type(tree)()
        node_mapping = {}
        operation_mapping = {}
        distances = {cost: 0 for cost in self._costs}
        for node in tree:
            value = random.random()
            operation = self._operation_generator.no_operation
            if value < self._probability:
                operation = self._operation_generator()
                if operation.type() == DELETE_OPERATION and node.parent() is None:
                    # perform NoOperation as we don't have a parent to map nodes to after deletion
                    operation = self._operation_generator.no_operation
            print("[%s] performing %s" % (node.name, operation))
            node_mapping[node] = operation(node, node_mapping, result_tree)
            try:
                mapped_node = node_mapping[node][-1]
            except IndexError:
                mapped_node = node
            parent = node.parent()
            if parent is not None and parent not in operation_mapping:
                parent = node_mapping[parent][-1]
            if parent is not None:
                print("[%s] parent %s, operations %s" % (mapped_node.name, parent.name, operation_mapping.get(parent, set())))
            else:
                print("[%s] parent %s, operations %s" % (mapped_node.name, None, operation_mapping.get(parent, set())))
            for cost in self._costs:
                distances[cost] += cost(mapped_node, operation_mapping.get(parent, []), operation.type())
            operation_mapping.setdefault(mapped_node, [] + operation_mapping.get(parent, [])).append(operation.type())
            print("[%s] operations %s" % (mapped_node.name, operation_mapping[mapped_node]))
            print("distance %s" % [distance for distance in distances.values()])
        result_tree.__dict__["distance"] = distances
        return result_tree
