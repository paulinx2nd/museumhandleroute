# Source Provenance

## Collection behavior

No live source is fetched. Object requirements, route steps, and sensor readings are public caller attestations; sensor hardware is not authenticated.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `82bb9e60af2cce6e80c0b98891a96a23ead9dfdcf4b2e307538c1555662aa1f7`
- ABI SHA-256: `8861690a73eaf0dcbef353d7ba1d5511959b145790c2b11405a346581607dc26`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
