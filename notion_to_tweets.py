import argparse

from notion_to_tweets import *

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="path to input file")
ap.add_argument(
    "-o", "--output", default="tweets.md", help="path to output file")
args = ap.parse_args()


file = MarkdownFile(args.file)

with open(args.output, "w", encoding="utf-8") as f:
    f.write("\n\n".join(map(str, file.to_tweets())))
