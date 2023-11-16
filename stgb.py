#!/usr/bin/env python3

import sys
from html.parser import HTMLParser

h_depth = {
  "h1": 1,
  "h2": 2,
  "h3": 3,
  "h4": 4,
  "h5": 5,
  "h6": 6,
  "h7": 7,
}

def attrs_string(attrs):
  res = ""
  for (k, v) in attrs:
    res += f"{k}=\"{v}\" "
  return res

class MyHTMLParser(HTMLParser):
    stack = []

    def handle_starttag(self, tag, attrs):
        if tag in h_depth.keys():
          for (k, v) in attrs:
            if k == "id":
              if len(self.stack) > 0 and h_depth[tag] <= h_depth[self.stack[-1]]:
                print("</div>")
                self.stack.pop()
              else:
                self.stack.append(tag)
                print(f"<div id=\"{v}-div\">")
        indent = (len(self.stack) - 1) * "  "
        print(f"{indent}<{tag} {attrs_string(attrs)}>")

    def handle_endtag(self, tag):
          indent = (len(self.stack) - 1) * "  "
          print(f"{indent}</{tag}>")

    def handle_data(self, data):
        indent = len(self.stack) * "  "
        for line in data.splitlines():
          print(f"{indent}{line}")


parser = MyHTMLParser()
parser.feed(sys.stdin.read())

while len(parser.stack) > 0:
  parser.stack.pop()
  indent = len(parser.stack) * "  "
  print(f"{indent}</div>")
