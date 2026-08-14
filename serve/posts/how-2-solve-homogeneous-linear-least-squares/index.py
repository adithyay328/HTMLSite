from adihtml.core import *
from adihtml import snippets
from adihtml import latex

problemSetup = P(
"""
In computer vision, and many problems involving geometry, we need to solve specific types of linear least squares problems, specifically problems of the form AX=0.
""")

# Generate the HTML content
title = "Solving Homogenous Linear Least Squares"
out = HTML(
    Head(Title(title), snippets.V1_headPreamble()),
    Body(
        Div(
            H1(title),
            Br(),
            Br(),
            Br(),
            H3("Problem Setup"),
            problemSetup,
            className="standardContent",
        )
    ),
)


# Write the generated HTML to a file
def writeHTML():
    with open(__file__.replace(".py", ".html"), "w") as f:
        f.write(out)


writeHTML()
