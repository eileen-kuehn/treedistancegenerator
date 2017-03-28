import unittest

from treedistancegenerator.ted_generator import TEDGenerator
from treedistancegenerator.costs.costs import *
from treedistancegenerator.operations.random_operation import RandomOperation

from assess.prototypes.simpleprototypes import Prototype


class TestTEDGenerator(unittest.TestCase):
    def test_creation(self):
        tedgen = TEDGenerator(costs=[TreeEditDistanceCost()],
                              operation_generator=RandomOperation(delete_probability=1))
        self.assertIsNotNone(tedgen)

    def test_deletion(self):
        tedgen = TEDGenerator(costs=[FanoutWeightedTreeEditDistanceCost(), TreeEditDistanceCost()],
                              operation_generator=RandomOperation(delete_probability=1))
        prototype = Prototype()
        root = prototype.add_node("root", pid=1, ppid=0)
        one = root.add_node("test1", pid=2, ppid=1)
        root.add_node("test2", pid=3, ppid=1)
        root.add_node("test3", pid=4, ppid=1)
        one.add_node("test1.1", pid=5, ppid=2)
        one.add_node("test1.2", pid=6, ppid=2)
        one.add_node("test1.3", pid=7, ppid=2)
        result = tedgen.generate(tree=prototype)
        print("received %s" % result.distance)

    def test_insertion(self):
        tedgen = TEDGenerator(costs=[FanoutWeightedTreeEditDistanceCost(), TreeEditDistanceCost()],
                              operation_generator=RandomOperation(insert_probability=1))
        prototype = Prototype()
        root = prototype.add_node("root", pid=1, ppid=0)
        one = root.add_node("test1", pid=2, ppid=1)
        root.add_node("test2", pid=3, ppid=1)
        root.add_node("test3", pid=4, ppid=1)
        one.add_node("test1.1", pid=5, ppid=2)
        one.add_node("test1.2", pid=6, ppid=2)
        one.add_node("test1.3", pid=7, ppid=2)
        result = tedgen.generate(tree=prototype)
        print("received %s" % result.distance)

    def test_edit(self):
        tedgen = TEDGenerator(costs=[FanoutWeightedTreeEditDistanceCost(), TreeEditDistanceCost()],
                              operation_generator=RandomOperation(edit_probability=1))
        prototype = Prototype()
        root = prototype.add_node("root", pid=1, ppid=0)
        one = root.add_node("test1", pid=2, ppid=1)
        root.add_node("test2", pid=3, ppid=1)
        root.add_node("test3", pid=4, ppid=1)
        one.add_node("test1.1", pid=5, ppid=2)
        one.add_node("test1.2", pid=6, ppid=2)
        one.add_node("test1.3", pid=7, ppid=2)
        result = tedgen.generate(tree=prototype)
        print("received %s" % result.distance)

    def test_all(self):
        tedgen = TEDGenerator(costs=[FanoutWeightedTreeEditDistanceCost(),
                                     TreeEditDistanceCost(),
                                     SubtreeWeightedTreeEditDistanceCost(),
                                     SubtreeHeightWeightedTreeEditDistanceCost()],
                              operation_generator=RandomOperation(delete_probability=1/3.0,
                                                                  insert_probability=1/3.0,
                                                                  edit_probability=1/3.0),
                              probability=.5)
        prototype = Prototype()
        root = prototype.add_node("root", pid=1, ppid=0)
        one = root.add_node("test1", pid=2, ppid=1)
        root.add_node("test2", pid=3, ppid=1)
        root.add_node("test3", pid=4, ppid=1)
        one.add_node("test1.1", pid=5, ppid=2)
        one.add_node("test1.2", pid=6, ppid=2)
        one.add_node("test1.3", pid=7, ppid=2)
        two = one.add_node("test1.4", pid=8, ppid=2)
        two.add_node("test2.1", pid=9, ppid=8)
        two.add_node("test2.2", pid=10, ppid=8)
        two.add_node("test2.3", pid=11, ppid=8)
        two.add_node("test2.4", pid=12, ppid=8)
        result = tedgen.generate(tree=prototype)
        result2 = tedgen.generate(tree=prototype)
        print("received %s" % result.distance)
        print("received %s" % result2.distance)
