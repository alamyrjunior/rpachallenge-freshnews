from RPA.Robocorp.Storage import Storage


def get_text_asset(asset_name):
    storage = Storage()
    asset = storage.get_text_asset(asset_name)
    return asset
