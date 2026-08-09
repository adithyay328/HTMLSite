"""
This module implements the core
HTML generation code. Stupid simple.
"""

from typing import List
import functools

# Define the core function to create HTML tags
def _tagCore(tagName: str, *args: List[str], **kwargs: List[str]) -> str:
  result = f"<{tagName}"
  for k, v in kwargs.items():
    if k == "className":
      result += f' class="{v}" '
    else:
      result += f' {k}="{v}" '
  result += ">" + "".join(args) + f"</{tagName}>"
  return result

# List of supported HTML tags
_supportedTags = [
  "Head", "Link", "Body", "Div",
  "P", "A", "Title", "Meta", "Ul", "Li", "Span",
  "Figure", "Figcaption"
]

# Add all heading tags (H1-H6)
for i in range(1, 7):
  _supportedTags.append(f"H{i}")

# Create partial functions for each HTML tag
for tag in _supportedTags:
  globals()[tag] = functools.partial(_tagCore, tag.lower())

def HTML(*args: List[str], **kwargs: List[str]) -> str:
  """Generate HTML document with DOCTYPE"""
  return f"<!DOCTYPE html>\n" + _tagCore("html", *args, **kwargs)

def Br(repeats : int = 1) -> str:
  """
  Generate a line break tag,
  which is syntactically
  different than a normal
  HTML tag.

  Also, to make life a lot easier,
  this one can take in a number allowing
  for us to repeat breaks over and over again.
  Not the same as HTML spec, but a nice creature
  comfort.
  """
  return "<br>" * repeats

async def Img(src, width: str = None, height: str = None, alt: str = "", **kwargs) -> str:
  """
  Generate a self-closing <img> tag.

  src is expected to be an awaitable (e.g. a Task from web2local).
  Width/height can be px values like "300" or CSS values like "50%".
  Any extra kwargs become HTML attributes.
  """
  resolved_src = await src
  result = f'<img src="{resolved_src}" alt="{alt}"'
  if width:
    result += f' width="{width}"'
  if height:
    result += f' height="{height}"'
  for k, v in kwargs.items():
    if k == "className":
      result += f' class="{v}"'
    else:
      result += f' {k}="{v}"'
  result += ">"
  return result
