import pytest

from ansible_base.lib.workload_identity import EDACredentialResolutionScope


def test_list_claims():
    """
    Test that EDACredentialResolutionScope defines the correct set of claims.
    """
    expected_claims = {
        'aap_eda_organization_name',
        'aap_eda_organization_id',
        'aap_eda_target_credential_name',
        'aap_eda_target_credential_id',
        'aap_eda_source_credential_name',
        'aap_eda_source_credential_id',
    }

    scope = EDACredentialResolutionScope()
    actual_claims = set(scope.list_claims())

    assert actual_claims == expected_claims


def test_get_target_claim_names_to_sub_stubs():
    """
    Test that get_target_claim_names_to_sub_stubs returns the correct mapping
    of claim names to their sub claim stubs.
    """
    expected_mapping = {
        'aap_eda_organization_name': 'organization',
        'aap_eda_target_credential_name': 'credential',
    }

    actual_mapping = EDACredentialResolutionScope.get_target_claim_names_to_sub_stubs()

    assert actual_mapping == expected_mapping


def test_get_target_claim_names_to_sub_stubs_keys_are_valid_claims():
    """
    Test that all keys in the target claim names mapping are valid claims
    defined in the scope.
    """
    mapping = EDACredentialResolutionScope.get_target_claim_names_to_sub_stubs()
    all_claims = set(EDACredentialResolutionScope.list_claims())

    for claim_name in mapping.keys():
        assert claim_name in all_claims, f"{claim_name} is not a valid claim in EDACredentialResolutionScope"


@pytest.mark.parametrize(
    "workload_claims,expected_sub_claim",
    [
        (
            {
                'aap_eda_organization_name': 'my-org',
                'aap_eda_target_credential_name': 'my-credential',
            },
            "workload_type:aap_eda_automation_credential_resolution:organization:my-org:credential:my-credential",
        ),
        (
            {
                'aap_eda_organization_name': '',
                'aap_eda_target_credential_name': '',
            },
            "workload_type:aap_eda_automation_credential_resolution:organization::credential:",
        ),
        (
            {'aap_eda_target_credential_name': 'my-credential'},
            "workload_type:aap_eda_automation_credential_resolution:organization::credential:my-credential",
        ),
    ],
)
def test_generate_sub_claim(workload_claims, expected_sub_claim):
    """
    Test that generate_sub_claim produces the correct sub claim string
    with full values, empty values, and missing keys.
    """
    actual_sub_claim = EDACredentialResolutionScope.generate_sub_claim(workload_claims)
    assert actual_sub_claim == expected_sub_claim
