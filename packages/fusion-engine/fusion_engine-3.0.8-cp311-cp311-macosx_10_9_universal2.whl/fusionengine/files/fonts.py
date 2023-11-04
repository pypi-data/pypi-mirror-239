import fusionengine as fusion


class Fonts:
    def __init__(self):
        """A class that contains all the build-in fonts."""
        self.NUNITO_LIGHT = f"{list(fusion.__path__)[0]}/fonts/nunito_sans_light.ttf"
        self.SAIRACONDENSED_EXTRABOLD = (
            f"{list(fusion.__path__)[0]}/fonts/SairaCondensed-ExtraBold.ttf"
        )
