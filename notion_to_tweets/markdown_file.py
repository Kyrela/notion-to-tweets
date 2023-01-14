import os
import re

from .tweet import Tweet
from .media import Media


__all__ = ("MarkdownFile",)


class MarkdownFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.working_dir = os.path.dirname(file_path)
        self.file_name = os.path.basename(file_path)
        self.content = self._read_file()

    def _read_file(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()

    def to_tweets(self) -> list[Tweet]:

        tweets: list[Tweet] = []

        for line in self.content.splitlines():
            parsed_line: str = self._parse(line)

            if isinstance(parsed_line, Media):
                if not tweets or len(tweets[-1].medias) == 4:
                    tweets.append(Tweet(""))
                tweets[-1].append(parsed_line)
                continue

            if not parsed_line:
                continue

            if (tweets and tweets[-1].medias
                    and parsed_line == tweets[-1].medias[-1].alt):
                continue

            while len(parsed_line) > 280:
                # find last space
                last_space = parsed_line.rfind(" ", 0, 280)
                if last_space == -1:
                    last_space = 280
                tweets.append(Tweet(parsed_line[:last_space]))
                parsed_line = parsed_line[last_space + 1:]

            if parsed_line:
                if (
                    len(tweets) > 1
                    and re.fullmatch(r"[^a-z]+", tweets[-1].content)
                    and re.fullmatch(r"[^a-z]+", parsed_line)
                    and len(tweets[-1].content) + len(parsed_line) + 2 <= 280
                ):
                    tweets[-1].append(parsed_line)
                else:
                    tweets.append(Tweet(parsed_line))

        return tweets

    def _parse(self, text: str) -> str | Media:
        if match := re.fullmatch(r"!\[(.*?)]\((.+)\)", text):
            return Media(match.group(2), alt=match.group(1))

        if match := re.fullmatch(r"#+ (.+)", text):
            text = match.group(1).upper()

        # replace markdown bold text to uppercase text
        text = re.sub(r"\*\*(.+?)\*\*", lambda m: m.group(1).upper(), text)
        text = re.sub(r"__(.+?)__", lambda m: m.group(1).upper(), text)

        # replace markodwn italic text to normal text
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        text = re.sub(r"_(.+?)_", r"\1", text)

        # replace strikethrough text to text with false strikethrough with
        # this character: ̶
        text = re.sub(
            r"~~(.+?)~~", lambda m: "̶".join(list(m.group(1))) + "̶", text)

        # replace markdown links to normal text
        text = re.sub(
            r"\[(.+?)?]\((.+?)\)",
            lambda m: ((m.group(1) + ": ") if m.group(1) else "") + m.group(2),
            text)

        # delete markdown separators
        text = re.sub(r"---+", "", text)

        return text
