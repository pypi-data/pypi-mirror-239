
from dataclasses import dataclass
from typing import Optional


# SMI 파싱 결과로 리턴할 Class 타입 (Type-Safety)

@dataclass
class ParsedSMI:
    orig: str
    main: list[list[str]]
    raw: str
    text: list[str]
    line: int
    type: Optional[str]
