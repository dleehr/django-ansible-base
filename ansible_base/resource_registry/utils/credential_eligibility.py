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
