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
    - **Norm**: A measure of the length (magnitude) of a vector. Intuitively they measure how far a vector is from the origin (or point we are measuring from)
        - Norms map vectors to non-negative numbers
        - Commonly used norms:
            - $\text{L}^1 \text{ Norm}:$ Norm (Manhattan Norm): $\|\bold{x}\|_1 = \sum_{i} |\bold{x}_i|$
            - $\text{L}^2 \text{ Norm}:$ Norm (Euclidean Norm): $\|\bold{x}\|_2 = \sqrt{\sum_{i} \bold{x}_i^2}$
                - Extremely common in ML - it's mostly noted as $\|\bold{x}\|$ without the subscript
                - Squared Norm can be calculated easily via the Dot Product: $\|\bold{x}\|_2 = \sqrt{\bold{x} \cdot \bold{x}}$
            - Formally, $\text{L}^p \text{ Norm}: \|\bold{x}\|_p = \left( \sum_{i} |\bold{x}_i|^p \right)^{1/p}$
            - Commonly used to measure distances between points in space, or to regularize models in machine learning to prevent overfitting
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
- **Inverse**: The inverse of a square matrix $\textit{A}$ is another matrix $\textit{A}^{-1}$ such that when multiplied together, they yield the identity matrix
    - $\textit{A}^{-1} \cdot \textit{A} = \textit{I}$
    - Not all matrices have inverses; a matrix must be square and have a non-zero determinant to have an inverse
- **Determinant**: The determinant is a scalar value that can be computed from the elements of a square matrix. It provides some useful information about a matrix - mostly around:
    - How much it "squashes" or "expands" space when the matrix is viewed as a linear transformation
    - Whether the matrix is invertible (i.e., has an inverse)
    - And formally, it's the product of all of the eigenvalues of a matrix (when it's square)
- **Eigenvector**: An eigenvector of a square matrix $\textit{A}$ is a non-zero vector $\bold{v}$ such that when $\textit{A}$ is applied to $\bold{v}$, the result is a scalar multiple of $\bold{v}$
    - It's a direction in which the transformation represented by the matrix acts by stretching or compressing, rather than rotating
    - It simply is a "stationary" vector for the linear transformation

### Useful Properties
- From above, a matrix being square with a non-zero determinant means it has an inverse
    - This is crucial for solving systems of linear equations, as having an inverse allows us to find unique solutions
        - $\textit{A} \cdot \bold{x} = \bold{b}$
        - Therefore, $\bold{x} = \textit{A}^{-1} \cdot \bold{b}$
        - This solution is unique *if and only if $det(A) \neq 0$*
            - When $\textit{A}^{-1}$ exists, several algorithms are able to find it in closed form, meaning you can analytically solve for this
            - However, this isn't typically used in practice in most software libraries, as it's often computationally expensive, can only be represented with limited precision, and is less stable than other methods
                - Instead, methods like LU decomposition or iterative solvers are often preferred

## Linear Systems and Vector Coordinates
Thinking of Vectors simply as points in space is usually the best way of visualizing them. Each vector can be represented as a point in an n-dimensional space, where $n$ is the number of dimensions or components in the vector

The point $[1, 2, 3]$ is a point in 3D space 1 unit right, 2 units up, and 3 units forward from the origin

In linear algebra the most common way of describing these are using ***basis vectors***:
- $\hat{i}$ is the unit vector in the direction of the x-axis $[1, 0, 0]$
- $\hat{j}$ is the unit vector in the direction of the y-axis $[0, 1, 0]$
- $\hat{k}$ is the unit vector in the direction of the z-axis $[0, 0, 1]$

Therefore, in the example above, the vector $[1, 2, 3]$ can be expressed as a linear combination of the basis vectors:
$$[1, 2, 3] = 1 \cdot \hat{i} + 2 \cdot \hat{j} + 3 \cdot \hat{k}$$

Vectors are just scalars that you use to multiply against these common basis vectors - so a good question is: how many points in 2D space can you reach using the basis vectors $\hat{i}$ and $\hat{j}$? The answer is: every point in $\mathbb{R}^2$.

