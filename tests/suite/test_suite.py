# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the Apache 2.0 License.

import reconfiguration
import recovery
import rekey
import memberclient

from inspect import signature, Parameter

# This suite tests that rekeying, network configuration changes
# and recoveries can be interleaved
suite_rekey_recovery = [
    recovery.test,
    reconfiguration.test_add_node,
    rekey.test,
    reconfiguration.test_add_node,
    recovery.test,
    rekey.test,
    reconfiguration.test_add_node,
]

# This suite tests that membership changes and recoveries can be interleaved
suite_membership_recovery = [
    memberclient.test_add_member,
    recovery.test,
    memberclient.test_retire_member,
    recovery.test,
    memberclient.test_set_recovery_threshold,
    recovery.test,
    memberclient.test_update_recovery_shares,
    recovery.test,
]


full_suite = []
full_suite.extend(suite_rekey_recovery)
full_suite.extend(suite_membership_recovery)

#
# Test functions are expected to be in the following format:
#
# @requirements_decorator (see suite/test_requirements.py)
def test_example(network, args):
    # Test logic, e.g. issuing transaction or adding a node
    return network


def test_name(test):
    return f"{test.__module__}.{test.__name__}"


def validate_tests_signature(suite):
    """
    Validates that the test functions signatures are in the correct format
    """
    valid_sig = signature(test_example)

    for test in suite:
        sig = signature(test)

        assert len(sig.parameters) >= len(
            valid_sig.parameters
        ), f"{test_name(test)} should have at least {len(valid_sig.parameters)} parameters (only has {len(sig.parameters)})"

        p_index = 0
        for p, v in zip(sig.parameters.items(), valid_sig.parameters.items()):
            assert (
                p[0] == v[0]
            ), f'Signature of {test_name(test)} does not contain "{v[0]}" parameter in the right order'
            p_index += 1

        for p in list(sig.parameters.values())[p_index:]:
            assert (
                p.default is not Parameter.empty
            ), f'Signature of {test_name(test)} includes custom non-defaulted parameter "{p}"'
