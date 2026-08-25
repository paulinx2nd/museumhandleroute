# MuseumHandleRoute

A reusable museum transfer protocol that screens handling steps against an object's frozen requirements and then enforces ordered custodian sensor attestations with an excursion hold path.

## Why GenLayer

Validators agree on SAFE or REVISE and the exact flagged-stop mask using handling text only. Code checks custodian order and environmental bounds; an out-of-envelope reading places the route on HOLD until the curator continues or aborts.

## Roles

- curator
- ordered custodians
- GenLayer validators

## Lifecycle

register object envelope -> open ordered route -> consensus handling screen -> custodian attestations -> curator excursion decision -> delivery or abort

## Contract interface

- Constructor: none
- Write methods: attest_stop, cancel_draft, open_route, register_object, resolve_excursion, screen_route
- View methods: get_object, get_object_count, get_object_id, get_route, get_route_count, get_route_id
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

No live source is fetched. Object requirements, route steps, and sensor readings are public caller attestations; sensor hardware is not authenticated.

## Verification

```text
genvm-lint check contracts/museum_handle_route.py
genvm-lint typecheck contracts/museum_handle_route.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

This contract is not conservation, transport, or condition certification. Wallet roles and sensor readings remain caller-attested.

Licensed under MIT. See `LICENSE`.
