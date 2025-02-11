from typing import List, Dict

from pydantic import BaseModel

# Models

class AFDRequest(BaseModel):
    states: List[str]
    input_symbols: List[str]
    transitions: Dict[str, Dict[str, str]]
    initial_state: str
    final_states: List[str]

class APDRequest(BaseModel):
    states: List[str]
    input_symbols: List[str]
    stack_symbols: List[str]
    transitions: Dict[str, Dict[str, Dict[str, List[str]]]]
    initial_state: str
    final_states: List[str]
    stack_start_symbol: str

class MT_Request(BaseModel):
    states: List[str]
    input_symbols: List[str]
    tape_symbols: List[str]
    transitions: Dict[str, Dict[str, Dict[str, str]]]
    initial_state: str
    final_states: List[str]