from typing import Tuple

# idk how to explain why this is required.

class _Inf(float):
    
    def __new__(cls, val = 1):
        self = super().__new__(cls, "inf")
        setattr(self, "val", val)
        return self
        
    def __str__(self) -> str:
        return "∞"
    
    def as_integer_ratio(self) -> Tuple[int, int]:
        return (getattr(self, "val", 1), 0)
    
    def is_integer(self) -> bool:
        return False

INFINITY = _Inf()

for i in [ "__sub__", "__isub__",  "__mul__", "__imul__",  "__truediv__", "__itruediv__",  "__floordiv__",  "__ifloordiv__", "__add__", "__iadd__", "__pow__", "__ipow__", ]:
    setattr(_Inf, i, lambda self, other: INFINITY)