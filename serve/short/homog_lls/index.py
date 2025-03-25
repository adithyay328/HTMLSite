from adihtml.core import *
from adihtml import snippets

problem = Div (
  P( """A common problem that shows up in computer vision is solving matrix equations of the
    form $$A \\vec{x} = \\vec{0}, \\text{subject to } ||x||_2 = 1 $$""" ),
  P("""
    This shows up in a lot of places, especially in operations like triangulation of 3D
    points, homography + fundamental matrix estimation, and more. They tend to arise due to
    the use of a cross product based constraint in the problem, whic shows up in similarity relations
    for homographies and in the epipolar constraint for the fundamental matrix. We'll cover this specific
    problem setup in a bit, which is known as the Direct Linear Transform, or DLT.
  """),
  Br(2)
)

normalMethods = Div(
  P("""
    If we were to naively use normal methods like the normal equations and gradient descent, we'd never
    get meaningful results, only getting the trivial i.e. zero solution for $\\vec{x}$, which is valid but
    not useful.
  """)
)

normalEquationsProof = Div(
  H2("Proof that normal equations provide trivial solution"),
  P("Proving that the normal equations don't yield meaningful solutions is trivial;"),
  P( """
    $$
    A \\vec{x} = \\vec{0} \\rightarrow \\vec{x} = (A^TA)^{-1}A^T \\vec{0} = \\vec{0}
    $$
  """ )
)

gradientDescentProof = Div(
  H3("Proof that gradient descent and other iterative methods provide trivial solution"),
)

orthogonalMatrixSubproof = Div()

derivation = Div(
  H3("Derivation of the SVD Solution"),
  P("""Deriving the SVD solution is actually rather simple, provided
    we do one intermeddaite proof, which is showing that matrix muliplying
    a vector with an orthogonal matrix does not affect the vector's magnitude."""),
  Br(2),
  P("""
    I'll do that proof now, then we can use its result.
  """),
  orthogonalMatrixSubproof,
  H2("The main derivation"),
  P("""
    Let $A \in \mathbf{R}^{m \\times n}$ be some arbitrary matrix. Let's find the constrained solution such that the solution has unit norm.
  """),
  Br(),
  P(
    """Invoking the SVD, we can rewrite $A = U \Sigma V^T$, with each resultant having the appropriate shape. 
    We now want to find $\\vec{x}$ that minimizes $||U \Sigma V^T \\vec{x}||_2$, subject
    to $||\\vec{x}||_2 = 1$"""
  ),
  Br(),
  P("""Now, using the fact that if $C$ is orthogonal then $||Cx||_2 = ||x||_2$, and the fact that $U$ is orthogonal 
  by the definition of the SVD, minimizing $||U \Sigma V^T \\vec{x}||_2$ is equivalent to minimizing
  $||\Sigma V^T \\vec{x}||_2$, where we removed the $U$ matrix entirely. Let's use this simplified objective
  going forward.
  """),
  Br(),
  P("""We now want to minimize $||\Sigma V^T \\vec{x}||_2$, subject to $||\\vec{x}||_2 = 1$. We can't
    just ignore any of the following 2 matrices since matrix multiplies don't commute. But, some simple
    algebra can get us a long way. Let $\\vec{y} = V^T\\vec{x}$. Note that since $V^T$ is also orthogonal
    by the definition of the SVD, we can say that $ ||\Sigma \\vec{y}||_2 = || \Sigma V^T \\vec{x} ||_2$, and also
    that if $||x||_2 = 1 \\rightarrow ||y||_2 = 1$, due to that same property about orthogonal matrices."""),
  Br(),
  P("""With those prior 2 equivalences, we can now solve for $\\vec{x}$ in a different way; first solve the
    equivalent problem of minimizing $||\Sigma \\vec{y}||_2$ subject to $||\\vec{y}||_2 = 1$, then
    solve for $\\vec{x}$ using $\\vec{y} = V^T \\vec{x}$."""),
  Br(),
  P(
    """That rewrite allows to simply find the minimal $y$. Note that by the definition
    of the SVD, the elements of $\Sigma$ are all non-negative and are ordered from
    greatest to lowest as you go from the top-left to the bottom right of the matrix.
    """
  ),
  Br(),
  P(
    """
    As such, we can denote the quantity $||\Sigma y||_2$ as the same as
    $\sqrt{ (\sigma_1 y_1)^2 + (\sigma_2 y_2)^2 + ... + (\sigma_n y_n)^2  }$,
    where $\sigma_n$ is the n-th element on the main diagonal of $\Sigma$.
    Since we know that $\sigma_n \leq \sigma_{n-1} \leq ... \leq \sigma_0$, it's
    apparent that if we set all the elements of $y$ to 0 but the last i.e.
    $y = [0, 0, ..., 1]^T$, we can minimize the quantity $||\Sigma y||_2$.
    """
  ),
  Br(),
  P(
    """
    Now, let's turn back to $x$ and try to solve for it. Since we know that
    \\vec{y}
    """
  )
)

out = HTML (
  Head(
    Title("Adi"),
    snippets.V1_headPreamble(),
    snippets.V1_katexScript()
  ),
  Div (
    H2("Solving Homogenous LLS"),
    problem,
    Br(), Br(), 
    normalMethods,
    normalEquationsProof,
    gradientDescentProof,
    derivation,
    className="standardContent"
  )
)

with open ("index.html", "w") as f:
  f.write(str(out))
