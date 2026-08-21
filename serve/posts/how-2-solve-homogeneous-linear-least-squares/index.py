from adihtml.core import *
from adihtml import snippets
from adihtml.latex import InlineTex

problemSetup = Div(
"""
In computer vision, and many problems involving geometry, we need to solve linear least squares problems of the form Ax=0.""",
Br(), Br(),
"""It might not be clear why conventional solutions from linear algebra and other fields wouldn't work. Consider the case of finding the homogenous form of a 3D point, which must be non-zero.""",
Br(),Br(),
"""
Shortly, we will see why traditional methods are not useful in this context.
"""
)

successCriteria = Div(
H3(B("Success Criteria")),
"""
Show that traditional least squares solutions do not solve for meaningful solutions to homogenous linear least squares problems, and derive a meaningful solution with a formal proof. 
"""
)

whatDoYouMeanNotMeaningful = Div(
  H3(B("What do you mean, not meaningful?")),
  """
  Suppose we are working in computer vision, and are facing a problem of the form Ax=0, where x is a four dimensional, "homogenous" point. This means a normal vector in the first 3 dimensions, but a special "scale" factor in the last dimension. To turn it into a normal 3D vector, you divide the 3D point in the first 3 dimensions by the last dimension, and return it.""",
  Br(),
  Br(),
  """As a result, a solution that is all zeroes would imply division by zero, an invalid operation. As well, scalar multiplication in general does NOT change the true associated 3D point, meaning that constraints like unit-norm do not limit the range of points expressible.
  """,
  Br(), Br(),
  """
  So why do we care? Well, let's see what happens when you solve this kind of problem with Linear Algebra.
  """,
  Br(),
  Br(),
  InlineTex(
  """
  \\text{Suppose you have the problem }Ax=0
  \\\\
  \\text{Using the standard solution from linear algebra}
  \\begin{gather*}
  Ax=0 \\rightarrow A^TAx=0 \\\\
  x = (A^TA)^{-1}0 = 0
  \\end{gather*}
  """,
  scale=2,
  className="fit centered"
  ),
  Br(),
  """
  Now, assuming that the QR decomposition and all other OLS solvers find the same perfect solution, we have just found a solution that is ... not useful. Sure, it's a perfect solution, but we can't use it. How would a single solution for every possible A show us anything about a problem encoded in A?
  """
)

problemReframing = Div(
  H3(B("Problem Reframing")),
  """
  Now that we've shown that the normal solutions do not produce interesting solutions, let's consider what might be a useful reframing.
  """, Br(), Br(),
  """
  For one, notice that in the case of homogenous points, we need a vector that is non-zero. However, as with many problems in geomery, the exact scale does not matter, only the relative proportions. As a result, let's pick a random, simple constraint: <b>the vector X must be of unit norm i.e. length 1</b>.
  """,
  Br(), Br(),
  """
  As we shall now see, this makes our life much simpler, and gives us a solution.
  """
)

method = Div(
"""
Now, let's derive a solution to our new problem, which now takes on the form
""", Br(), 
Div(
InlineTex("\\text{minimize} ||Ax|| \\text{ subject to } ||x|| = 1", scale=2),
className="centered"
),
"""
There are 2 primary things you'll need to know to follow along:
""",
Br(),
Br(),
Div(
InlineTex(
"""
\\begin{enumerate}
\\item For any matrix $A$ that is orthogonal, $||Ax||=||x||$ \\text{ i.e. orthogonal matrices do not change norm.}
\\item The SVD operation exists, and decomposes any matrix $A$ into $$USV^T$$, where U and V are orthogonal, and S is a non-increasing diagonal matrix of non-negative real numbers
\\end{enumerate}

""", scale=2
), className=""
),
Br(),
"""
Now, it's time to derive!
""",
Br(),
)


