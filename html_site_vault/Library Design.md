Briefly, I want to go over how this library and site are going to be laid out. The rationale for even having a lib are outlined in [[Why my own lib?]]

## Base Example Code
```
from adihtml.core import *
from adihtml import snippets

# Generate the HTML content
currently = Div(
  P("I'm currently"),
  Ul(
    Li("a junior at ASU going for a double major in CS + Math"),
    Li("an undergrad researcher working at ", A("ASU Active Perception Group", href="https://faculty.engineering.asu.edu/yezhouyang/")),
    Li("working on building a NeRF of all of Seattle from some driving data I collected"),
    Li("implementing and playing with various algos/problems in ML/CV including Diffusion Models, NeRFs, Visual-SLAM and more")
  ),
)

....

out = HTML(
  Head(
    Title("Adi"),
    snippets.V1_headPreamble()
  ),
  Body(
    Div(
      H1("Adithya ", Span("\"Adi\"", style="font-weight:400;"), " Yerramsetty"),
      Div(id="socials"),
      P("Howdy! My name's Adi. Below you'll find some things I've made public, which you hopefully find interesting/useful."),
      Br(), Br(),
      currently,
      past,
      tinkerProjects,
      # buildLog,
      writingUp,
      className="standardContent"
    )
  )
)

# Write the generated HTML to a file
def writeHTML():
  with open(__file__.replace(".py", ".html"), "w") as f:
    f.write(out)

writeHTML()
```

As we can see, it's a really simple and clean syntax. It's all native Python, with a thin( < 100 LOC ) wrapper on top of it to make HTML generation possible.

The core library( adihtml ) is stored in a separate tree in a source folder that can be built and installed in 1 shell invocation, allowing me to add snippets and core features as time goes on.

## Code Organization

I am a fan of NextJS, even thought I ditched it for this library of my own in this case. I think NextJS's routing concept is pretty nifty. As a result, **we follow the same concept**.

At its core, we have a directory called serve. This directory maps to /. Note this for later.

Every time we enter into a subdirectory, we're adding another section to the URL i.e. /serve/main will map to adiy.io/main

Now, to understand how file selection works, we just have to look at our nginx config. Internally, we allow nginx to use try_files in the following manner:
```
try_files $uri $uri/index.html $uri =404;

```
Basically, first try the URL itself, then the index.html for that dir. So, adiy.io/main would first try to access that as a file(fails) and then later would try adiy.io/main/index.html, which would indeed be a valid file to pull from.

As such, all of our python files for code gen will be named index.py. When they run, they'll dump an HTML file to their same dir with the name index.py, which will automatically be servable as a route.

Originally I wanted to maintain a separate src and assets folder, but I don't think that's needed. It's a lot easier logistically to colocate most of them, but of course you can use sub-dirs called assets if you'd like to colocate them but not mix source and html files with jpegs, for example. But that doesn't matter; each page can do it differently if it desires, which is part of my aim for flexibility as outlined in [[Why my own lib?]].

## For now
For now, that's enough. Time to actually start working on a post instead of being an architecture astronaut.