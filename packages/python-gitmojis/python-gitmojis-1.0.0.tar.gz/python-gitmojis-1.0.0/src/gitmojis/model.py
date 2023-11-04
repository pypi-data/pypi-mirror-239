from collections import UserList
from dataclasses import dataclass
from typing import Iterable, Literal


@dataclass(frozen=True, kw_only=True)
class Gitmoji:
    """Represents a single Gitmoji and its data.

    The data model is adapted from the schema of the original Gitmoji project.

    Attributes:
        emoji: The emoji symbol representing the Gitmoji.
        entity: The HTML entity corresponding to the Gitmoji.
        code: The Markdown code of the Gitmoji's emoji.
        description: A brief description of changes introduced by commits and pull
            requests marked by the Gitmoji.
        name: The user-defined name or identifier of the Gitmoji.
        semver: The Semantic Versioning level affected by the commits or pull requests
            marked by the emoji associated with the Gitmoji, if specified. May be `None`
            or one of the following: `"major"`, `"minor"`, `"patch"`.
    """

    emoji: str
    entity: str
    code: str
    description: str
    name: str
    semver: Literal["major", "minor", "patch"] | None


class Guide(UserList[Gitmoji]):
    """Represents a list of (a "guide" through) `Gitmoji` objects.

    This class is used to create a collection of `Gitmoji` objects, providing a simple
    framework for accessing various Gitmojis and their data.
    """

    def __init__(self, *, gitmojis: Iterable[Gitmoji] | None = None) -> None:
        """Construct a new `Guide` object.

        Args:
            gitmojis: An optional iterable of `Gitmoji` objects used to create
                the guide. If `None`, the guide is initialized as empty. Note
                that the data must be passed as a keyword argument, in contrast
                to the implementation provided by the base class.
        """
        super().__init__(gitmojis)

    @property
    def gitmojis(self) -> list[Gitmoji]:
        """Return the guide's data with a semantically meaningful attribute name."""
        return self.data
