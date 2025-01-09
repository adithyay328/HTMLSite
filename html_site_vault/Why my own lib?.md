In the past for my personal sites, I used a lot of existing tools, like Hugo, Next JS, MDX, all that fancy stuff. While all cool and teaching me some jargon and random shit, none of them were really good for what I wanted.

So what do I want? What kind of tool do I want to be able to author websites with?
1. Lightweight. Having to install an entire package or framework, with fancy code optimizer, bundlers, custom package managers, and even basic compilers is overkill. This invalidated normal SSGs like Hugo, and also tools like Next and MDX; it's too complicated, and if you were want to build anything weird, it's hard to even know how to do it. Being close to HTML is great
2. Modular/component oriented. This was the original reason I decided on Next; **components**. Being ale to write components once, and then reuse them, instead of copy pasting as in native HTML, is a god send. Native HTML is a pita like that
3. Performant, both on client and dev side. I want the core website to be able to load super fast, which is helped with being mostly a static site and all that. Being lightweight and close to HTML is optimal. Being fast on the dev side also matters, but not nearly as much
4. Flexible. While it's great to be able to reuse components and do the same stuff most of the time, being able to easily say "screw this!" and just make a fully custom UI for one page is awesome. This was a part of where Hugo failed; it was way too restrictive on this front

My HTML site gen library is, or at least will develop into, all of these things. The core philosophy is simple; we define a bunch of functions, each of which emits an HTML string as its output. All the core components in HTML are implemented using Python functool partials and some other dirty tricks, allowing "HTML" code that looks like this:
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

past = Div(
  P("In the past I"),
  Ul(
    Li("interned as a Deep Learning Intern at Silicon Valley Bank(May 2022 - January 2023), where I worked on Graph Neural Nets for investment predictions"),
    Li("was president at the ASU Machine Learning Club, where I taught ML, Deep Learning and more to interested members"),
    Li('was an undergrad researcher at ', A("ASU DREAM Lab", href="https://dreams-lab.replit.app/"), " working on NeRF/View Synthesis"),
    Li('won at some hackathons, including ', A("DataFest @ ASU", href="https://www.linkedin.com/feed/update/urn:li:activity:7118055246525841408/"), ", ", A("ASU AI In Education", href="https://news.asu.edu/20231214-hackathon-leverages-ai-improve-learner-outcomes-educational-access"), " and ", A("SVB @ ASU 2021", href="https://www.linkedin.com/feed/update/urn:li:activity:6924447358961291264/"))
  ),
)

writingUp = Div(
  P("I'm currently writing up"),
  Ul(
    Li("a whirlwind tour of ML, going over some of the topics we would normally cover at the ML club"),
    Li('an explainer for the proof for gradient descent; a lot of it is detailed nicely by ', A("this article", href="https://arxiv.org/pdf/2301.11235.pdf"), ", but I want to go through it myself"),
    Li("a derivation for the SVD Solution to Homogenous LLS. I have it on my old site, but haven't moved it here yet. It's pretty useful in V-SLAM, from triangulation to Fundamental/Essential Matrix computations"),
    Li("a post on the basics of vector search(LSH, HNSW, etc). They're a super cool application of Neural Nets, and fascinated me during my freshman year"),
  ),
)

tinkerProjects = Div(
  P("For fun, I've been working on"),
  Ul(
    Li(A("a toy scalar-only AutoGrad library", href="https://github.com/adithyay328/AdiGrad/tree/develop"), " I built, inspired by ", A("MicroGrad", href="https://github.com/karpathy/micrograd"), " by ", A("Karpathy", href="https://karpathy.ai/"), " - not very performant, but can fit Linear Models and MNIST MLP, and in theory can handle most models"),
    Li(A("SimpleVAE", href="https://github.com/adithyay328/SimpleVAE"), ": some simple VAEs I've trained up, as stepping stones towards building an LDM for NeRF supervision."),
    Li(A("Linear Regression in OCAML", href="https://github.com/adithyay328/OCAMLLinearRegression/blob/develop/ocaml_lin_reg/bin/main.ml"), ": out of curiosity about how OCAML works, I just built a Linear Regression model in it. As it turns out, OCAML is pretty nice.")
  ),
)

buildLog = Div(
  P("Some things I learned to build from scratch, written with all the failures I had along the way:"),
  Ul(
    Li(   A("A scalar valued factor graph I built from scratch", href="/projects/factor_graph_from_scratch")   )
  )
)

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

Some other neat features:
- Being Python, it can easily call into other sub-routines, and **generate programmatic visuals and content as part of the site update**. So, stuff like auto-generating a Matplotlib visual and showing it are on the table
- Simple syntax. It's just good ol python