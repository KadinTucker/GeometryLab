from enum import Enum

class DataType(Enum):
    TYPE_UNKNOWN = 0  # A 'null' type; only for error/trivial cases
    NOMINAL = 1  # Only equality is supported
    ORDINAL = 2  # Nominal; but where quality and comparisons supported (totally ordered domain)
    INTERVAL = 3  # Ordinal; and supports addition, multiplication, and subtraction.
    INTEGRAL = 4  # Integer-like: interval; and supports modulo and integer division (by integers).
    RATIO = 5  # Rational-like: interval; and supports arbitrary division, absolute value
    PERIODIC = 6  # Rational-like, but where x + T == x for some nonzero period T. Must be templated.
    TEXT = 7  # Arbitrary strings supported for e.g. remarks; discouraged in favour of nominal/ordinal with templates.

# NOTE: consider using the Python base library numbers.py for base level implementation

class DataValue:

    def __init__(self):
        self.dtype = DataType.TYPE_UNKNOWN

class QuietNull:

    """
    A "Quiet Null" that acts as though it is a missing data value and is ignored in operations
    The quiet null QN satisfies the following:
     - QN == X -> False
     - QN != X -> True
     - QN op X -> X, for all binary operations 'op'.
    """

    def __init__(self):
        self.dtype = DataType.TYPE_UNKNOWN

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __add__(self, other):
        return other

    def __sub__(self, other):
        return other

    def __mul__(self, other):
        return other

    def __truediv__(self, other):
        return other

    def __floordiv__(self, other):
        return other

    def __mod__(self, other):
        return other

    def __pow__(self, other):
        return other

    def __neg__(self):
        return self

    def __pos__(self):
        return self

    def __abs__(self):
        return self

    def __invert__(self):
        return self

class NominalTemplate:

    """
    A nominal template can also act as an ordinal template
    where the key's value determines its order through the key order
    """

    def __init__(self, template_name):
        self.template_name = template_name
        self.keys: list[int] = []  # TODO: should be a search tree.
        self.names: dict[int, str] = {}

    def add_key(self, key: int, name: str):
        self.keys.append(key)
        self.names[key] = name

    def change_key(self, old_key: int, new_key: int):
        # changes an existing key to a new value
        if new_key in self.keys:
            raise KeyError(f"key {new_key} already exists in template")
        for i in range(len(self.keys)):
            if old_key == self.keys[i]:
                self.keys[i] = new_key
                self.names[new_key] = self.names.pop(old_key)
                return
        raise KeyError(f"key '{old_key}' not in template")

class NominalValue(DataValue):

    def __init__(self, value: int, template: NominalTemplate = None):
        super().__init__()
        self.dtype = DataType.NOMINAL
        self.template = template
        if template is not None:
            if value not in template.keys:
                raise ValueError(f"value '{value}' not in template")
        self.value = value

    @staticmethod
    def to(value: int, template=None):
        return NominalValue(value, template)

    def __eq__(self, other):
        return self.value == other.value and self.template is other.template

    def __ne__(self, other):
        return not self == other

class OrdinalValue(NominalValue):

    def __init__(self, value: int, template: NominalTemplate = None):
        super().__init__(value, template)
        self.dtype = DataType.ORDINAL

    def __lt__(self, other):
        return self.value < other.value and self.template is other.template

    def __gt__(self, other):
        return self.value > other.value and self.template is other.template

    def __le__(self, other):
        return self.value <= other.value and self.template is other.template

    def __ge__(self, other):
        return self.value >= other.value and self.template is other.template

