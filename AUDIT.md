# Audit Record

Audit date: 2026-08-25

## Automated results

- GenVM lint and SDK validation: PASS
- Strict Pyright through genvm-lint: PASS
- Direct-mode tests: 7 PASS
- Five-validator GLSim integration: 1 PASS
- ABI regenerated from final source: PASS
- Pinned runner header: PASS
- Dependency vulnerability audit: PASS, zero known vulnerabilities
- Full-workspace structural originality scan: PASS, 121 contracts scanned; every nearest external match is below 0.35 and has a different public method shape
- StudioNet: PASS - fresh owner-isolated wallets, all transactions finalized and executed successfully, deployed source/schema matched, and mechanism-specific bound state read back
- GitHub publication: PASS - private remote and clean one-commit reachable history verified

## Artifact hashes

- Source: `82bb9e60af2cce6e80c0b98891a96a23ead9dfdcf4b2e307538c1555662aa1f7`
- ABI: `8861690a73eaf0dcbef353d7ba1d5511959b145790c2b11405a346581607dc26`

## Manual findings

The substantive validator independently reruns the task. The contract documents caller-attested source limitations, public-data exposure, role boundaries, terminal states, and residual risk. It joins semantic route screening to ordered custody and numeric envelope enforcement. The StudioNet manifest records the contract address, transaction receipts, fresh public test roles, exact source and schema readback, and the mechanism-specific terminal assertion.
