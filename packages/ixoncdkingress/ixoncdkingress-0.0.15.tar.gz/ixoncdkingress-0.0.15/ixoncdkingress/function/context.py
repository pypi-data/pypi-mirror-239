"""
Context.
"""
from typing import Any, Dict, Optional, Set

from inspect import _empty, signature

from ixoncdkingress.function.api_client import ApiClient
from ixoncdkingress.function.document_db_client import DocumentDBClient

class FunctionResource:
    """
    Describes an IXAPI resource.
    """
    public_id: str
    name: str
    custom_properties: Dict[str, Any]
    permissions: Optional[Set[str]]

    def __init__(
            self,
            public_id: str,
            name: str,
            custom_properties: Dict[str, Any],
            permissions: Optional[Set[str]]
        ) -> None:
        self.public_id = public_id
        self.name = name
        self.custom_properties = custom_properties
        self.permissions = permissions

    def __repr__(self) -> str:
        return (
            '<FunctionResource'
            f' public_id={self.public_id},'
            f' name={self.name},'
            f' custom_properties={repr(self.custom_properties)},'
            f' permissions={repr(self.permissions)},'
            f'>'
        )

class FunctionContext:
    """
    The context for a Cloud Function.
    """
    config: Dict[str, str]
    api_client: ApiClient
    document_db_client: Optional[DocumentDBClient] = None
    user: Optional[FunctionResource] = None
    company: Optional[FunctionResource] = None
    asset: Optional[FunctionResource] = None
    agent: Optional[FunctionResource] = None

    @property
    def agent_or_asset(self) -> FunctionResource:
        """
        Return either an Agent or an Asset resource, depending on what's available. If both are
        available in the context, returns the Asset resource.
        """
        if self.asset:
            return self.asset

        assert self.agent
        return self.agent

    def __init__(
            self,
            config: Dict[str, str],
            api_client: ApiClient,
            document_db_client: Optional[DocumentDBClient] = None,
            user: Optional[FunctionResource] = None,
            company: Optional[FunctionResource] = None,
            asset: Optional[FunctionResource] = None,
            agent: Optional[FunctionResource] = None,
            **kwargs: Any
        ) -> None:
        del kwargs

        self.config = config
        self.api_client = api_client
        self.document_db_client = document_db_client
        self.user = user
        self.company = company
        self.asset = asset
        self.agent = agent

    def __repr__(self) -> str:
        return (
            f'<FunctionContext'
            f' config={repr(self.config)},'
            f' api_client={repr(self.api_client)},'
            f' document_db_client={repr(self.document_db_client)},'
            f' user={repr(self.user)},'
            f' company={repr(self.company)},'
            f' asset={repr(self.asset)},'
            f' agent={repr(self.agent)},'
            f'>'
        )

    @staticmethod
    def expose(function: Any) -> Any:
        """
        Decorator to mark a function as an exposed endpoint.
        """
        sig = signature(function)

        if not sig.parameters:
            raise Exception('Function has no argument for FunctionContext')

        # If the first function argument has a type annotation it should be of FunctionContext
        context_param = sig.parameters[next(iter(sig.parameters))]
        if (context_param.annotation is not _empty
                and context_param.annotation is not FunctionContext):
            raise Exception('First function parameter should be of type FunctionContext')

        setattr(function, 'exposed', True)

        return function