![VectorScalingDemo](/img/VectorScalingDemo.gif)

You can even use different basis vectors, and there's an inherent relationship between them. For example, in 2D space, you can use $\hat{i}$ and $\hat{j}$ as our basis vectors, but you could also use any other pair of linearly independent vectors - the linear transformation to take either of those to $[1, 2]$ would still hold

If both of our basis vectors end up pointing in the "same direction", they're said to be ***linearly dependent***. This would be something like if you had $\hat{i} [1, 0]$ and $[2, 0]$ as our basis vectors, then the set of all possible vectors you could reach would only be on the x-axis. At this point you can no longer reach other points "upwards" or "downwards" in the 2D plane - our space is effectively reduced to a line. This is a key concept in linear algebra: the set of points you can reach using linear combinations of basis vectors is known as the **span** of those vectors.

Using $\hat{i}$ and $\hat{j}$, you can reach any point in the 2D plane, as they are linearly independent. However, if you were to use $\hat{i} [1, 0]$ and $[2, 0]$ as our basis vectors, they would be linearly dependent, and you could only reach points along the line defined by $\hat{i}$. In the former scenario our span is $\mathbb{R}^2$, while in the latter it is just $\mathbb{R}$.

So a span is a set of points, specifically the set of all possible linear combinations of a given set of vectors, but vectors can be thought of as individual points - it's a helpful nuance 

The same idea holds in all dimensions: if you have a 3D space and two independent basis vectors, your span is a 2D plane sitting in the 3D space. If the basis is $\hat{i}$ and $\hat{j}$ it will be the standard $xy$-plane through the origin.

### Linear Transformations
Linear Algebra helps us to manipulate matrices, and one of the most important topics / use cases of this are systems of linear transformations

Having a matrix $\textit{A}$ and a vector $x$, you can express the linear transformation as $\textit{A}x = b$, where $b$ is the output vector

![Linear Systems of Equations](/img/linear_system.png)

A linear transformation, for example, would take the 2D grid and perform any number of linear transformations on it - shrink, expand, twist, turn, etc and all of these are described by matrix transformations on top of our basis vectors

If $\textit{A}$ is a transformation, and $\bold{x}$ is a vector you want to find, such that when you transform $\bold{x}$ you get to our desired output $\bold{v}$

So knowing this, if you have our output $\bold{v}$ and a Transformation $\textit{A}$, you could hypothetically find the Inverse $\textit{A}^{-1}$, which should give us our desired vector $\bold{x}$

![Linear Transformation Over Basis Vector](/img/linear_transformation_basis_vectors.png)

This is useful because it allows us to understand how different transformations affect our vector space. Having a matrix $\textit{A}$ and a vector $x$, you can express the linear transformation as $\textit{A}x = b$, where $b$ is the output vector. Alongside that, you can also consider the inverse transformation, which would allow us to map the output vector $b$ back to the input vector $x$. In the grand scheme of things in the real world, the ***matrix represents linear combinations of weights*** and our output vector is our ***weighted sum of inputs / output***. In graphics, ML, analytics, etc you use the matrix as a weight representation constantly, and it's just a way to transform our input vectors

Tracking the transformation of the basis vectors also allows us to track the output of any other vector in our system. If our basis is $\hat{i}$ and $\hat{j}$, and a random starting vector is $[2, 3]$, you can express it in terms of our basis as $2\hat{i} + 3\hat{j}$. Therefore, if you apply the transformation $\textit{A}$ to this space, you just have to track the effects on $\hat{i}$ and $\hat{j}$, and then apply those effects to the starting vector.

There's a way to ultimately tell what a matrix transformation is doing to space by looking at the **determinant** of the matrix, which helps to understand how much area or volume is being scaled by the transformation. Formally the determinant calculation is a bit more complex, but the intuition is that it gives you a scalar value that represents how much the transformation scales areas (in 2D) or volumes (in 3D). A determinant of 1 means the area/volume is preserved, greater than 1 means it's expanded, and less than 1 means it's contracted. A determinant of 0 indicates that the transformation collapses the space into a lower dimension (e.g., a plane to a line). Having a non-zero determinant is crucial for ensuring that the transformation is invertible, meaning you can reverse the transformation and recover the original vectors (because no information is lost)

