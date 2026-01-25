from oauth2_provider.oauth2_validators import OAuth2Validator

from .controller import AutomationControllerJobScope


class CustomValidator(OAuth2Validator):

    # oidc_claim_scope = { c: AutomationControllerJobScope.name for c in claims}

    # def get_discovery_claims(self, request):
    #  return AutomationControllerJobScope().list_claims()
    def get_discovery_claims(self, request):
        claims = super().get_discovery_claims(request)
        claims.extend(AutomationControllerJobScope().list_claims())
        return sorted(claims)


if __name__ == '__main__':
    print(CustomValidator.oidc_claim_scope)
