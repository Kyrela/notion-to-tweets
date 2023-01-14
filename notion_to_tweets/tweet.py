__all__ = ("Tweet",)

from .media import Media

class Tweet:
    def __init__(self, text: str, medias: list[Media] = None):
        self.content = text
        self.medias = medias or []

    @property
    def content(self) -> str:
        return self._content

    @content.setter
    def content(self, value: str):
        value = value.strip()
        if len(value) > 280:
            raise ValueError("Tweet cannot be longer than 280 characters")
        self._content = value

    @property
    def medias(self) -> tuple[Media]:
        return tuple(self._medias)

    @medias.setter
    def medias(self, value: list[Media]):
        if len(value) > 4:
            raise ValueError("Tweet cannot have more than 4 medias")
        self._medias = value

    def append(self, value):
        if isinstance(value, str):
            self.content += "\n\n" + value
        elif isinstance(value, Media):
            if len(self.medias) == 4:
                raise ValueError("Tweet cannot have more than 4 medias")
            self._medias.append(value)

    def __str__(self):
        md_lines = []
        for line in self.content.splitlines():
            md_lines.append(f"> {line}")
        for media in self.medias:
            md_lines.append(f"> {media}")

        return "\n".join(md_lines)

    def __repr__(self):
        return f"Tweet({self.content!r}, {self.medias!r})"
