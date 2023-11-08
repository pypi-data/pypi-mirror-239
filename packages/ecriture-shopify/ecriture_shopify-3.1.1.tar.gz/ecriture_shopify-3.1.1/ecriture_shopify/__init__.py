# to ease import from package
from ecriture_shopify.main import shopify_to_ec  # noqa
from ecriture_shopify.tools.exceptions import (ShopifyError, ShopifyFileEmptyError,  # noqa
                                               ShopifyFormatError)


# la version est définie ici et dans pyproject.toml. La cohérence est vérifiée dans pytest
__version__ = "3.1.1"
