from adihtml.core import *
from adihtml import snippets


out = HTML(
    Head(
        Title("How to Solve Homogeneous Linear Least Squares"),
        snippets.V1_headPreamble(),
    ),
    Body(
        Div(
            H1("How to Solve Homogeneous Linear Least Squares"),
            H2("Problem setup"),
            P(
                "Given a matrix A, we want a non-zero vector x that minimizes "
                "the homogeneous least-squares objective ||Ax||_2."
            ),
            P(
                "Without a constraint, x = 0 minimizes the objective for every "
                "matrix A, so the usual problem cannot identify a useful direction. "
                "We instead require x to have unit norm."
            ),
            H2("Success criteria"),
            P(
                "The post contains a proof of a proposition that identifies the "
                "unit-norm minimizer of the homogeneous linear least-squares "
                "objective, and includes an unexecuted two-line NumPy example that "
                "obtains the SVD solution."
            ),
            H2("Relevant background"),
            P(
                "We use the singular value decomposition A = U Sigma V^T, where U "
                "and V are orthogonal. Orthogonal matrices preserve the Euclidean "
                "norm, so ||Uy||_2 = ||y||_2 and ||Vy||_2 = ||y||_2."
            ),
            H2("Method"),
            P("The derivation will be developed in the next section of this draft."),
            H2("Remarks"),
            P("To be developed."),
            H2("Results"),
            P("To be developed."),
            H2("Addendums"),
            P("To be developed."),
            className="standardContent",
        )
    ),
)


def writeHTML():
    with open(__file__.replace(".py", ".html"), "w", encoding="utf-8") as f:
        f.write(out)


writeHTML()