At the end of the day ***matrices are just transformations of space, that's IT!***. Formally, a Linear Combination is defined as:
- $\{\bold{v}^{(1)}, ..., \bold{v}^{(n)}\} \in \mathbb{R}^n$ 
- Such that when multiplied by corresponding scalars $c_{1,n}$ 
- you get to $c_1 \bold{x_1} + c_2 \bold{x_2} + ... + c_n \bold{x_n} = \bold{b}$, where the $c_i$ are scalars

From the above, if you add them together ${\sum \over {i}} {c_i \bold{v}^{(i)}} = \bold{b}$, you can see that the output point $\bold{b}$ is a linear combination of the input vectors

*Therefore, a square matrix with a determinant allows us to solve a system of equations, to define a linear combination, and ultimately to find transformations that bring us from one point (usually the origin) to another fixed point via dimensional traversals*

### Span
The span of a set of vectors is the ***set*** of all points obtainable by linear combinations of the original vectors
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


### Rank
The Rank of a matrix is a number, it's the dimension of the column space of the matrix - meaning how many dimensions does the output of the transformation span
- If the output of a transformation is a single point, you say the Rank is 0
- When the output of a transformation is a line, you say the Rank is 1
- If all output vectors land in 2D plane, the Rank is 2
- Therefore, ***Rank can be thought of as the number of dimensions in the output of the Transformation***
- $2 \times 2$ matrix with $\text{Rank} = 2$ means nothing has collapsed, but $3 \times 3$ matrix with the same Rank means something / some group of vectors or points has collapsed

### Determinant
Determinant is based on Transformations, and can therefore be extended to matrices

Determinants help us to quantify how much Transformations scale unit areas of a metric space - meaning in a 2 dimensional space with $i$ and $j$ unit vectors, meaning a 1x1 = 1 area, if our Transformation $T$ turns that into a 2x3 area then our determinant would be 6

Determinants for 3 dimensional spaces would correspond to Volume of a cube, whereas 2 dimensional would be on flat area

Determinants also have signs for when there is an orientation flip, and a determinant of 0 would correspond to reduction of dimensions - meaning 2d down to 1d or single point

Given a $2 \times 2$ matrix:
$$
A = \begin{bmatrix}
a \& b \\
c \& d
\end{bmatrix}
$$

The determinant of $A$ is:
$$
\det(A) = ad - bc
$$

They are similar to integrals in that they both measure a form of "volume" - in the case of determinants, it's the volume of the parallelepiped formed by the column vectors of the matrix. Ultimately they just allow us to tell how much the transformation represented by the matrix "stretches" or "compresses" space.

### Solutions to Linear Systems
Now that there's definitions in place, discussing solutions to Linear Systems makes more sense

For the examples below assume there's an input vector $\bold{x}$, a transformation $\textit{A}$, and an output vector $\bold{b}$ as usual

Intuitively, having a solution means our metric space should have both $\bold{x}$ and $\bold{b}$ - if they're both in the metric space there must be a way to connect them through the transformation $\textit{A}$

The columns of $\textit{A}$ span a certain subspace of $\mathbb{R}^m$ (the column space), and they can be viewed as the images of the basis vectors that underlie the domain of the linear mapping (transformation). Therefore, only vectors inside of that reachable subscape can be "hit"

Determining whether or not $\textit{A}\bold{x} = \bold{b}$ has a solution involves checking if $\bold{b}$ is in the span of the columns of $\textit{A}$ - this is intuitive because it means that $\bold{b}$ can be expressed as a linear combination of the columns of $\textit{A}$, which is necessary for there to exist some $\bold{x}$ such that $\textit{A}\bold{x} = \bold{b}$, if the $\textit{A}$ was "living in another dimension" than $\bold{b}$ then there would be no way to connect to it from $\bold{x}$

