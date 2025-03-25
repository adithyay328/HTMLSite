from adihtml.core import *
from adihtml import snippets

intro = Div ( 
  P ( """The equations for DDPM, the original and most
     popular class of Diffusion models, has some
     pretty gnarly math behind it. But, it turns out it's
     not too bad. Let's derive it!""" )
  , Br(2),
  P ( """It turns out, you can build an understanding
     of how to make diffusion models work by working
     in 2 steps:""" ),
  Ul(
    Li("""First, derive the equations for forwards and backwards
        for a single sample, assuming a perfect model i.e. you know exactly what noise was added"""),
    Li("""Second, substitute in the model that estimates the noise from a sample. In theory, requires no change in the forward or backwards code, just build a U-Net model and put its fowrard cal in place of the function that knows the perfect noise""") 
),
  P("""If that doesn't make much sense yet, that's fine. We'll go through more of it as we go.""")

)

out = HTML (
  Head(
    Title("Adi"),
    snippets.V1_headPreamble(),
    snippets.V1_katexScript()
  ),
  Div (
    H2("Deriving the equations for DDPM"),
    intro,
    className="standardContent"
  )
)

with open ("index.html", "w") as f:
  f.write(str(out))
