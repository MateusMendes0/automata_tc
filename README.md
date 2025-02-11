
# Como executar o projeto

## Clone o repositório

```
git clone https://github.com/seu-usuario/seu-repositorio.git
cd automata-tc
```

## Crie um ambiente virtual

```
python -m venv venv
venv\Scripts\activate
```

## Instale as dependências

```
pip install -r requirements.txt
```

## Inicie a aplicação

```
uvicorn main:app --reload

Visite http://127.0.0.1:8000
Ou http://127.0.0.1:8000/docs
```
## TIPOS

### AFD : AUTÔMATO FINITO DETERMINÍSTICO

### APD : AUTÔMATO COM PILHA

### MT : MÁQUINA DE TURING

## POST /{tipo}/criar

Tipos: afd, apd, mt.

AFD : `/afd/criar`

Body :

```json
{
  "states": ["q0", "q1", "q2"],
  "input_symbols": ["0", "1"],
  "transitions": {
    "q0": {"0": "q1", "1": "q0"},
    "q1": {"0": "q2", "1": "q0"},
    "q2": {"0": "q2", "1": "q0"}
  },
  "initial_state": "q0",
  "final_states": ["q2"]
}

```

APD : `/apd/criar`

body :

```json

{
  "states": ["q0", "q1", "q2"],
  "input_symbols": ["0", "1"],
  "stack_symbols": ["Z", "X"],
  "transitions": {
    "q0": {
      "0": {"Z": ["q1", "XZ"]}
    },
    "q1": {
      "0": {"X": ["q1", "XX"]},
      "1": {"X": ["q2", ""]}
    },
    "q2": {
      "1": {"X": ["q2", ""]}
    }
  },
  "initial_state": "q0",
  "final_states": ["q2"],
  "stack_start_symbol": "Z"
}

```



MT : `/mt/criar`

body :

```json
{
  "states": ["q0", "q1", "q2", "q3", "q4"],
  "input_symbols": ["0", "1"],
  "tape_symbols": ["0", "1", "x", "y", "."],
  "transitions": {
    "q0": {
      "0": {"q1": "x,R"},
      "y": {"q3": "y,R"}
    },
    "q1": {
      "0": {"q1": "0,R"},
      "1": {"q2": "y,L"},
      "y": {"q1": "y,R"}
    },
    "q2": {
      "0": {"q2": "0,L"},
      "x": {"q0": "x,R"},
      "y": {"q2": "y,L"}
    },
    "q3": {
      "y": {"q3": "y,R"},
      ".": {"q4": ".,R"}
    }
  },
  "initial_state": "q0",
  "final_states": ["q4"]
}


```


## POST /{tipo}/{id}/testar?input_string={string_teste}


AFD : `/afd/dfa_1/testar?input_string=0001`

Resposta : 

```json
{"aceito": true}
```

```json
{"aceito": false}
```

APD : `/apd/pda_1/testar?input_string=0001`

Resposta : 

```json
{"aceito": true}
```

```json
{"aceito": false}
```

MT : `/mt/tm_1/testar?input_string=0001`

Resposta : 

```json
{"aceito": true}
```

```json
{"aceito": false}
```


## GET /listar-automatos

Retorna uma lista de todos os autômatos criados.


## GET /{tipo}/{id}/info
Lista as informações de um Automato

AFD : `/afd/dfa_1/info`

APD : `/apd/pda_1/info`

MT : `/mt/tm_1/info`












