"""
OIDC Workload Identity Scope for AAP EDA.

Defines the scope and claims for EDA credential-resolution workload identity.
"""

from .base import BaseWorkloadIdentityScope


class EDACredentialResolutionScope(BaseWorkloadIdentityScope):
    """
    Default scope for AAP EDA credential-resolution workload identity.

    Covers every place EDA resolves a CredentialInputSource against an
    external secrets backend (event stream signature validation, activation
    env var/file injection, vault password lookup, AAP connection lookup) -
    they all funnel through the same resolution path, so one scope covers all
    of them, mirroring how AutomationControllerJobScope covers every unified
    job type in Controller.
    """

    name = "aap_eda_credential_resolution"
    description = "Default AAP EDA credential resolution workload identity"

    CLAIM_ORGANIZATION_NAME = 'aap_eda_organization_name'
    CLAIM_ORGANIZATION_ID = 'aap_eda_organization_id'
    CLAIM_TARGET_CREDENTIAL_NAME = 'aap_eda_target_credential_name'
    CLAIM_TARGET_CREDENTIAL_ID = 'aap_eda_target_credential_id'
    CLAIM_SOURCE_CREDENTIAL_NAME = 'aap_eda_source_credential_name'
    CLAIM_SOURCE_CREDENTIAL_ID = 'aap_eda_source_credential_id'

    @classmethod
    def list_claims(cls) -> list[str]:
        return [getattr(cls, attr) for attr in dir(cls) if attr.startswith('CLAIM_')]

    @classmethod
    def get_target_claim_names_to_sub_stubs(cls) -> dict[str, str]:
        return {
            cls.CLAIM_ORGANIZATION_NAME: "organization",
            cls.CLAIM_TARGET_CREDENTIAL_NAME: "credential",
        }
