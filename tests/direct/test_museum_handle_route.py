"""Direct tests for route screening and ordered environmental attestations."""

import json


REQUIREMENTS = "Keep the framed paper work upright, avoid direct light and vibration, use two-person handling at every transfer, and do not remove the sealed backing board."


def _address(value):
    if isinstance(value, (bytes, bytearray)):
        return "0x" + bytes(value).hex()
    return str(value)


def _object(contract, direct_vm, curator):
    direct_vm.sender = curator
    return contract.register_object("PRINT-A", "Framed paper print", REQUIREMENTS, 150, 250, 40, 60)


def _route(contract, direct_vm, curator, object_id, custodians):
    direct_vm.sender = curator
    plan = {
        "stops": [
            {"id": f"STOP-{index + 1}", "custodian": _address(custodian), "handling_step": "Keep the work upright in its sealed crate and use two-person handling through the transfer."}
            for index, custodian in enumerate(custodians)
        ]
    }
    return contract.open_route(object_id, "ROUTE-1", plan)


def _screen(contract, direct_vm, curator, route_id, status="SAFE", flags=None):
    direct_vm.sender = curator
    direct_vm.mock_llm(
        r".*Screen an ordered museum handling route.*",
        json.dumps({"status": status, "flagged_stop_ids": flags or []}),
    )
    contract.screen_route(route_id)


def test_route_screening_binds_safe_plan(contract, direct_vm, direct_alice, direct_bob):
    object_id = _object(contract, direct_vm, direct_alice)
    route_id = _route(contract, direct_vm, direct_alice, object_id, [direct_bob])
    _screen(contract, direct_vm, direct_alice, route_id)
    route = contract.get_route(route_id)
    assert route["screening_status"] == "SAFE"
    assert route["status"] == "ACTIVE"


def test_flagged_route_requires_revision(contract, direct_vm, direct_alice, direct_bob):
    object_id = _object(contract, direct_vm, direct_alice)
    route_id = _route(contract, direct_vm, direct_alice, object_id, [direct_bob])
    _screen(contract, direct_vm, direct_alice, route_id, "REVISE", ["STOP-1"])
    assert contract.get_route(route_id)["status"] == "REVISION_REQUIRED"


def test_custodian_order_and_sensor_envelope_deliver_route(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    object_id = _object(contract, direct_vm, direct_alice)
    route_id = _route(contract, direct_vm, direct_alice, object_id, [direct_bob, direct_charlie])
    _screen(contract, direct_vm, direct_alice, route_id)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("stop_out_of_order"):
        contract.attest_stop(route_id, "STOP-2", 200, 50, "Trying to attest the second stop before the first.")
    direct_vm.sender = direct_bob
    contract.attest_stop(route_id, "STOP-1", 200, 50, "Crate arrived upright with seals intact and no visible damage.")
    direct_vm.sender = direct_charlie
    contract.attest_stop(route_id, "STOP-2", 205, 48, "Final handoff completed upright with stable readings and intact seals.")
    assert contract.get_route(route_id)["status"] == "DELIVERED"


def test_out_of_envelope_reading_places_hold(contract, direct_vm, direct_alice, direct_bob):
    object_id = _object(contract, direct_vm, direct_alice)
    route_id = _route(contract, direct_vm, direct_alice, object_id, [direct_bob])
    _screen(contract, direct_vm, direct_alice, route_id)
    direct_vm.sender = direct_bob
    contract.attest_stop(route_id, "STOP-1", 300, 50, "Temperature was above the registered envelope at handoff.")
    assert contract.get_route(route_id)["status"] == "HOLD"


def test_only_curator_resolves_excursion(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    object_id = _object(contract, direct_vm, direct_alice)
    route_id = _route(contract, direct_vm, direct_alice, object_id, [direct_bob])
    _screen(contract, direct_vm, direct_alice, route_id)
    direct_vm.sender = direct_bob
    contract.attest_stop(route_id, "STOP-1", 300, 50, "Temperature was above the registered envelope at handoff.")
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_curator"):
        contract.resolve_excursion(route_id, False, "An unrelated account cannot resolve the environmental excursion.")


def test_curator_can_abort_after_excursion(contract, direct_vm, direct_alice, direct_bob):
    object_id = _object(contract, direct_vm, direct_alice)
    route_id = _route(contract, direct_vm, direct_alice, object_id, [direct_bob])
    _screen(contract, direct_vm, direct_alice, route_id)
    direct_vm.sender = direct_bob
    contract.attest_stop(route_id, "STOP-1", 300, 50, "Temperature was above the registered envelope at handoff.")
    direct_vm.sender = direct_alice
    contract.resolve_excursion(route_id, False, "Curator aborts the route so conservation staff can inspect the object.")
    assert contract.get_route(route_id)["status"] == "ABORTED"


def test_safe_model_output_cannot_include_flags(contract, direct_vm, direct_alice, direct_bob):
    object_id = _object(contract, direct_vm, direct_alice)
    route_id = _route(contract, direct_vm, direct_alice, object_id, [direct_bob])
    direct_vm.mock_llm(
        r".*Screen an ordered museum handling route.*",
        json.dumps({"status": "SAFE", "flagged_stop_ids": ["STOP-1"]}),
    )
    with direct_vm.expect_revert("safe_route_has_flags"):
        contract.screen_route(route_id)
    assert contract.get_route(route_id)["status"] == "DRAFT"
