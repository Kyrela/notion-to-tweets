__all__ = ('Media',)


class Media:
    def __init__(self, media_path: str, alt: str = None):
        self.media_path = media_path
        self.alt = alt if alt != "Untitled" and alt else None

    def __str__(self):
        return f"![]({self.media_path}) {self.alt or ''}"

    def __repr__(self):
        return f"Media({self.media_path!r}, {self.alt!r})"