Really hitting on the points above because they're all interconnected

Taking $\textit{A}\bold{x} = \bold{b}$ for all values of $\bold{b} \in \mathbb{R}^m$, it must be the case that the column space of $\textit{A}$ is equal to $\mathbb{R}^m$ (the space of all possible output vectors). If any point in $\mathbb{R}^m$ is not in the column space of $\textit{A}$, then there is no way to reach it from $\bold{x}$, and it's also a potential $\bold{b}$ that we cannot reach - Intuitively, this just means you need enough "directions" in our column space to reach any point in $\mathbb{R}^m$. Immediately, this means that $\textit{A}$ must have at least $m$ columns to be able to span $\mathbb{R}^m$ - it could have more, and that would mean that the potential $\bold{x}$ vectors we use would need to "sqush" down to a lower dimensional $\bold{b}$ space. An example of this would be if we're working in 3D space, but our transformation only outputs 2D points - this would mean that our column space is a 2D plane in 3D space.

Another, clearer example, would be a $3 \times 2$ matrix - in this the target $\bold{b}$ is in $\mathbb{R}^3$, but the column space of $\textit{A}$ can only span a 2D plane in that 3D space. Therefore, the only $\bold{b}$ we can reach is one that lies in that 2D plane traced out by the column space of $\textit{A}$. Any $\bold{b}$ that lies outside of that plane is unreachable, and therefore there is no solution for those $\bold{b}$

Intuitively now, having more columns than rows (i.e., more variables than equations) means that the system is underdetermined, and there may be infinitely many solutions or no solution at all, depending on whether $\bold{b}$ lies in the column space of $\textit{A}$. It basically means there's "extra dimensions" in the input space that can be adjusted without affecting the output, leading to multiple possible $\bold{x}$ vectors that map to the same $\bold{b}$

Conversely, having fewer columns than rows (more equations than variables) means the system is overdetermined, which can lead to no solution or a unique solution if the equations are consistent and independent. This is similar to the $3 \times 2$ matrix example above, where the output space is larger than the input space, leading to potential unreachable outputs, so there are still some solutions we can find but there will most likely be unfindable ones

#### Invertibility Final Notes
Point 1: At the end of the day the column space of $\textit{A}$ must be equal to $\mathbb{R}^m$ for there to be a solution for every possible $\bold{b}$, and actually the condition is necessary ***and sufficient*** - meaning if the column space of $\textit{A}$ is equal to $\mathbb{R}^m$, then there is a solution for every possible $\bold{b}$, and if there is a solution for every possible $\bold{b}$, then the column space of $\textit{A}$ must be equal to $\mathbb{R}^m$

Point 2: For the matrix $\textit{A}$ to have an inverse, we additionally need to ensure that $\textit{A}\bold{x} = \bold{b}$ has *at most* one solution for each $\bold{b}$ in its column space. This requires that the columns of $\textit{A}$ has *at most* $m$ columns. Otherwise, there's more than one way to parameterize each solution, leading to infinitely many solutions for some $\bold{b}$

Points 1 and 2 together means the matrix $\textit{A}$ must be square ($m = n$) and have full rank ($\text{rank}(A) = n$) to ensure that $\textit{A}\bold{x} = \bold{b}$ has exactly one solution for every possible $\bold{b}$ in $\mathbb{R}^m$. This is equivalent to saying that $\textit{A}$ is ***invertible***, which allows us to uniquely map each input vector $\bold{x}$ to a distinct output vector $\bold{b}$, and vice versa

***If the matrix isn't square there's other ways to solve it, but it won't be done via matrix inversion analytically***

Altogether now:
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
    - All of the above imply each other, and intuitively mean that the transformation represented by $\textit{A}$ is ***bijective (one-to-one and onto)***, allowing us to uniquely map each input vector $\bold{x}$ to a distinct output vector $\bold{b}$, and vice versa
