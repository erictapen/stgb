#!/usr/bin/env python3

from html.parser import HTMLParser

intendation = {
  "h1": " ",
  "h2": "  ",
  "h3": "   ",
  "h4": "    ",
  "h5": "     ",
  "h6": "      ",
  "h7": "       ",
}

class MyHTMLParser(HTMLParser):
    current_tag = (None, None)

    def handle_starttag(self, tag, attrs):
        if tag in intendation.keys():
          for (k, v) in attrs:
            if k == "id":
              # print(f"{intendation[tag]}{v}")
              self.current_tag = (tag, v)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if not self.current_tag == (None, None):
          (tag, _) = self.current_tag
          data = data.replace("\n", " ")
          print(f"{intendation[tag]}{intendation[tag]}{data}")
          self.current_tag = (None, None)


parser = MyHTMLParser()
with open("stgb.html") as f:
   parser.feed(f.read())
