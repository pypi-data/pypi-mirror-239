from dataclasses import dataclass
from functools import partial
from requests import post
from typing import Optional, List, Callable

def variable_value_proposition_todict(variable_prop) -> dict:
    return {
        "id": variable_prop.id,
        "type": variable_prop.__class__.__name__,
        "value": float(variable_prop.value),
        "variables": list(
            map(
                lambda variable: variable.to_dict(),
                variable_prop.variables,
            )
        )
    }

def variable_proposition_todict(variable_prop) -> dict:
    return {
        "id": variable_prop.id,
        "type": variable_prop.__class__.__name__,
        "variables": list(
            map(
                lambda variable: variable.to_dict(),
                variable_prop.variables,
            )
        )
    }

@dataclass
class Variable:
    id: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": "Variable",
        }

@dataclass
class Proposition:
    pass

@dataclass
class AtLeast(Proposition):
    value: int
    variables: List[Proposition]
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return variable_value_proposition_todict(self)

@dataclass
class AtMost(Proposition):
    value: int
    variables: List[Proposition]
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return variable_value_proposition_todict(self)

@dataclass
class And(Proposition):
    variables: List[Proposition]
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return variable_proposition_todict(self)

@dataclass
class Or(Proposition):
    variables: List[Proposition]
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return variable_proposition_todict(self)

@dataclass
class Xor(Proposition):
    variables: List[Proposition]
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return variable_proposition_todict(self)

@dataclass
class XNor(Proposition):
    variables: List[Proposition]
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return variable_proposition_todict(self)

@dataclass
class Implies(Proposition):
    left:   Proposition
    right:  Proposition
    id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

@dataclass
class PropKey:
    prop:   Proposition
    key:    str

    def to_dict(self) -> dict:
        return {
            "prop": self.prop.to_dict(),
            "key": self.key,
        }

@dataclass
class Evaluation:
    data: Optional[List[List[str]]]
    error:  Optional[str]

def evaluate(prop_keys: List[PropKey], interpretations: List[dict], backend_url: str) -> Evaluation:
    try:
        response = post(
            f"{backend_url}/evaluate",
            json={
                "evaluables": list(
                    map(
                        lambda prop_key: prop_key.to_dict(),
                        prop_keys,
                    )
                ),
                "interpretations": interpretations,
            }
        )
        if response.status_code == 200:
            return Evaluation(
                data=response.json(),
                error=None,
            )
        else:
            return Evaluation(
                data=None,
                error=response.text,
            )
    except Exception as e:
        return Evaluation(
            data=None,
            error=str(e),
        )
    
def evaluation_composer(backend_url: str) -> Callable[[List[PropKey], dict], Evaluation]:
    return partial(
        evaluate,
        backend_url=backend_url,
    )