- Infinite solutions
    - You can't have more than one but less than infinite - The idea: If you have one solution, you can always add a multiple of the null space to it to get another solution, thus creating infinitely many solutions.
        - If both $\bold{x}$ and $\bold{y}$ are solutions, then $\bold{z} = \alpha \bold{x} + (1 - \alpha) \bold{y}$ is also a solution for ***any*** scalar $\alpha$
        - The above solution has infinitely many solutions because you can choose any value for $\alpha$

### Special Matrices
- **Diagonal Matrix**: A matrix where all off-diagonal elements are zero. It's written as $\text{diag} (\bold{v})$ where $\bold{v}$ is a vector holding the scalar entries that represent the diagonal. It is represented as:
    $$
    D = \begin{bmatrix}
        d_1 \& 0 \& \cdots \& 0 \\
        0 \& d_2 \& \cdots \& 0 \\
        \vdots \& \vdots \& \ddots \& \vdots \\
        0 \& 0 \& \cdots \& d_n
        \end{bmatrix}
    $$ 
    - These matrices are useful because multiplying them by a vector $\bold{x}$ simply scales each component of $\bold{x}$ by the corresponding diagonal entry which is computationally efficient
    - The inverse is also computationally efficient to compute, as long as none of the diagonal entries are zero - it's simply the reciprocal of each diagonal entry
- **Symmetric Matrix**: A square matrix that is equal to its transpose, i.e., $\textit{A} = \textit{A}^T$. This means that the elements are mirrored across the main diagonal:
    $$
    A = \begin{bmatrix}
        a_{11} \& a_{12} \& \cdots \& a_{1n} \\
        a_{12} \& a_{22} \& \cdots \& a_{2n} \\
        \vdots \& \vdots \& \ddots \& \vdots \\
        a_{1n} \& a_{2n} \& \cdots \& a_{nn}
        \end{bmatrix}
    $$
    - These often come about from functions of two arguments where the order of the arguments doesn't matter, such as distance metrics or covariance matrices
- **Orthogonal Matrix**: A square matrix $\textit{Q}$ whose columns (and rows) are orthonormal vectors. This means that $\textit{Q}^T \textit{Q} = \textit{Q} \textit{Q}^T = \textit{I}$, where $\textit{I}$ is the identity matrix
    - Orthogonal vectors have a dot product of zero, meaning they are perpendicular to each other in the vector space
    - Orthonormal vectors are orthogonal vectors that also have a norm (length) of 1
    - The inverse of an orthogonal matrix is simply its transpose: $\textit{Q}^{-1} = \textit{Q}^T$
    - Geometrically, orthogonal matrices represent rotations and reflections in space without scaling

### Eigenvalues, Eigenvectors, and Eigendecomposition
Eigenvalues and Eigenvectors are a weird subset of linear algebra that suck at first but are useful once understood

Mathematical objects are better understood by breaking them down into more fundamental components, and then studying those components and their similarities. Breaking down integers into prime factors, functions into Taylor series, and distributions into mean and variances is all examples of this

**Eigenvalues** and **Eigenvectors** are one such way of breaking down matrices (linear transformations) into more fundamental components

An **Eigenvector** of a square matrix $\textit{A}$ is a non-zero vector $\bold{v}$ such that multiplication with $\textit{A}$ alters only the values of $\bold{v}$

$\textit{A} \bold{v} = \lambda \bold{v}$ - in this case the $\lambda$ is the **Eigenvalue** corresponding to the Eigenvector $\bold{v}$

If $\bold{v}$ is an Eigenvector of $\textit{A}$, then so is any rescaled vector $\textit{s}\bold{v} \space \text{for} \space \textit{s} \in \mathbb{R}$, and moreover $\textit{s}$ has the same Eigenvalue $\lambda$

Why does that matter? Intuitively it means that $\bold{v}$ is a direction in space that is ***invariant*** under the transformation represented by $\textit{A}$ - it only gets scaled by $\lambda$, not rotated or otherwise changed. They are useful methods for describing "concrete" bricks that make up a matrix transformation

