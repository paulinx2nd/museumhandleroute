# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators agree on SAFE or REVISE and the exact flagged-stop mask using handling text only. Code checks custodian order and environmental bounds; an out-of-envelope reading places the route on HOLD until the curator continues or aborts.
- External world: No live source is fetched. Object requirements, route steps, and sensor readings are public caller attestations; sensor hardware is not authenticated.

## Event path

register object envelope -> open ordered route -> consensus handling screen -> custodian attestations -> curator excursion decision -> delivery or abort

## Actors

- curator
- ordered custodians
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

Code checks custodian order and environmental bounds; an out-of-envelope reading places the route on HOLD until the curator continues or aborts. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `82bb9e60af2cce6e80c0b98891a96a23ead9dfdcf4b2e307538c1555662aa1f7`.
