def is_secret_free_credential_type(inputs: dict) -> bool:
    """
    Return True if a CredentialType's `inputs` schema guarantees that no instance
    of it can ever persist secret material at rest.

    This holds iff every field flagged `secret: True` is also flagged `internal:
    True`. `internal` fields are excluded from the accepted input schema by both
    Controller and EDA, so they can never be populated from user input and are
    never written to a Credential's encrypted/stored `inputs` - they are only
    ever injected transiently at execution time (e.g. an OIDC workload identity
    token). A type meeting this bar can safely be synced across services via the
    resource registry, since there is no secret value the sync would ever carry.

    Deliberately takes the raw `inputs` dict (not a model instance) so it works
    identically against Controller's and EDA's CredentialType schemas, which both
    use the same `{"fields": [...], "metadata": [...], "required": [...]}` shape.
    """
    fields = inputs.get('fields', [])
    secret_fields = {f['id'] for f in fields if f.get('secret') is True}
    internal_fields = {f['id'] for f in fields if f.get('internal') is True}
    return secret_fields.issubset(internal_fields)


def has_workload_identity_token_field(inputs: dict) -> bool:
    """
    Return True if a CredentialType's `inputs` schema declares an internal
    `workload_identity_token` field.

    A CredentialType meeting this bar expects to have a JWT injected at
    execution time (e.g. by populate_workload_identity_tokens() in Controller,
    or the equivalent resolution path in EDA) rather than ever storing a real
    token value. Used to decide whether a given CredentialInputSource's
    source_credential needs a freshly-minted workload identity token before
    its plugin backend is invoked.

    Deliberately takes the raw `inputs` dict (not a model instance), matching
    is_secret_free_credential_type() above, so it works identically against
    Controller's and EDA's CredentialType schemas.
    """
    return any(field.get('id') == 'workload_identity_token' and field.get('internal') for field in inputs.get('fields', []))
