from ansible_base.resource_registry.utils.credential_eligibility import (
    has_workload_identity_token_field,
    is_secret_free_credential_type,
)


def test_is_secret_free_credential_type_no_secret_fields():
    inputs = {"fields": [{"id": "url", "type": "string"}]}
    assert is_secret_free_credential_type(inputs) is True


def test_is_secret_free_credential_type_secret_is_internal():
    inputs = {
        "fields": [
            {"id": "url", "type": "string"},
            {"id": "workload_identity_token", "type": "string", "secret": True, "internal": True},
        ]
    }
    assert is_secret_free_credential_type(inputs) is True


def test_is_secret_free_credential_type_secret_not_internal():
    inputs = {
        "fields": [
            {"id": "password", "type": "string", "secret": True},
        ]
    }
    assert is_secret_free_credential_type(inputs) is False


def test_has_workload_identity_token_field_present():
    inputs = {
        "fields": [
            {"id": "url", "type": "string"},
            {"id": "workload_identity_token", "type": "string", "secret": True, "internal": True},
        ]
    }
    assert has_workload_identity_token_field(inputs) is True


def test_has_workload_identity_token_field_not_internal():
    """A field merely named workload_identity_token isn't enough without internal: True."""
    inputs = {"fields": [{"id": "workload_identity_token", "type": "string", "secret": True}]}
    assert has_workload_identity_token_field(inputs) is False


def test_has_workload_identity_token_field_absent():
    inputs = {"fields": [{"id": "url", "type": "string"}]}
    assert has_workload_identity_token_field(inputs) is False


def test_has_workload_identity_token_field_empty_inputs():
    assert has_workload_identity_token_field({}) is False
