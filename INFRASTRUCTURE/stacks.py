from EXCEPTIONS.custom_exceptions import StackError


class UndoStack:
    """ The stack containing all the operations that can be undone """

    def __init__(self):
        """
        The constructor of the undo stack.
        The stack is represented as a list, which is empty at the moment of instantiation.
        """
        self.__operations_to_undo = []

    def push(self, operation):
        """
        Adds an operation on top of the stack.
        :param operation: the operation to be added
        """
        self.__operations_to_undo.append(operation)

    def pop(self):
        """
        Gets the operation on top of the stack and also removes it from the stack.
        Raises StackError if there are no operations to be popped.
        :return: the operation on top of the stack
        """
        if len(self.__operations_to_undo) == 0:
            raise StackError("No more undos available!\n")
        return self.__operations_to_undo.pop()

    def __len__(self):
        """
        Overwritten len() method.
        :return: the number of operations on the stack
        """
        return len(self.__operations_to_undo)

    @property
    def operations(self):
        """
        Getter for the operations from the stack.
        :return: the operations on the stack
        """
        return self.__operations_to_undo


class RedoStack:
    """ The stack containing all the operations that can be redone """

    def __init__(self):
        """
        The constructor of the redo stack.
        The stack is represented as a list, which is empty at the moment of instantiation.
        """
        self.__operations_to_redo = []

    def push(self, operation):
        """
        Adds an operation on top of the stack.
        :param operation: the operation to be added
        """
        self.__operations_to_redo.append(operation)

    def pop(self):
        """
        Gets the operation on top of the stack and also removes it from the stack.
        Raises StackError if there are no operations to be popped.
        :return: the operation on top of the stack
        """
        if len(self.__operations_to_redo) == 0:
            raise StackError("No more redos available!\n")
        return self.__operations_to_redo.pop()

    def clear_stack(self):
        """
        Removes all the operations from the stack.
        """
        self.__operations_to_redo.clear()

    def __len__(self):
        """
        Overwritten len() method.
        :return: the number of operations on the stack
        """
        return len(self.__operations_to_redo)

    @property
    def operations(self):
        """
        Getter for the operations from the stack.
        :return: the operations on the stack
        """
        return self.__operations_to_redo