If a matrix $\textit{A}$ has $n$ linearly independent Eigenvectors $\{\bold{v}_1, \bold{v}_2, ..., \bold{v}_n\}$ with corresponding Eigenvalues $\{\lambda_1, \lambda_2, ..., \lambda_n\}$, then these Eigenvectors can form a basis for $\mathbb{R}^n$. We can concatenate these Eigenvectors into a matrix $\textit{V}$ where each column is an Eigenvector:
$$\textit{V} = [\bold{v}_1 \ \bold{v}_2 \ ... \ \bold{v}_n]$$
And we can create a diagonal matrix $\textit{D}$ with the corresponding Eigenvalues on the diagonal:
$$\textit{D} = \begin{bmatrix}
\lambda_1 & 0 & \cdots & 0 \\
0 & \lambda_2 & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & \lambda_n
\end{bmatrix}$$

**Eigendecomposition** is the process of decomposing a matrix into its eigenvalues and eigenvectors. For a square matrix $\textit{A}$, if it can be decomposed, it can be expressed as:
$$\textit{A} = \textit{V} \textit{D} \textit{V}^{-1}$$

Constructing matrices with specific eigenvalues and eigenvectors enables us to stretch space in desired directions. The flip side is also true - decomposing a matrix into it's eigenvalues and eigenvectors allows for analyzing properties of the matrix

Every real symmetric matrix can bedecomposed into an expression using only real-valued eigenvectors and eigenvalues - this is known as the **Spectral Theorem**. This is particularly useful in many applications, such as Principal Component Analysis (PCA) in machine learning, where we analyze the covariance matrix of data to find the directions of maximum variance (the principal components), which are given by the eigenvectors of the covariance matrix

The solution above may not be unique because any two eigenvectors could share the same eigenvalue, so any set of orthogonal vectors lying in their span are also eigenvectors with that eigenvalue - this is known as the **Eigenspace** corresponding to that eigenvalue. The dimension of the eigenspace is called the **geometric multiplicity** of the eigenvalue

## Singular Value Decomposition (SVD)
Singular Value Decomposition (SVD) is a technique in linear algebra that generalizes the concept of eigendecomposition to non-square matrices. SVD provides a way to factorize a matrix into **singular vectors** and **singular values**. Every real matrix $\textit{A}$ of size $m \times n$ can be decomposed using SVD, but not necessarily into eigenvalues and eigenvectors unless it is square and symmetric

In eigendecomposition: $$\textit{A} = \textit{V} \textit{D} \textit{V}^{-1}$$ (which looks very similar to SVD calc below)

If $\textit{A}$ is an $m \times n$ matrix, and is real or complex, then SVD decomposes $\textit{A}$ into three matrices: $\textit{U}$, $D$, and $\textit{V}^T$, such that:
$$\textit{A} = \textit{U} D \textit{V}^T$$
Where:
- $\textit{U}$ is an $m \times m$ orthogonal matrix whose columns are the left singular vectors of $\textit{A}$
- $D$ is an $m \times n$ diagonal matrix with non-negative real numbers on the diagonal, known as the singular values of $\textit{A}$
- $\textit{V}$ is an $n \times n$ orthogonal matrix whose columns are the right singular vectors of $\textit{A}$

The elements along $D$ are the singular values of $\textit{A}$, which are always non-negative and are typically arranged in descending order

The columns of $\textit{U}$ are the left singular vectors of $\textit{A}$, and the columns of $\textit{V}$ are the right singular vectors of $\textit{A}$. These singular vectors form orthonormal bases for the column space and row space of $\textit{A}$, respectively

Intuitively, SVD is used to show rotation / reflection with $\textit{U}$ and $\textit{V}$, and scaling with $D$. This helps show how much each independent direction is stretched or squeezed, and can quickly reveal rank and numeric stability in a linear transformation. Allows for a deeper understanding of the underlying structure of the data before doing anything crazy

Altogether, SVD provides a way to analyze and manipulate matrices, with applications in areas such as data compression, noise reduction, and latent semantic analysis. It's used to partially generalize matrix inversion to non-square matrices like in **Moore-Penrose pseudoinverse**

