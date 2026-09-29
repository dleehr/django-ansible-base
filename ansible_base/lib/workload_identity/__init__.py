"""
Workload Identity module.

Provides scope definitions and registry for workload identity tokens.
"""

from .base import BaseWorkloadIdentityScope
from .controller import AutomationControllerJobScope
from .eda import EDACredentialResolutionScope

SCOPE_REGISTRY = {
    AutomationControllerJobScope.name: AutomationControllerJobScope,
    EDACredentialResolutionScope.name: EDACredentialResolutionScope,
}

__all__ = [
    'BaseWorkloadIdentityScope',
    'AutomationControllerJobScope',
    'EDACredentialResolutionScope',
    'SCOPE_REGISTRY',
]
