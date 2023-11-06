# Trimble Identity SDK Libraries for Python

## Installation
The Trimble Identity library is available as a PyPi package. To use this package, run the following pip command.

```
pip install trimble-id --index- url=https://<trimble-email>:<password>@artifactory.trimble.tools/artifactory/api/pypi/trimblecloudflatform-engagement-pypi/simple --extra-index-url=https://pypi.python.org/simple
```

### Well-Known URL endpoint
The well-known URL endpoint is used to retrieve the authorization, token and user info endpoints for a given environment. The following endpoints are available for the staging and production environments:

<table>
    <tbody>
        <tr>
            <th>Staging</th>
            <td>https://stage.id.trimblecloud.com/.well-known/openid-configuration</td>
        </tr>
        <tr>
            <th>Production</th>
            <td>https://id.trimble.com/.well-known/openid-configuration</td>
        </tr>
    </tbody>
</table>

## OpenID Endpoint Provider

This endpoint provider is used to retrieve the endpoints from a well-known URL endpoint.

### Usage
```python
from trimble.id.open_id_endpoint_provider import OpenIdEndpointProvider

endpoint_provider = OpenIdEndpointProvider("open_id_configuration_url")
endpoint = await endpoint_provider.retrieve_authorization_endpoint()
```

## Fixed Endpoint Provider

This endpoint provider is used to provide a fixed set of endpoints.

### Usage
```python
from trimble.id.fixed_endpoint_provider import FixedEndpointProvider

endpoint_provider = FixedEndpointProvider("https://authorization.url", "https://token.url", "https://userinfo.url")
endpoint = await endpoint_provider.retrieve_authorization_endpoint()
```

## Client Credential Token Provider

This token provider is used to retrieve an access token using the client credentials grant type.

### Usage
```python
from trimble.id.client_credential_token_provider import ClientCredentialTokenProvider

token_provider = ClientCredentialTokenProvider(endpoint_provider, "consumer_key", "consumer_secret").with_scopes(["scope"])

access_token = await token_provider.retrieve_token()
```

## Bearer Token HTTP Client Provider

It is possible to use the trimble-id library to retrieve an HttpClient with the appropriate authorization header set. This can be used to make requests to the Trimble Cloud Core Platform APIs.

### Usage
```python
from trimble.id.bearer_token_http_client_provider import BearerTokenHttpClientProvider

http_client_provider = BearerTokenHttpClientProvider(token_provider, "base_url")
http_client = await http_client_provider.retrieve_client()
```