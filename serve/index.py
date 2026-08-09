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
            className="standardContent",
        )
    ),
)


# Write the generated HTML to a file
def writeHTML():
    with open(__file__.replace(".py", ".html"), "w") as f:
        f.write(out)


writeHTML()