### Moore-Penrose Pseudoinverse
The Moore-Penrose pseudoinverse is a generalization of the matrix inverse for non-square matrices. It's useful when $\textit{A}$ has more rows than columns (i.e., $m > n$) or more columns than rows (i.e., $m < n$). It is denoted as $\textit{A}^+$ and can be computed using the SVD of $\textit{A}$:

1. Compute the SVD of $\textit{A}$: $$\textit{A} = \textit{U} D \textit{V}^T$$
2. Form the pseudoinverse by taking the reciprocal of the non-zero singular values in $D$ and transposing the matrices: $$\textit{A}^+ = \textit{V} D^+ \textit{U}^T$$

Where $D^+$ is obtained by taking the reciprocal of each non-zero singular value in $D$ and transposing the resulting matrix.

Why is this useful?
- It provides a least-squares solution to linear systems that may not have a unique solution
- It can be used for dimensionality reduction and data compression
- It is widely used in machine learning algorithms, particularly in linear regression and support vector machines

At the end of the day it's an extension of the concept of matrix inversion to a broader class of problems, making it a solution that's more realistic to use in day-to-day problems versus "perfectly square, nice" matrices

### Trace Operator
The trace operator is the sum of all the diagonal entries of a matrix - it's a pretty simple operation:
The trace is written inline as $\operatorname{tr}(\textit{A}) = \sum_i a_{ii}$.

It's used in a few different algorithms, but nothing much more to discuss

## Example: Principal Component Analysis (PCA)
Principal Component Analysis (PCA) is a dimensionality reduction technique that is widely used in machine learning and statistics. It transforms the data into a new coordinate system, where the greatest variances lie on the first coordinates (called principal components)

These principal components, ideally, allow us to combine our original inputs into less dimensions while retaining a majority of the variance - if we can go from 100 dimensions down to 2 or 3, we can visualize our data much more easily while still capturing the important patterns, and if we keep 95% of the variance in the 2 dimensions it helps ensure that we're not losing critical information about the data

Suppose there's a collection of $m$ points - $\{x^{(1)}, x^{(2)}, \ldots, x^{(m)}\}$, where each $x^{(i)}$ is a point in $\mathbb{R}^n$. The goal of PCA is to find a new set of axes (the principal components) that maximize the variance of the projected data. A typical example involves performing "lossy" compression over these points, which means reducing the number of dimensions while preserving as much information as possible. A way of doing this would be encoding these points in a lower-dimensional version - for each $x^{(i)}$ in $\mathbb{R}^n$ we find a corresponding vector $\bold{c}^{(i)}$ in $\mathbb{R}^l$, where $l < n$

Ideally there's an encoding function $f: \mathbb{R}^n \rightarrow \mathbb{R}^l$ such that $f(x^{(i)}) = \bold{c}^{(i)}$, and a corresponding decoding function $g: \mathbb{R}^l \rightarrow \mathbb{R}^n$ such that $g(f(x^{(i)})) \approx x^{(i)}$

PCA is actually defined by the choice of that decoding function $g$ - typically a linear function of the form $g(\bold{c}^{(i)}) = D \bold{c}^{(i)} + \bold{b}$, where $D \in \mathbb{R}^{n \times l}$ is a weight matrix and $\bold{b}$ is a bias vector

To make the above concept easier, $D$ is usually chosen so that it's columns are orthogonal to each other (to ensure that the principal components are uncorrelated), and to have unit norm (to ensure unique solutions)

### Achieving PCA
To turn the above concepts into a practical algorithm, PCA must:
- Figure out how to generate the optimal code point $\bold{c}^*$ for each input point $x^{(i)}$, and so ideally we can minimize the distance 
$$\text{argmin}_{\bold{c}} ||g(f(x^{(i)})) - x^{(i)}||^2$$

Which will simplify to 
$$(\bold{x} - g(\bold{c}))^T(\bold{x} - g(\bold{c}))$$

And after some more simplification and multiplying things out, it comes out to 
$$\text{argmin}_{\bold{c}} -2\bold{x}^T D \bold{c} + \bold{c}^T \bold{c} $$

