import random
import logging

from operations import *


class RandomOperation(object):
    def __init__(self, no_operation=None, insert_operation=None, insert_probability=0,
                 delete_operation=None, delete_probability=0,
                 edit_operation=None, edit_probability=0,
                 move_operation=None, move_probability=0):
        self._probability_list = []
        self.no_operation = no_operation or NoTreeEditOperation()
        for probability, operation in [(insert_probability, insert_operation or InsertTreeEditOperation()),
                                       (delete_probability, delete_operation or DeleteTreeEditOperation()),
                                       (edit_probability, edit_operation or EditTreeEditOperation()),
                                       (move_probability, move_operation or MoveTreeEditOperation())]:
            if probability <= 0:
                continue
            try:
                self._probability_list.append((self._probability_list[-1][0]+probability, operation,))
            except IndexError:
                self._probability_list.append((probability, operation,))
        if self._probability_list[-1][0] > 1:
            logging.getLogger(self.__class__.__name__).warning(
                "sum of operations is more than 100% (%s)", self._probability_list[-1][0])
        elif self._probability_list[-1][0] < 1:
            logging.getLogger(self.__class__.__name__).warning(
                "sum of operations is less than 100% (%s)", self._probability_list[-1][0])

    def __call__(self):
        current_value = random.random()
        last_value = 0
        for (value, operation) in self._probability_list:
            if last_value < current_value < value:
                # return last checked operation
                return operation
        return self.no_operation
