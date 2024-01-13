import os
import Ice

try:
    import IceDrive

except ImportError:
    Ice.loadSlice(
        os.path.join(
            os.path.dirname(__file__),
            "icedrive.ice",
        )
    )