deriving = Div(
Br(),
Div(
InlineTex(
r"""
\newcommand{\st}{~ \text{s.t.} ~ }
\newcommand{\minim}{\text{min} ~ }

\text{Suppose that we have some matrix A, and we want to solve the problem} \\ \\ $$ \minim ||Ax|| \st  ||x||=1$$
\\
\newline
Starting off, let's invoke the SVD and rewrite this as:
\\
$$ \minim ||USV^T x|| \st ||x||=1$$
\newline
\newline
Since $||USV^Tx|| = ||SV^Tx||$ by orthogonality of U,
we can reduce this to
$$\minim ||SV^Tx|| \st ||x||=1$$
\\
Given just this, it's hard to see how we'd get any useful solution.
This is where we employ a pretty standard trick; introduce a change of variables.
\\\\ By defining $y := V^Tx$, we can replace the above with the following problem:

$$\minim ||Sy|| \st ||x||=1$$

However, since $y=V^Tx$, and $V^T$ is also orthogonal, we get that
$$||x|| = ||V^Tx|| = ||y||$$
\\
and the objective can be rewritten as

$$\minim ||Sy|| \st ||y||=1$$

Now this looks a bit easier to solve.
\\\\
The important thing to remember in this case is that $S$ is non-increasing, i.e. $S_i \geq S_2 \geq ... \geq S_n$, where $S_i$ is the first member of the diagonal at the top-left, and vice-versa for $S_n$.
\\ \\
As such, we can rewrite all $S_i$ as $S_n + a_i$, where $a_i \in \mathbb{R} \land a_i \geq 0$.
\\ \\
Using this, now note that we can expand $||Sy||$ as
\begin{gather*}
||Sy|| = \sqrt{ \sum_i ((S_n + a_i)y_i)^2 } = \sqrt{ \sum_i (S_ny_i + a_iy_i)^2 } = \\
\sqrt{ \sum_i S_n^2y_i^2 + 2S_na_iy_i^2 + a_i^2y_i^2 } = \\
\sqrt{ \sum_i S_n^2y_i^2 + \sum_i 2S_na_iy_i^2 + \sum_i a_i^2y_i^2 }
\end{gather*}

You might be wondering why we did this. Well, some of you may have been able to get an idea of what $y$ must be to minimize $||Sy||$. I will propose this solution now, and show that it works.

\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}

\begin{lemma}
Given a non-increasing, non-negative diagonal matrix $S$, a global minima for the expression $||Sy|| \st ||y|| = 1$ is given by $y=[0,0, ...,1]^T$
\end{lemma}

\begin{proof}
As we only need to prove that it is \textbf{a} global minima, and not a unique one, we need to show that
$$\forall y ~ ||y|| = 1 \rightarrow ||Sy|| \geq ||S[0,0,...1]^T||$$

, taking $y$ as some unit vector, and $S$ as a non-increasing non-negative diagonal matrix, both arbitrary but fixed. Expanding that inequality out, we get
$$
\sqrt{ \sum_i S_n^2y_i^2 + \sum_i 2S_na_iy_i^2 + \sum_i a_i^2y_i^2 } \geq \sqrt{S_n^2}
$$
Now note, because $||y|| = 1$, it follows by definition that $$\sqrt{\sum_i y_i^2} = 1 \rightarrow \sum_i y_i^2 = 1$$ As well, since $S_n^2$ is a constant, it follows that
$$
\sum_i S_n^2y_i^2 = S_n^2 \sum_i y_i^2 = S_n^2
$$

Subsituting this back into the inequality, we get that
$$
\sqrt{ S_n^2 + i\sum_i 2S_na_iy_i^2 + \sum_i a_i^2y_i^2 } \geq \sqrt{S_n^2}
$$

Looking at the other 2 terms, we can easily deduce that they are both non-negative; squares cannot be negative, and both $S_n$ and $a_i$ are non-negative by construction. As a result, this inequality holds.
\end{proof}

With that out of the way, we now have Lemma 1 to use freely. As a reminder, we are trying to minimize $||Ax|| \st ||x|| = 1$, which we showed is equivalent to minimizing $||Sy|| \st ||y||=1$. Lemma 1 now gives us an answer to that in $y=[0,0,...1]$.
\\
\\
Since $y=V^Tx$, we can recover $x = Vy$. And since $y=[0,0,..., 1]^T$, $x$ is \textbf{the last column of the V matrix}.

""", scale=2
),
className="centered",
),
Br(),
Br(),
Br(),
)

results = ()


# Generate the HTML content
title = "Solving Homogeneous Linear Least Squares"
out = HTML(
    Head(Title(title), snippets.V1_headPreamble()),
    Body(
        Div(
            H2(B(title)),
            Br(),
            Br(),
            Br(),
            H3(B("Problem Setup")),
            problemSetup,
            Br(),
            successCriteria,
            Br(),
            whatDoYouMeanNotMeaningful,
            problemReframing,
            method,
            deriving,
            className="standardContent",
        )
    ),
)


# Write the generated HTML to a file
def writeHTML():
    with open(__file__.replace(".py", ".html"), "w") as f:
        f.write(out)


writeHTML()
