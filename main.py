from automata.pda.dpda import DPDA
from automata.tm.dtm import DTM
from fastapi import FastAPI, HTTPException
from automata.fa.dfa import DFA
from typing import Dict, List, Optional, Tuple, Any, Union, Literal

from fastapi.middleware.cors import CORSMiddleware

from Model import *

app = FastAPI()

origins = ["http://locahost:8080", "http://locahost:8000", "*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods = ["*"], allow_headers = ["*"])

# Dicionário para armazenar os autômatos
automata_db = {
    "dfa": {},
    "pda": {},
    "tm": {}
}

# Endpoints para AFD
@app.post("/afd/criar", response_model=Dict)
def create_afd(dfa_request: AFDRequest):
    dfa = DFA(
        states=set(dfa_request.states),
        input_symbols=set(dfa_request.input_symbols),
        transitions=dfa_request.transitions,
        initial_state=dfa_request.initial_state,
        final_states=set(dfa_request.final_states)
    )
    automata_id = f"dfa_{len(automata_db['dfa']) + 1}"
    automata_db['dfa'][automata_id] = dfa
    return {"id": automata_id, "message": "Automato criado com sucesso"}

@app.get("/afd/{automata_id}/info", response_model=Dict)
def get_afd(automata_id: str):
    if automata_id not in automata_db['dfa']:
        raise HTTPException(status_code=404, detail=automata_db)

    dfa = automata_db['dfa'][automata_id]
    return {
        "states": list(dfa.states),
        "input_symbols": list(dfa.input_symbols),
        "transitions": dfa.transitions,
        "initial_state": dfa.initial_state,
        "final_states": list(dfa.final_states)
    }

@app.post("/afd/{automata_id}/testar", response_model=Dict)
def test_afd(automata_id: str, input_string: str):
    if automata_id not in automata_db['dfa']:
        raise HTTPException(status_code=404, detail="DFA not found")
    dfa = automata_db['dfa'][automata_id]
    accepted = dfa.accepts_input(input_string)
    return {"aceito": accepted}

# Função para converter as transições do formato dict para o formato esperado

def converter_listas(d):
    if isinstance(d, list):
        return tuple(d)  # Converte listas diretamente em tuplas
    elif isinstance(d, dict):
        return {k: converter_listas(v) for k, v in d.items()}
    else:
        return d


# Endpoints para Autômatos com Pilha
@app.post("/apd/criar", response_model=Dict)
def create_apd(apd_request: APDRequest):
    pda = DPDA(
        states=set(apd_request.states),
        input_symbols=set(apd_request.input_symbols),
        stack_symbols=set(apd_request.stack_symbols),
        transitions=converter_listas(apd_request.transitions),
        initial_state=apd_request.initial_state,
        final_states=set(apd_request.final_states),
        initial_stack_symbol=apd_request.stack_start_symbol,
        acceptance_mode = "both"
    )
    automata_id = f"pda_{len(automata_db['pda']) + 1}"
    automata_db['pda'][automata_id] = pda
    return {"id": automata_id, "message": f"Automato criado com sucesso com id : {automata_id} "}

@app.get("/apd/{automata_id}/info", response_model=Dict)
def get_apd(automata_id: str):
    if automata_id not in automata_db['pda']:
        raise HTTPException(status_code=404, detail="Automato nao encontrado")
    pda = automata_db['pda'][automata_id]
    return {
        "states": list(pda.states),
        "input_symbols": list(pda.input_symbols),
        "stack_symbols": list(pda.stack_symbols),
        "transitions": pda.transitions,
        "initial_state": pda.initial_state,
        "final_states": list(pda.final_states),
        "stack_start_symbol": pda.stack_start_symbol
    }

# Endpoint para listar autômatos
@app.get("/listar-automatos", response_model=List[Dict])
def list_automata():
    automata_list = []
    for type, automata in automata_db.items():
        for automaton_id, automaton in automata.items():
            automata_list.append({
                "id": automaton_id,
                "type": type,
                "states": list(automaton.states),
                "input_symbols": list(automaton.input_symbols),
                "initial_state": automaton.initial_state,
                "final_states": list(automaton.final_states),
            })
    return automata_list

@app.post("/apd/{automata_id}/testar", response_model=Dict)
def test_apd(automata_id: str, input_string: str):

    if automata_id not in automata_db['pda']:
        raise HTTPException(status_code=404, detail="PDA not found")
    pda = automata_db['pda'][automata_id]
    accepted = pda.accepts_input(input_string)
    return {"aceito": accepted}


def convert_transitions(transitions: dict) -> Dict[str, Dict[str, Tuple[Any, str, Literal['L', 'R', 'N']]]]:
    converted = {}

    for state in transitions:
        converted[state] = {}
        for symbol in transitions[state]:
            # Pegamos o único item do dicionário interno
            next_state = list(transitions[state][symbol].keys())[0]
            actions = transitions[state][symbol][next_state].split(',')
            # Convertemos para o formato (next_state, write_symbol, direction)
            converted[state][symbol] = (next_state, actions[0], actions[1])

    return converted

# Endpoints para Máquinas de Turing
@app.post("/mt/criar", response_model=Dict)
def create_mt(tm_request: MT_Request):
    tm = DTM(
        states=set(tm_request.states),
        input_symbols=set(tm_request.input_symbols),
        tape_symbols=set(tm_request.tape_symbols),
        transitions=convert_transitions(tm_request.transitions),
        initial_state=tm_request.initial_state,
        final_states=set(tm_request.final_states),
        blank_symbol='.'
    )
    automata_id = f"tm_{len(automata_db['tm']) + 1}"
    automata_db['tm'][automata_id] = tm
    return {"id": automata_id, "message": "Maquina de turing criado com sucesso"}

@app.get("/mt/{automata_id}/info", response_model=Dict)
def get_mt(automata_id: str):
    if automata_id not in automata_db['tm']:
        raise HTTPException(status_code=404, detail="Maquina de turing nao encontrada")
    tm = automata_db['tm'][automata_id]
    return {
        "states": list(tm.states),
        "input_symbols": list(tm.input_symbols),
        "tape_symbols": list(tm.tape_symbols),
        "transitions": tm.transitions,
        "initial_state": tm.initial_state,
        "final_states": list(tm.final_states)
    }

@app.post("/mt/{automata_id}/testar", response_model=Dict)
def test_tm(automata_id: str, input_string: str):
    if automata_id not in automata_db['tm']:
        raise HTTPException(status_code=404, detail="Maquina de turing nao encontrada")
    mt = automata_db['tm'][automata_id]
    accepted = mt.accepts_input(input_string)
    return {"aceito": accepted}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)