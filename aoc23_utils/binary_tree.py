import enum

class BinaryTreeDir(enum.Enum):
    NONE = 0
    RIGHT = 1
    LEFT = 2


class BinaryTreeNode:
    def __init__(self, left=None, right=None):
        self._left = self
        self._right = self
        if left:
            self._left = left
        if right:
            self._right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, val):
        self._left = val

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, val):
        self._right = val

    def get_child(self, direction: 'BinaryTreeDir'):
        if direction == BinaryTreeDir.LEFT:
            return self.left
        elif direction == BinaryTreeDir.RIGHT:
            return self.right
