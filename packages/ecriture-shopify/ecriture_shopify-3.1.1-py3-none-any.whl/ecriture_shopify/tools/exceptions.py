"""exceptions to cover issues when loading customer file"""


class ShopifyError(Exception):
    pass


class ShopifyFileEmptyError(ShopifyError):
    pass


class ShopifyFormatError(ShopifyError):
    pass

# end
