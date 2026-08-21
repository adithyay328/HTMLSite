import os
import json

from pydantic import BaseModel, Field, ConfigDict

from adihtml.core import *
from adihtml import snippets

# Generate the HTML content
currently = Div(
    P("I'm currently"),
    Ul(
        Li("a recent CS + Math grad from ASU"),
        Li(
            "building SLAM systems and end-to-end 3D reconstruction solutions from stereo cameras"
        ),
        Li(
            "learning how to control drones and solve missions with real-time dense recontruction aboard"
        ),
    ),
)

past = Div(
    P("In the past I"),
    Ul(
        Li(
            "interned as a Deep Learning Intern at Silicon Valley Bank(May 2022 - January 2023), where I worked on Graph Neural Nets for investment predictions"
        ),
        Li(
            "was president at the ASU Machine Learning Club, where I taught ML, Deep Learning and more to interested members"
        ),
        Li(
            "was an undergrad researcher at ",
            A("ASU DREAM Lab", href="https://dreams-lab.replit.app/"),
            " working on NeRF/View Synthesis",
        ),
        Li(
            "won at some hackathons, including ",
            A(
                "DataFest @ ASU",
                href="https://www.linkedin.com/feed/update/urn:li:activity:7118055246525841408/",
            ),
            ", ",
            A(
                "ASU AI In Education",
                href="https://news.asu.edu/20231214-hackathon-leverages-ai-improve-learner-outcomes-educational-access",
            ),
            " and ",
            A(
                "SVB @ ASU 2021",
                href="https://www.linkedin.com/feed/update/urn:li:activity:6924447358961291264/",
            ),
        ),
    ),
)

# Before being done, we have to put all our posts here.
allValidPosts = [ x for x in os.listdir("./posts") if "meta.json" in os.listdir(f"./posts/{x}")]

# We assume this schema; this should be a subset of what's
# in meta.json
class MinimalMeta(BaseModel):
  model_config = ConfigDict(extra="allow")

  year : int
  month : int
  day : int
  active : bool
  title : str
  LLM_description : str

def loadJSON(p):
  with open(p, "r") as f:
    t = f.read()
    return MinimalMeta.model_validate_json(t)

# We assume your linting passed, and that has a schema. Simply
# look for the title, and then we'll inject the link
configs = [ loadJSON(f"./posts/{x}/meta.json") for x in allValidPosts ] 
pathsAndConfs = zip(allValidPosts, configs)

# Exclude any that are not active
activeConfigs = [ conf for conf in pathsAndConfs if conf[1].active ]

# Now, sory by year month day
chrono = sorted(activeConfigs, key = lambda c: f"{c[1].year}_{c[1].month}_{c[1].day}", reverse=True)

# Now, go ahead and write out the bit
postBlock = Div(
"I've written about",
Ul(
*[
    Li(A(f"{x[1].title}", href=f"./posts/{x[0]}/index.html"))
  for x in chrono]
)
)

out = HTML(
    Head(Title("Adi"), snippets.V1_headPreamble()),
    Body(
        Div(
            H1("Adithya ", Span('"Adi"', style="font-weight:400;"), " Yerramsetty"),
            Div(id="socials"),
            P(
                "Howdy! My name's Adi. Below you'll find some things I've made public, which you hopefully find interesting/useful."
            ),
            Br(),
            Br(),
            currently,
            past,
            postBlock,
            className="standardContent",
        )
    ),
)


# Write the generated HTML to a file
def writeHTML():
    with open(__file__.replace(".py", ".html"), "w") as f:
        f.write(out)


writeHTML()
