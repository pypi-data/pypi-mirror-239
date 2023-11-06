import re
from cwstorm.dsl.node import Node


VALID_NAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z0-9_\-]*$")
NAME_NUMBER_PADDING = 5


class DagNode(Node):

    """A node in a directed acyclic graph.

    Note: No node removal (ever)

    Subclasses are Job and Task.

    Job can never be a child, but it is a dag_node as
    its useful to inherit the add() method.

    An Instance is task that is a child of more than one parent
    It is represented by one node in the DAG. However it must
    be written many times in the output serialize.
    During  traversal it is visited repeatedly, from differnt
    parents. So it is considered the original task with
    respect to its first parent, and an instance task with
    respect to all other parents.
    """

    instances = {}  # Class dictionary to hold instances
    name_counter = {}  # Dictionary to keep track of class_name and number

    @classmethod
    def reset(cls):
        cls.instances = {}
        cls.name_counter = {}

    @classmethod
    def generate_unique_name(cls):
        class_name = cls.__name__
        cls.name_counter.setdefault(class_name, 0)
        counter = cls.name_counter[class_name]
        name = cls.format_name(class_name, counter)
        cls.name_counter[class_name] += 1
        return name

    @classmethod
    def get_unique_name(cls, name):
        base_name = name.split("_")[0]
        if base_name not in cls.instances:
            return name

        counter = 1
        while True:
            name = cls.format_name(base_name, counter)
            if name not in cls.instances:
                return name
            counter += 1

    @classmethod
    def format_name(cls, base_name, counter):
        return f"{base_name}_{str(counter).zfill(NAME_NUMBER_PADDING)}"

    def __init__(self, name=None):
        """Init parent and children arrays.

        A Node remembers its parents to make it quick to determine
        whether it is an instance with respect to that parent.
        """
        if name is None:
            name = self.generate_unique_name()
        else:
            name = self.get_unique_name(name)
        self.instances[name] = self  # Add instance to class dictionary

        self._name = name
        self.parents = []
        self.children = []

        super().__init__()

    def add(self, *children):
        """Add children if not already added.

        Also add a pointers on the child nodes' parent attr back to self.
        """
        if any(type(child).__name__ != "Task" for child in children):
            raise TypeError("Only Task nodes can be children")

        for child in children:
            if child not in self.children:
                self.children.append(child)
                if self not in child.parents:
                    child.parents.append(self)
        return self

    def name(self):
        """get a name

        This is not handled by the node accessor mechanism
        because we need to treat it differently, i.e. add unique suffix"""
        return self._name

    def __str__(self):
        return self._name

    def is_leaf(self):
        return not self.children

    def is_root(self):
        return not self.parents

    def count_descendents(self):
        visited = set()

        def dfs_descendents(node):
            visited.add(node.name())
            for child in node.children:
                if child.name() not in visited:
                    dfs_descendents(child)

        dfs_descendents(self)
        return len(visited) - 1

    def count_ancestors(self):
        visited = set()

        def dfs_ancestors(node):
            visited.add(node.name())
            for parent in node.parents:
                if parent.name() not in visited:
                    dfs_ancestors(parent)

        dfs_ancestors(self)
        return len(visited) - 1

    def is_original(self, parent=None):
        raise NotImplementedError("is_original() must be implemented by subclass")

    def is_reference(self, parent=None):
        raise NotImplementedError("is_reference() must be implemented by subclass")

    @classmethod
    def validate_name(cls, name):
        if not isinstance(name, str):
            raise TypeError("name() argument must be a string")
        if not cls.is_unique_name(name):
            raise ValueError("name() argument must be unique")
        if not VALID_NAME_REGEX.match(name):
            raise ValueError(
                "name() argument must match {}".format(VALID_NAME_REGEX.pattern)
            )
        return True
