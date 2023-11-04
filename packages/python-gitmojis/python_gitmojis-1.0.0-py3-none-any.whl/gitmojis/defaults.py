from pathlib import Path
from typing import Final

import gitmojis

GITMOJI_API_URL: Final = "https://gitmoji.dev/api/gitmojis"

GITMOJI_API_KEY: Final = "gitmojis"

GITMOJI_API_PATH: Final = Path(gitmojis.__file__).parent / "assets" / "gitmojis.json"
