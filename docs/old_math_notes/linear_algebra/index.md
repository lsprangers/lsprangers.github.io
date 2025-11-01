---
title: Linear Algebra Notes
layout: default
---

## Linear Algebra
All of the old notes I have on Linear Algebra topics, plus [3Blue1Brown](https://www.3blue1brown.com/), and some [DL Books](https://www.deeplearningbook.org/contents/linear_algebra.html)

Combining this with the [Probability and Statistics](/docs/old_math_notes/probability_and_statistics/index.md) section is basically ML and Effects Testing

### Definitions
- **Scalar**: A single number, often representing a quantity in space
    - Often written in italics, e.g., $x$.
- **Vector**: An ordered array of numbers, which can represent a point in space, or direction in physics, where each element gives the coordinates along a different axis
    - Often written in bold, e.g., $\bold{v}$
    - Can identify each individual number by it's index - i.e. $\bold{x}_1$
    - A vector having $n$ elements would have $\bold{x} \in \mathbb{R}^n$
    - Can subset a vector
        - $\bold{x}_{1:n}$ for contiguous subset
        - $\bold{x}_{[1,4,n]}$ for a defined index set $S$ 
        - $\bold{x}_{-1}$ for all numbers except number at index 1
- **Matrix**: A 2-D array of numbers, which can also represent a linear transformation, or a system of linear equations
    - Often written in italic uppercase bold, e.g., $\textit{A}$
    - A matrix having $m$ rows and $n$ columns would have $\textit{A} \in \mathbb{R}^{m \times n}$
    - Can identify each individual element by its row and column indices - i.e. $\textit{A}_{ij}$
    - Can identify an entire row - i.e. $\textit{A}_{i:}$
    - Or an entire column - i.e. $\textit{A}_{:j}$
- **Tensors**: A generalization of scalars, vectors, and matrices to higher dimension. They can also be defined as an array with more than 2 axes. "An array of numbers arranged on a regular grid with a variable number of axes (dimensions) is known as a tensor"
    - Tensors are denoted by boldface type, e.g., $\bold{T}$
    - To access element of $\bold{T}$, at coordinates $(i, j, k)$, you would write $\bold{T}_{ijk}$

### Operations

- **Addition**: Matrices and vectors can be added together element-wise
    - $\textit{A}_{i, j} + \textit{B}_{i, j} = \textit{C}_{i, j}$
- **Scalar Multiplication**: A matrix or vector can be multiplied by a scalar (a single number) by multiplying each element by that scalar
    - $\textit{D} = a \cdot \textit{B} + c = k$ where $\textit{D}_{i, j} = a \cdot \textit{B}_{i, j} + c$
- **Matrix Multiplication**: Two matrices can be multiplied together if the number of columns in the first matrix is equal to the number of rows in the second matrix. The resulting matrix will have the number of rows of the first matrix and the number of columns of the second matrix
    - $\textit{A}_{i, j} \cdot \textit{B}_{j, k} = \textit{C}_{i, k}$
    - $\textit{C}_{i, k} = \sum_{j} \textit{A}_{i, j} \cdot \textit{B}_{j, k}$
        - $\textit{A}$ must have same number of columns as $\textit{B}$ has rows
    - This **is not** commutative
- **Element-wise Multiplication (Hadamard Product)**: Two matrices or vectors of the same dimensions can be multiplied together element-wise
    - $\textit{C}_{i, j} = \textit{A}_{i, j} \odot \textit{B}_{i, j}$
- **Transposition**: The transpose of a matrix is obtained by flipping it over its diagonal, turning rows into columns and vice versa
    - $\textit{A}^T_{i, j} = \textit{A}_{j, i}$
    - ![Transpose](/img/transpose.png)
- **Dot Product**: The dot product of two vectors is the sum of the products of their corresponding elements
    - $\bold{a} \cdot \bold{b} = \sum_{i} \bold{a}_i \cdot \bold{b}_i$
    - This **is** commutative
- **Identity**: The identity matrix $\textit{I}$ is a square matrix with ones on the diagonal and zeros elsewhere
    - $\textit{I}_{i, j} = \begin{cases} 1 & \text{if } i = j \\ 0 & \text{if } i \neq j \end{cases}$
    - Identity matrix has the property that when multiplied by any compatible matrix $\textit{A}$, it returns $\textit{A}$
    - $\textit{A} \cdot \textit{I} = \textit{A}$
- **Inverse**: The inverse of a square matrix $\textit{A}$ is another matrix $\textit{A}^{-1}$ such that when multiplied together, they yield the identity matrix
    - $\textit{A}^{-1} \cdot \textit{A} = \textit{I}$
    - Not all matrices have inverses; a matrix must be square and have a non-zero determinant to have an inverse

### Useful Properties
- From above, a matrix being square with a non-zero determinant means it has an inverse
    - This is crucial for solving systems of linear equations, as having an inverse allows us to find unique solutions
        - $\textit{A} \cdot \bold{x} = \bold{b}$
        - Therefore, $\bold{x} = \textit{A}^{-1} \cdot \bold{b}$
        - This solution is unique *if and only if $det(A) \neq 0$*
            - When $\textit{A}^{-1}$ exists, several algorithms are able to find it in closed form, meaning you can analytically solve for this
            - However, this isn't typically used in practice in most software libraries, as it's often computationally expensive, can only be represented with limited precision, and is less stable than other methods
                - Instead, methods like LU decomposition or iterative solvers are often preferred

### Linear Systems and Vector Coordinates
Thinking of Vectors simply as points in space is usually the best way of visualizing them. Each vector can be represented as a point in an n-dimensional space, where $n$ is the number of dimensions or components in the vector

The point $[1, 2, 3]$ is a point in 3D space 1 unit right, 2 units up, and 3 units forward from the origin

In linear algebra the most common way of describing these are using ***basis vectors***:
- $\hat{i}$ is the unit vector in the direction of the x-axis $[1, 0, 0]$
- $\hat{j}$ is the unit vector in the direction of the y-axis $[0, 1, 0]$
- $\hat{k}$ is the unit vector in the direction of the z-axis $[0, 0, 1]$

Therefore, in the example above, the vector $[1, 2, 3]$ can be expressed as a linear combination of the basis vectors:
$$[1, 2, 3] = 1 \cdot \hat{i} + 2 \cdot \hat{j} + 3 \cdot \hat{k}$$

Vectors are just scalars that you use to multiply against these common basis vectors - so a good question is how many points in 2D space by using the basis vectors $\hat{i} \text{and} \hat{j}$? The answer is everything!

![VectorScalingDemo](/img/VectorScalingDemo.gif)

You can even use different basis vectors, and there's an inherent relationship between them. For example, in 2D space, you can use $\hat{i}$ and $\hat{j}$ as our basis vectors, but you could also use any other pair of linearly independent vectors - the linear transformation to take either of those to $[1, 2]$ would still hold

If both of our basis vectors end up pointing in the "same direction", they're said to be ***linearly dependent***. This would be something like if you had $\hat{i} [1, 0] \text{and} [2, 0]$ as our basis vectors, then the set of all possible vectors you could reach would only be on the x-axis. At this point you can no longer reach other points "upwards" or "downwards" in the 2D plane - our space is effectively reduced to a line. This is a key concept in linear algebra - the set of points you can reach using linear transformations from our basis vectors is known as the **span** of those vectors.

Using $\hat{i}$ \text{and} $\hat{j}$, you can reach any point in the 2D plane, as they are linearly independent. However, if you were to use $\hat{i} [1, 0] \text{and} [2, 0]$ as our basis vectors, they would be linearly dependent, and you could only reach points along the line defined by $\hat{i}$. In the former scenario our span is $\mathbb{R}^2$, while in the latter it is just $\mathbb{R}$

So a span is a set of points, specifically the set of all possible linear combinations of a given set of vectors, but vectors can be thought of as individual points - it's a helpful nuance 

The same idea holds in all dimensions - if you have a 3D space, and our basis vectors relate to the 2D basis vectors, our span would be a 2D plane sitting in the 3D space that you can create from those basis vectors. If it's $\hat{i}$ \text{and} $\hat{j}$ it will be the 2D plane on the origin 

#### Linear Transformations
Linear Algebra helps us to manipulate matrices, and one of the most important topics / use cases of this are systems of linear transformations

A linear transformation, for example, would take the 2D grid and perform any number of linear transformations on it - shrink, expand, twist, turn, etc and all of these are described by matrix transformations on top of our basis vectors

![Linear Transformation Over Basis Vector](/img/linear_transformation_basis_vectors.png)

This is useful because it allows us to understand how different transformations affect our vector space. Having a matrix $\textit{A}$ and a vector $x$, you can express the linear transformation as $\textit{A}x = b$, where $b$ is the output vector. Alongside that, you can also consider the inverse transformation, which would allow us to map the output vector $b$ back to the input vector $x$. In the grand scheme of things in the real world, the ***matrix represents linear combinations of weights*** and our output vector is our ***weighted sum of inputs / output***. In graphics, ML, analytics, etc you use the matrix as a weight representation constantly, and it's just a way to transform our input vectors

Tracking the transformation of the basis vectors also allows us to track the output of any other vector in our system - if our basis is $\hat{i}$ \text{and} $\hat{j}$, and a random starting vector is $[2, 3]$, you can express it in terms of our basis as $2\hat{i} + 3\hat{j}$. Therefore, if you apply the transformation $\textit{A}$ to this metric space, you just have to track the effects on $\hat{i}$ \text{and} $\hat{j}$, and then you can apply those effects to our starting vector

At the end of the day ***matrices are just transformations of space, that's IT!***

#### Why Solve Linear Systems
Having a matrix $\textit{A}$ and a vector $x$, you can express the linear transformation as $\textit{A}x = b$, where $b$ is the output vector

![Linear Systems of Equations](/img/linear_system.png)

If $\textit{A}$ is a transformation, and $\bold{x}$ is a vector you want to find, such that when you transform $\bold{x}$ you get to our desired output $\bold{v}$

So knowing this, if you have our output $\bold{v}$ and a Transformation $\textit{A}$, you could hypothetically find the Inverse $\textit{A}^{-1}$, which should give us our desired vector $\bold{x}$

***This means you can analytically solve for this***, however this solution is unique *if and only if $det(A) = 0$*, because if $det(A) = 0$ there are multiple solutions that can "squeeze" things down by a dimension. Another thought is "there's no inverse to map 1D to a unique 2D plane", you can't just "create" another dimension
- This solution is only unique because it means "if you first apply $\textit{A}$, and then apply $\textit{A}^{-1}$, you end up where you started"
- There still may be a solution though...a solution is unique iff it's $det != 0$, but $det(A) = 0$ does not imply there is no solution

For a system of linear equations, and an output $\bold{b}$, there's either:
- No solution
- One exact solution
    - There's one solution of $\textit{A}\bold{x} = \bold{b}$ if and only if $\textit{A}$ is invertible, which corresponds to:
        - $\det(A) \neq 0$
            - If $\textit{A}$ is a square matrix and $\det(A) \neq 0$ then it's columns span all of $\mathbb{R}^n$
            - If $\det(A) = 0$ then it's columns do not span all of $\mathbb{R}^n$ and there's none, or infinite, solutions
        - $\text{rank}(A) = n$ (full rank)
        - Columns of $A$ are linearly independent
        - Columns of $A$ span all of $\mathbb{R}^n$
    - All of the above imply each other
- Infinite solutions
    - you can't have more than one but less than infinite - proof:
        - Idea: If you have one solution, you can always add a multiple of the null space to it to get another solution, thus creating infinitely many solutions.
        - If both $\bold{x}$ and $\bold{y}$ are solutions, then $\bold{z} = \alpha \bold{x} + (1 - \alpha) \bold{y}$ is also a solution for ***any*** scalar $\alpha$
        - The above solution has infinitely many solutions because you can choose any value for $\alpha$

These systems of equations can also be viewed as ***Linear Combinations*** of the input vectors - formally this can be viewed as 
- $\{\bold{v}^{(1)}, ..., \bold{v}^{(n)}\} \in \mathbb{R}^n$ 
- Such that when multiplied by corresponding scalars $c_{1,n}$ 
- you get to $c_1 \bold{x_1} + c_2 \bold{x_2} + ... + c_n \bold{x_n} = \bold{b}$, where the $c_i$ are scalars

From the above, if you add them together ${\sum \over {i}} {c_i \bold{v}^{(i)}} = \bold{b}$, you can see that the output point $\bold{b}$ is a linear combination of the input vectors

*Therefore, a square matrix with a determinant allows us to solve a system of equations, to define a linear combination, and ultimately to find transformations that bring us from one point (usually the origin) to another fixed point via dimensional traversals*

#### Span
The span of a set of vectors is the set of all points obtainable by linear combinations of the original vectors
- They define all of the points dimensionally you can "get to" from our basis vectors
- The particular span of all of the columns of $\textit{A}$ is known as the **Column Space** or ***range*** of $\textit{A}$
- The ***basis vectors*** of $\textit{A}$ are the vectors that span the column space of $\textit{A}$
    - In 3D our basis vectors are $\{\bold{e}_1, \bold{e}_2, \bold{e}_3\}$ where $\bold{e}_i$ are the standard basis vectors representing $(1, 0, 0)$, $(0, 1, 0)$, and $(0, 0, 1)$ respectively
    - Basis vectors are just the "unit vectors" which you can multiply, combine, and use to get to points in 3D space - any point in 3D cube can be reached uniquely by altering these 3 unit vectors
    - If one of these was missing, say $(0, 0, 1)$, our Z axis, then the Column Space of that set is 2D and we'd never be able to go up or down the Z axis - we'd be stuck in 2D!
        - This point comes up repeatedly as "column space must be equal to $\mathbb{R}^m$", but when stated this way it's less intuitive

Unique solutions also require ***Linear Independence***, which means that no vector (column) in the basis vectors can be written as a linear combination of the others - if that were the case then one of our vectors could be removed without changing the span, which would contradict the definition of a basis
- For the linear system $A\bold{x} = \bold{b}$, having a unique solution (for a given $\bold{b}$) requires that the columns of $\textit{A}$ be linearly independent (i.e. full column rank)
    - In the square case $n \times n$, linear independence of the columns is equivalent to $\det(A) \neq 0$, which makes $\textit{A}$ invertible and guarantees a unique solution for every $\bold{b}$
    - In a tall rectangular case $m \gt n$, if the $n$ columns are independent and $\bold{b}$ lies in the column space, then the solution is unique. If $\bold{b}$ is outside the column space, there’s no solution

So how does this help us?
- Determining whether $\textit{A}\bold{x} = \bold{b}$ has a solution involves checking if $\bold{b}$ is in the span of the columns of $\textit{A}$
    - In order for $\textit{A}\bold{x} = \bold{b}$ to have a solution for ***all values of $\bold{b} \in \mathbb{R}^m$***, it must be the case that the column space of $\textit{A}$ is equal to $\mathbb{R}^m$ (the space of all possible output vectors)
        - Intuitively, this just means you need enough "directions" in our column space to reach any point in $\mathbb{R}^m$
        - If one of the "directions" or dimensions in $m$ is unreachable because one of our basis vectors is missing or linearly dependent, then you can never reach that dimension



#### Rank
- When the output of a transformation is a line, you say the Rank is 1
- If all output vectors land in 2D plane, the Rank is 2
- Therefore, ***Rank can be thought of as the number of dimensions in the output of the Transformation***
- $2 \times 2$ matrix with $Rank = 2$ means nothing has collapsed, but $3 \times 3$ matrix with the same Rank means something / some group of vectors or points has collapsed

### Determinant
Determinant is based on Transformations, and can therefore be extended to matrices

Determinants help us to quantify how much Transformations scale unit areas of a metric space - meaning in a 2 dimensional space with $i$ and $j$ unit vectors, meaning a 1x1 = 1 area, if our Transformation $T$ turns that into a 2x3 area then our determinant would be 6

Determinants for 3 dimensional spaces would correspond to Volume of a cube, whereas 2 dimensional would be on flat area

Determinants also have signs for when there is an orientation flip, and a determinant of 0 would correspond to reduction of dimensions - meaning 2d down to 1d or single point

Given a $2 \times 2$ matrix:
$$
A = \begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
$$

The determinant of $A$ is:
$$
\det(A) = ad - bc
$$


#### Commutative Product
The commutativity makes sense because it would just be 2 transformations chained onto each other...most linear transformations are just linear chains of transformations, so having the determinant also be one isn't surprising

$det(A) \times det(B) = det(AB)$
c & d
\end{bmatrix}
$$

The determinant of $A$ is:
$$
\det(A) = ad - bc
$$


#### Commutative Product
The commutativity makes sense because it would just be 2 transformations chained onto each other...most linear transformations are just linear chains of transformations, so having the determinant also be one isn't surprising

$det(A) \times det(B) = det(AB)$