"""
Following are some methods that can be utilised as function to skip nodes from generator.
"""


def skip_leaf(node):
    return not node.children_list()


def skip_inner_node(node):
    return node.children_list()


def skip_no_node(node):
    return False


def skip_all_but_attribute_nodes(node):
    try:
        return not node.traffic
    except AttributeError:
        return True
