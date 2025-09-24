class Node:
    """Simple binary tree node"""

    def __init__(self, frequency: int, symbol: str | None = None):
        """Initialize a new node.

        Args:
            frequency (int): The frequency of the node.
            symbol (str, optional): The symbol associated with the node. Defaults to None.
        """
        self.__frequency = frequency
        self.__symbol = symbol
        self.__left = None
        self.__right = None

    # -- Setters -- #

    def set_left(self, child) -> None:
        self.__left = child

    def set_right(self, child) -> None:
        self.__right = child

    # -- Getters -- #

    def get_frequency(self) -> int:
        return self.__frequency

    def get_symbol(self) -> str:
        return self.__symbol

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    # -- Overloaded operators -- #

    def __str__(self) -> str:
        return f"({self.__symbol}:{self.__frequency})"

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other: "Node") -> bool:
        return self.__frequency < other.__frequency
