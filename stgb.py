#!/usr/bin/env python3

import sys
import json
import re
from html.parser import HTMLParser

h_depth = {
  "h0": 0,
  "h1": 1,
  "h2": 2,
  "h3": 3,
  "h4": 4,
  "h5": 5,
  "h6": 6,
}

def attrs_string(attrs):
  res = ""
  for (k, v) in attrs:
    res += f"{k}=\"{v}\" "
  return res

def sanitize_title(title):
  res = title.strip()
  res = res.replace("\n", " ")
  if title.endswith(" -"):
    res = title[:-2]
  res = res.replace(" - ", " – ")
  return res

def parse_section(title):
  match = re.match("^§ ([\d]{1,3}[a-z]{0,1}) ", title)
  if match:
    return match.group(1)
  else:
    return None

class MyHTMLParser(HTMLParser):
    # Current heading stack
    stack = [("h0", "")]
    # Metadata structure, for JSON output
    structure = dict()
    # The HTML output
    output = ""
    # The name of the h* tag we are in right now. None otherwise. This is not
    # about the chapter, just about the tag.
    in_heading = None
    # The mapping from section to divs that reference it.
    sections = dict()

    def handle_starttag(self, tag, attrs):
        indent = len(self.stack) * "  "
        if tag in h_depth.keys():
          for (k, v) in attrs:
            if k == "id":
              div_id = f"{v}-div"
              self.in_heading = div_id
              if not div_id in self.structure:
                self.structure[div_id] = dict()
                self.structure[div_id]["level"] = tag
              while h_depth[self.stack[-1][0]] >= h_depth[tag]:
                indent = len(self.stack) * "  "
                self.output += f"{indent}</div>\n"
                self.stack.pop()
              self.structure[div_id]["part_of"] = [e[1] for e in self.stack if e[1] != ""]
              self.stack.append((tag, div_id))
              self.output += f"{indent}<div id=\"{div_id}\" class=\"{tag} h\">\n"
        indent = len(self.stack) * "  "
        self.output += f"{indent}  <{tag} {attrs_string(attrs)}>\n"

    def handle_endtag(self, tag):
          self.in_heading = None
          indent = len(self.stack) * "  "
          self.output += f"{indent}  </{tag}>\n"

    def handle_data(self, data):
        if self.in_heading:
          sanitized_title = sanitize_title(data)
          self.structure[self.in_heading]["title"] = sanitized_title
          self.structure[self.in_heading]["section"] = parse_section(sanitized_title)
        else:
          (_, div_id) = self.stack[-1]
          for s in re.findall(" ([\d]{1,3}[a-z]{0,1})", data):
            if not s in self.sections:
              self.sections[s] = [div_id]
            else:
              self.sections[s].append(div_id)
        indent = len(self.stack) * "  "
        for line in data.splitlines():
          self.output += f"{indent}    {line}\n"


parser = MyHTMLParser()
parser.feed(sys.stdin.read())

# Close all div's
while len(parser.stack) > 1:
  parser.stack.pop()
  indent = len(parser.stack) * "  "
  parser.output += f"{indent}</div>\n"

# Deduplicate references
for section, references in parser.sections.items():
  parser.sections[section] = list(set(references))

with open("stgb.html", "w") as f:
  f.write(parser.output)

with open("stgb.json", "w") as f:
  f.write(
    json.dumps({"structure": parser.structure, "sections": parser.sections}, indent=4)
  )

print(f"Wrote {len(parser.structure)} headings.")
