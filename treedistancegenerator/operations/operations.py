NO_OPERATION = 0
INSERT_OPERATION = 1
DELETE_OPERATION = 2
EDIT_OPERATION = 3
MOVE_OPERATION = 4


class TreeEditOperation(object):
    def type(self):
        return NO_OPERATION

    def __call__(self, node):
        raise NotImplementedError

    @staticmethod
    def _valid_parent(node, mapping_reference=None, tree_reference=None):
        """
        * A deleted node maps to an empty array, I therefore try to search as long as I don't
          get an exception to return mapped parent

        :param node:
        :param mapping_reference:
        :return: Reference to parent from mapped nodes
        """
        if mapping_reference:
            parent = node.parent()
            while parent:
                try:
                    return mapping_reference[parent][-1]
                except IndexError:
                    parent = parent.parent()
        return None


class NoTreeEditOperation(TreeEditOperation):
    def __call__(self, node, mapping_reference=None, tree_reference=None):
        current_node = node.dao()
        del current_node["node_id"]
        parent = self._valid_parent(node, mapping_reference)
        tree_node = tree_reference.add_node(parent=parent, **current_node)
        try:
            tree_node.ppid = parent.pid
        except AttributeError:
            pass
        return [tree_node]


class InsertTreeEditOperation(TreeEditOperation):
    def type(self):
        return INSERT_OPERATION

    def __call__(self, node, mapping_reference=None, tree_reference=None):
        current_node = node.dao()
        del current_node["node_id"]
        parent = self._valid_parent(node, mapping_reference)
        current_tree_node = tree_reference.add_node(parent=parent, **current_node)
        try:
            current_tree_node.ppid = parent.pid
        except AttributeError:
            pass
        inserted_node = current_tree_node.dao()
        del inserted_node["node_id"]
        inserted_node["name"] = "%s_inserted" % inserted_node.get("name", "")
        inserted_tree_node = current_tree_node.add_node(**inserted_node)
        inserted_tree_node.pid += 1
        return [current_tree_node, inserted_tree_node]


class DeleteTreeEditOperation(TreeEditOperation):
    def type(self):
        return DELETE_OPERATION

    def __call__(self, node, mapping_reference=None, tree_reference=None):
        return []


class EditTreeEditOperation(TreeEditOperation):
    def type(self):
        return EDIT_OPERATION

    def __call__(self, node, mapping_reference=None, tree_reference=None):
        current_node = node.dao()
        del current_node["node_id"]
        current_node["name"] = "%s_edited" % current_node.get("name", "")
        parent = self._valid_parent(node, mapping_reference)
        current_tree_node = tree_reference.add_node(parent=parent, **current_node)
        try:
            current_tree_node.ppid = parent.pid
        except AttributeError:
            pass
        return [current_tree_node]


class MoveTreeEditOperation(TreeEditOperation):
    def type(self):
        return MOVE_OPERATION

    def __call__(self, node, mapping_reference=None, tree_reference=None):
        current_node = node.dao()
        del current_node["node_id"]
        parent = self._valid_parent(node, mapping_reference)
        current_tree_node = tree_reference.add_node(parent=parent, **current_node)
        try:
            current_tree_node.ppid = parent.pid
        except AttributeError:
            pass
        return [current_tree_node]
