import random

from operations.operations import *
from costs.costs import TreeEditDistanceCost


class TEDGenerator(object):
    """
    TreeDistanceGenerator allows to edit a given tree for different types of edit operations.
    Therefore it relies on building a mapping between the nodes of the given tree and the nodes
    of the created tree. In addition, it holds a list for each node that contains information
    on all operations that were performed in its ancestry.
    """
    def __init__(self, costs, operation_generator, probability=.5, seed=None):
        self._costs = costs or [TreeEditDistanceCost()]
        self._probability = probability
        self._operation_generator = operation_generator
        if seed is not None:
            random.seed(seed)

    def generate(self, tree):
        result_tree = type(tree)()
        node_mapping = {}
        operation_mapping = {}
        distances = {cost: 0 for cost in self._costs}
        node_generator = tree.node_iter()  # currently only defined on nodes, not attributes
        try:
            node = next(node_generator)
            while node:
                value = random.random()
                operation = self._operation_generator.no_operation
                if value < self._probability:
                    operation = self._operation_generator()
                    if operation.type() == DELETE_OPERATION and node.parent() is None:
                        # perform NoOperation as we don't have a parent to map nodes to after deletion
                        operation = self._operation_generator.no_operation
                    elif operation.type() == MOVE_OPERATION:
                        try:
                            next_node = next(node_generator)
                        except StopIteration:
                            # at end of tree, so just insert the last node
                            operation = self._operation_generator.no_operation
                        else:
                            if next_node.parent() == node:
                                # skipping to next loop so that node can also be handled
                                self._handle_node(node=node,
                                                  operation=self._operation_generator.no_operation,
                                                  node_mapping=node_mapping,
                                                  operation_mapping=operation_mapping,
                                                  result_tree=result_tree, distances=distances)
                                node = next_node
                                continue
                            self._handle_node(
                                node=next_node, operation=operation, node_mapping=node_mapping,
                                operation_mapping=operation_mapping, result_tree=result_tree,
                                distances=distances)
                self._handle_node(node=node, operation=operation, node_mapping=node_mapping,
                                  operation_mapping=operation_mapping, result_tree=result_tree,
                                  distances=distances)
                node = next(node_generator)
        except StopIteration:
            pass
        result_tree.__dict__["distance"] = distances
        return result_tree

    def _handle_node(self, node, operation, node_mapping, operation_mapping, result_tree, distances):
        node_mapping[node] = operation(node, node_mapping, result_tree)
        try:
            mapped_node = node_mapping[node][-1]
        except IndexError:
            mapped_node = node
        parent = node.parent()
        if parent is not None and parent not in operation_mapping:
            parent = node_mapping[parent][-1]
        for cost in self._costs:
            distances[cost] += cost(mapped_node, operation_mapping.get(parent, []), operation.type())
        operation_mapping.setdefault(mapped_node, [] + operation_mapping.get(parent, [])).append(operation.type())
