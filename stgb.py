#!/usr/bin/env python3

import sys
import json
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
    # Current heading stack
    stack = []
    # Metadata structure, for JSON output
    structure = dict()
    # The HTML output
    output = ""
    # The name of the h* tag we are in right now. None otherwise. This is not
    # about the chapter, only about the tag.
    in_heading = None

    def handle_starttag(self, tag, attrs):
        indent = len(self.stack) * "  "
        if tag in h_depth.keys():
          for (k, v) in attrs:
            if k == "id":
              div_id = f"{v}-div"
              self.in_heading = div_id
              if not div_id in self.structure:
                self.structure[div_id] = dict()
              if len(self.stack) > 0 and h_depth[tag] < h_depth[self.stack[-1][0]]:
                self.output += f"{indent}</div>\n"
                self.stack.pop()
              elif len(self.stack) > 0 and h_depth[tag] == h_depth[self.stack[-1][0]]:
                self.output += f"{indent}</div>\n"
                self.stack.pop()
                self.stack.append((tag, div_id))
                self.output += f"{indent}<div id=\"{div_id}\" class=\"{tag} h\" >\n"
                self.structure[div_id]["part_of"] = [e[1] for e in self.stack]
              else:
                self.stack.append((tag, div_id))
                self.output += f"{indent}<div id=\"{div_id}\" class=\"{tag} h\">\n"
                self.structure[div_id]["part_of"] = [e[1] for e in self.stack]
        indent = len(self.stack) * "  "
        self.output += f"{indent}  <{tag} {attrs_string(attrs)}>\n"

    def handle_endtag(self, tag):
          self.in_heading = None
          indent = len(self.stack) * "  "
          self.output += f"{indent}  </{tag}>\n"

    def handle_data(self, data):
        if self.in_heading:
          self.structure[self.in_heading]["title"] = data.replace("\n", " ")
        indent = len(self.stack) * "  "
        for line in data.splitlines():
          self.output += f"{indent}    {line}\n"


parser = MyHTMLParser()
parser.feed(sys.stdin.read())

while len(parser.stack) > 0:
  parser.stack.pop()
  indent = len(parser.stack) * "  "
  parser.output += f"{indent}</div>\n"

with open("stgb.html", "w") as f:
  f.write(parser.output)

with open("stgb.json", "w") as f:
  f.write(json.dumps(parser.structure, indent=4))

print(f"Wrote {len(parser.structure)} headings.")