Which is solved via vector calculus and simple optimization techniques like gradient descent - specifically, we can use the fact that the gradient of a quadratic function is linear, allowing us to iteratively update our code points until convergence

Everything ends up coming down to 
$$\bold{c} = \bold{D}^T \bold{x}$$

So the optimal function $\bold{c}$ is given by the projection of $\bold{x}$ onto the subspace spanned by the columns of $\bold{D}$

How to find this projection? It's known that minimizing the $L^2$ distance between inputs and reconstructions is ideal output 

If we stack all of our input vectors $\bold{x}^{(i)}$ into a matrix $\bold{X} \in \mathbb{R}^{n \times m}$, where each row is an input vector, we can express the optimization problem in terms of this matrix

Therefore, $\bold{X}_c$ is the matrix of all code points, where there are $m$ rows of $n$ features 

Create a covariance matrix $$\bold{C} = \frac{1}{m} \bold{X}_c^T \bold{X}_c$$

Eigendecomposition is then applied to this covariance matrix to find its eigenvalues and eigenvectors. The eigenvectors represent the directions of maximum variance in the data, while the eigenvalues indicate the amount of variance captured by each eigenvector - after this decomposition, we will have our optimal code points for $D$

The covariance matrix is sort of a "magical solution thing" that just solves most of the core optimization problem - so dissecting that is crucial for understanding PCA. The covariance matrix ties together span, rank, eigenvalues, eigenvectors, SVD, projections, and pretty much every other topic from above:
- *Intuition*: Multiplying the data matrix $\bold{X}_c$ by its transpose and scaling by $\frac{1}{m}$ gives us the covariance matrix $\bold{C}$ which intuitively just measures how much the different dimensions of the data vary together
    - How do eigenvectors intuitively relay this information? As you multiply a vector by itself $\bold{X}^T \bold{X}$, you're essentially measuring how much each dimension of the data aligns with every other dimension - the directions where this alignment is strongest correspond to the eigenvectors of the covariance matrix
        - The vectors underlying the covariance matrix that simply shrink or expand, but do not rotate
            - Let's say you have to project data onto a single 1D vector $\bold{v}$. The optimal projection can be found by minimizing the distance between the original data points and their projections onto $\bold{v}$
            - What do you choose as $\bold{v}$? The optimal choice is the vector corresponding that "captures" the most variance in your dataset
        - Covariance is a measure of how much two random variables change together 
            - $Cov(X, Y) = E[(X - E[X])(Y - E[Y])]$
        - The covariance matrix captures this relationship for all pairs of dimensions in the data, so it will compare each row to every other row
    - ***Comparing every data point to each other shows how they vary together, and so underlying eigenvectors of this covariance relationship represent the directions along which the data is most spread out***
        - The actual covariance linear transformation will form an ellipses 
        - This ellipses represents the distribution of data in feature space
        - In picture below, $v$ and $u$ are the principal components
        - ![2D Variance ellipses](/img/2d_variance_ellipses.png)
        - ![3D Variance ellipses](/img/3d_variance_ellipses.png)
- *Rank*: The rank of the covariance matrix is equal to the number of non-zero eigenvalues, which corresponds to the number of dimensions in the data that have variance
- *Span / Column Space*: The top $k$ principal components (eigenvectors) form an orthonormal basis for the $k$-dimensional subspace capturing the most variance
    - Their span is where the low-rank reconstruction lives
- *Eigenvalues and vectors*: Eigenvalues represent the amount of variance captured by each principal component (eigenvector), and the larger the value the more variance is captured by that component
- *Determinant*: The determinant of the covariance matrix provides a measure of the volume of the space spanned by the principal components, with a larger determinant indicating a more "spread out" distribution of the data
    - I.e. it's how much variance is "covered" by PCA
- 

So after a lot of algebra, the optimization problem is solved using eigendecomposition - specifically, we look for the eigenvectors of the covariance matrix of the data, which are the directions of maximum variance. The principal components are then given by the top $k$ eigenvectors, where $k$ is the desired dimensionality of the reduced space

