from setuptools import setup, find_packages

description = """
`keycloakfastsso` est un package Python qui facilite l'intégration de l'authentification Keycloak dans des applications construites avec le framework web FastAPI.
"""
# Lis la version depuis le fichier __init__.py
# __version__ = None
setup(
    name="KeycloakFastSso",
    version='2023.13.0',
    url="https://github.com/alexandre-meline/keycloakfasty",
    author="Alexandre Meline",
    author_email="alexandre.meline.dev@gmail.com",
    long_description=description,
    packages=find_packages(),  
    install_requires=[], 
)