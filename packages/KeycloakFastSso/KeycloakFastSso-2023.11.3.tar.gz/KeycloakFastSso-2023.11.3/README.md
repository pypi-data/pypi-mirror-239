# keycloakfastsso

`keycloakfastsso` est un package Python qui facilite l'intégration de l'authentification Keycloak dans des applications construites avec le framework web FastAPI.

## Fonctionnalités

- Authentication avec bearer JWT tokens.
- Vérification de jetons JWT.
- Autorisation basée sur les rôles, les groupes et l'état de vérification de l'email de l'utilisateur dans Keycloak.
- Fournit des informations sur l'utilisateur validé.
- Outils utiles pour vérifier les rôles, les groupes et d'autres attributs utilisateur.

## Utilisation

### Middleware
Utilisez KeycloakFastSSOMiddleware pour protéger vos routes d'API. Vous devez d'abord configurer la connexion à Keycloak avec les paramètres appropriés.

```python
from fastapi import FastAPI
from keycloakfastsso.middleware import KeycloakFastSSOMiddleware

app = FastAPI()
app.add_middleware(KeycloakFastSSOMiddleware, server_url="https://my-keycloak-url/auth/", client_id="my-client-id", realm_name="my-realm-name", client_secret_key="my-client-secret-key")
```
### Décorateurs

Ces décorateurs peuvent être utilisés pour restreindre l'accès aux routes en fonction des rôles ou des groupes d'utilisateurs.

```python
from keycloakfastsso.decorators import require_role, require_group, require_scope, require_email_verified, require_active_user, require_token_type, require_resource_access, require_allowed_origin

@app.get("/require_role")
@require_role(["admin"])
def require_role_endpoint(): 
    return {"Hello": "World"}

@app.get("/require_group")
@require_group(["my_group"])
def require_group_endpoint(): 
    return {"Hello": "World"}

# other routes continue the same way 
```
  
### Utilitaires

Les utilitaires vous permettent de récupérer des informations spécifiques sur l'utilisateur actuellement authentifié.

```python
from keycloakfastsso.utils import KeycloakUtils

# In your route
@app.get("/whoami")
def who_am_i(request: Request):
    return {"user_id": KeycloakUtils.get_user_id(request)}
```

## Installation

Vous pouvez installer `keycloakfastsso` avec pip :

```bash
pip install keycloakfastsso
```

---

Pour plus d'informations sur comment utiliser ce package, consultez la documentation officielle.