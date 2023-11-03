from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.remove_registry_from_workspace_request import \
    RemoveRegistryFromWorkspaceRequest
from ...models.remove_registry_from_workspace_response_200 import \
    RemoveRegistryFromWorkspaceResponse200
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: RemoveRegistryFromWorkspaceRequest,

) -> Dict[str, Any]:
    url = "{}/v1/api/models/remove_registry_from_workspace".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = json_body.to_dict()



    

    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[RemoveRegistryFromWorkspaceResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RemoveRegistryFromWorkspaceResponse200.from_dict(response.json())



        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[RemoveRegistryFromWorkspaceResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: RemoveRegistryFromWorkspaceRequest,

) -> Response[RemoveRegistryFromWorkspaceResponse200]:
    """ 
    Args:
        json_body (RemoveRegistryFromWorkspaceRequest): The required information for removing a
            Model Registry from a workspace

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RemoveRegistryFromWorkspaceResponse200]
     """


    kwargs = _get_kwargs(
        client=client,
json_body=json_body,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Client,
    json_body: RemoveRegistryFromWorkspaceRequest,

) -> Optional[RemoveRegistryFromWorkspaceResponse200]:
    """ 
    Args:
        json_body (RemoveRegistryFromWorkspaceRequest): The required information for removing a
            Model Registry from a workspace

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RemoveRegistryFromWorkspaceResponse200
     """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: RemoveRegistryFromWorkspaceRequest,

) -> Response[RemoveRegistryFromWorkspaceResponse200]:
    """ 
    Args:
        json_body (RemoveRegistryFromWorkspaceRequest): The required information for removing a
            Model Registry from a workspace

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RemoveRegistryFromWorkspaceResponse200]
     """


    kwargs = _get_kwargs(
        client=client,
json_body=json_body,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Client,
    json_body: RemoveRegistryFromWorkspaceRequest,

) -> Optional[RemoveRegistryFromWorkspaceResponse200]:
    """ 
    Args:
        json_body (RemoveRegistryFromWorkspaceRequest): The required information for removing a
            Model Registry from a workspace

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RemoveRegistryFromWorkspaceResponse200
     """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
