import fusionengine as fusion


class DebugFiles:
    def __init__(self):
        """A class that contains all the debug files."""
        self.DEBUGIMAGE = f"{list(fusion.__path__)[0]}/debugfiles/fe.png"
