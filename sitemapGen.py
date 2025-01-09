"""
Autogenerates a sitemap
from the HTML files in /serve
"""
import os
import subprocess

if __name__ == "__main__":
  # First, run find to get
  # all html files
  allHTMLFiles = subprocess.check_output("find ./serve -name '*.html'", shell=True).decode("utf-8").split("\n")[:-1]

  # Replace ./serve with https://www.adiy.io/
  allHTMLFiles = [ fName.replace("./serve", "https://adiy.io") for fName in allHTMLFiles ]

  # Now, construct our sitemap XML
  sitemapXML = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
  
  for fName in allHTMLFiles:
    sitemapXML += f"""
      <url>
        <loc>{fName}</loc>
        <changefreq>monthly</changefreq>
      </url>
    """
  
  sitemapXML += "</urlset>"

  # Write to serve/sitemap.xml
  os.system("rm ./serve/sitemap.xml")
  with open("./serve/sitemap.xml", "w") as f:
    f.write(sitemapXML)