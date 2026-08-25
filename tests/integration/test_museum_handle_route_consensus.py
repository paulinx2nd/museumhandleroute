"""Five-validator GLSim flow for screened and attested museum transfer."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context():
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {"Screen an ordered museum handling route": json.dumps({"status": "SAFE", "flagged_stop_ids": []})}},
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_screen_and_ordered_delivery():
    curator_account, first_custodian_account, second_custodian_account = create_accounts(3)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "museum_handle_route.py")
    deployed = factory.deploy_contract_tx(args=[], account=curator_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    curator = factory.build_contract(address, account=curator_account)
    first_custodian = factory.build_contract(address, account=first_custodian_account)
    second_custodian = factory.build_contract(address, account=second_custodian_account)
    object_id = f"{str(curator_account.address).lower()}:PRINT-A"
    route_id = f"{str(curator_account.address).lower()}:ROUTE-1"
    requirements = "Keep the framed paper work upright, avoid direct light and vibration, use two-person handling at every transfer, and do not remove the sealed backing board."
    _ok(curator.register_object(args=["PRINT-A", "Framed paper print", requirements, 150, 250, 40, 60]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    plan = {"stops": [{"id": "STOP-1", "custodian": str(first_custodian_account.address), "handling_step": "Keep the work upright in its sealed crate and use two-person handling through the transfer."}, {"id": "STOP-2", "custodian": str(second_custodian_account.address), "handling_step": "Keep the work upright in its sealed crate and use two-person handling through the transfer."}]}
    _ok(curator.open_route(args=[object_id, "ROUTE-1", plan]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(curator.screen_route(args=[route_id]).transact(transaction_context=_context(), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(first_custodian.attest_stop(args=[route_id, "STOP-1", 200, 50, "Crate arrived upright with seals intact and no visible damage."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(second_custodian.attest_stop(args=[route_id, "STOP-2", 205, 48, "Final handoff completed upright with stable readings and intact seals."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert curator.get_route(args=[route_id]).call()["status"] == "DELIVERED"
