window.GLOSSARY = {
  "vector": {
    "name": "Vector",
    "short": "An ordered list of numbers of fixed length, read as a point or an arrow in a space with that many dimensions. An activation is a vector.",
    "def": "An ordered list of numbers of fixed length, read as a point or an arrow in a space with that many dimensions. An activation is a vector."
  },
  "activation": {
    "name": "Activation",
    "short": "The vector a model component outputs for one token at one layer; here a row of the residual stream after block 6 of GPT-2 small, length 768.",
    "def": "The vector a model component outputs for one token at one layer; here a row of the residual stream after block 6 of GPT-2 small, length 768."
  },
  "residual-stream": {
    "name": "Residual stream",
    "short": "The running vector each transformer layer reads from and adds to; the sum of the embedding and every earlier layer output.",
    "def": "The running vector each transformer layer reads from and adds to; the sum of the embedding and every earlier layer output."
  },
  "scalar": {
    "name": "Scalar",
    "short": "A single number, as opposed to a vector or matrix.",
    "def": "A single number, as opposed to a vector or matrix."
  },
  "linear-combination": {
    "name": "Linear combination",
    "short": "A sum of vectors each multiplied by a scalar, such as 2u − 3v.",
    "def": "A sum of vectors each multiplied by a scalar, such as 2u − 3v."
  },
  "dot-product": {
    "name": "Dot product",
    "short": "The sum of the products of matching coordinates of two vectors; a scalar that grows with alignment and with length.",
    "def": "The sum of the products of matching coordinates of two vectors; a scalar that grows with alignment and with length."
  },
  "norm": {
    "name": "Norm",
    "short": "The length of a vector: the square root of its dot product with itself.",
    "def": "The length of a vector: the square root of its dot product with itself."
  },
  "unit-vector": {
    "name": "Unit vector",
    "short": "A vector of norm 1; any nonzero vector divided by its norm.",
    "def": "A vector of norm 1; any nonzero vector divided by its norm."
  },
  "cosine-similarity": {
    "name": "Cosine similarity",
    "short": "The dot product of two vectors divided by the product of their norms; the cosine of the angle between them, between −1 and 1.",
    "def": "The dot product of two vectors divided by the product of their norms; the cosine of the angle between them, between −1 and 1."
  },
  "direction": {
    "name": "Direction",
    "short": "A unit vector, or any nonzero vector read only for its orientation; a feature direction is a candidate axis along which activations are measured.",
    "def": "A unit vector, or any nonzero vector read only for its orientation; a feature direction is a candidate axis along which activations are measured."
  },
  "projection": {
    "name": "Projection",
    "short": "The component of a vector along a direction; its coefficient is the dot product with the unit direction, a scalar per token.",
    "def": "The component of a vector along a direction; its coefficient is the dot product with the unit direction, a scalar per token."
  },
  "residual": {
    "name": "Residual",
    "short": "What is left of a vector after its projection is subtracted; orthogonal to the direction.",
    "def": "What is left of a vector after its projection is subtracted; orthogonal to the direction."
  },
  "orthogonal": {
    "name": "Orthogonal",
    "short": "Two vectors with dot product zero; at right angles.",
    "def": "Two vectors with dot product zero; at right angles."
  },
  "orthonormal": {
    "name": "Orthonormal",
    "short": "A set of unit vectors that are pairwise orthogonal.",
    "def": "A set of unit vectors that are pairwise orthogonal."
  },
  "matrix": {
    "name": "Matrix",
    "short": "A rectangular grid of numbers with a shape (rows, columns); read as a linear map, a batch of row vectors, or a table.",
    "def": "A rectangular grid of numbers with a shape (rows, columns); read as a linear map, a batch of row vectors, or a table."
  },
  "linear-map": {
    "name": "Linear map",
    "short": "A function that respects addition and scaling: f(u + v) = f(u) + f(v) and f(cu) = c f(u). Every matrix defines one and every linear map between coordinate spaces is a matrix.",
    "def": "A function that respects addition and scaling: f(u + v) = f(u) + f(v) and f(cu) = c f(u). Every matrix defines one and every linear map between coordinate spaces is a matrix."
  },
  "shape": {
    "name": "Shape",
    "short": "The tuple of array dimensions, such as (302, 768); the type signature of a tensor.",
    "def": "The tuple of array dimensions, such as (302, 768); the type signature of a tensor."
  },
  "matrix-multiplication": {
    "name": "Matrix multiplication",
    "short": "Combining an (n, k) and a (k, m) matrix into an (n, m) matrix whose entries are dot products of rows with columns; composition of linear maps.",
    "def": "Combining an (n, k) and a (k, m) matrix into an (n, m) matrix whose entries are dot products of rows with columns; composition of linear maps."
  },
  "transpose": {
    "name": "Transpose",
    "short": "The matrix with rows and columns swapped, written Aᵀ.",
    "def": "The matrix with rows and columns swapped, written Aᵀ."
  },
  "einsum": {
    "name": "einsum",
    "short": "A notation naming each axis by a letter, so that repeated letters are summed over; makes the shape of a product explicit.",
    "def": "A notation naming each axis by a letter, so that repeated letters are summed over; makes the shape of a product explicit."
  },
  "basis": {
    "name": "Basis",
    "short": "A set of vectors such that every vector in the space is exactly one linear combination of them; coordinates are the coefficients.",
    "def": "A set of vectors such that every vector in the space is exactly one linear combination of them; coordinates are the coefficients."
  },
  "neuron-basis": {
    "name": "Neuron basis",
    "short": "The standard basis in which coordinate i is the i-th entry of the activation; one basis among many, with no special status in the residual stream.",
    "def": "The standard basis in which coordinate i is the i-th entry of the activation; one basis among many, with no special status in the residual stream."
  },
  "change-of-basis": {
    "name": "Change of basis",
    "short": "Rewriting the same vector in the coordinates of a different basis; for an orthonormal basis the new coordinates are dot products.",
    "def": "Rewriting the same vector in the coordinates of a different basis; for an orthonormal basis the new coordinates are dot products."
  },
  "span": {
    "name": "Span",
    "short": "All linear combinations of a set of vectors; a line, plane, or higher flat through the origin.",
    "def": "All linear combinations of a set of vectors; a line, plane, or higher flat through the origin."
  },
  "linear-independence": {
    "name": "Linear independence",
    "short": "No vector in the set is a linear combination of the others; equivalently the only combination giving zero has all-zero coefficients.",
    "def": "No vector in the set is a linear combination of the others; equivalently the only combination giving zero has all-zero coefficients."
  },
  "rank": {
    "name": "Rank",
    "short": "The number of linearly independent columns (equivalently rows) of a matrix; the dimension of the space it maps onto.",
    "def": "The number of linearly independent columns (equivalently rows) of a matrix; the dimension of the space it maps onto."
  },
  "subspace": {
    "name": "Subspace",
    "short": "A flat through the origin closed under addition and scaling; the span of some vectors.",
    "def": "A flat through the origin closed under addition and scaling; the span of some vectors."
  },
  "superposition": {
    "name": "Superposition",
    "short": "A representation holding more features than it has dimensions, with feature directions that are not all orthogonal; defined in Toy Models of Superposition.",
    "def": "A representation holding more features than it has dimensions, with feature directions that are not all orthogonal; defined in Toy Models of Superposition."
  },
  "gram-schmidt": {
    "name": "Gram–Schmidt",
    "short": "A procedure that turns a list of vectors into an orthonormal list with the same span, by subtracting projections in order.",
    "def": "A procedure that turns a list of vectors into an orthonormal list with the same span, by subtracting projections in order."
  },
  "least-squares": {
    "name": "Least squares",
    "short": "Choosing coefficients to minimise the sum of squared differences between predictions and targets.",
    "def": "Choosing coefficients to minimise the sum of squared differences between predictions and targets."
  },
  "normal-equations": {
    "name": "Normal equations",
    "short": "XᵀX w = Xᵀy: the condition that the least-squares residual is orthogonal to every column of X.",
    "def": "XᵀX w = Xᵀy: the condition that the least-squares residual is orthogonal to every column of X."
  },
  "linear-probe": {
    "name": "Linear probe",
    "short": "A direction and offset fitted to predict a label from activations; its projection is the probe score.",
    "def": "A direction and offset fitted to predict a label from activations; its projection is the probe score."
  },
  "ridge": {
    "name": "Ridge",
    "short": "Least squares with a penalty on the squared norm of the coefficients; shrinks the solution and makes it unique when there are more columns than rows.",
    "def": "Least squares with a penalty on the squared norm of the coefficients; shrinks the solution and makes it unique when there are more columns than rows."
  },
  "held-out": {
    "name": "Held-out",
    "short": "Data not used to fit a direction, kept for checking what the direction predicts.",
    "def": "Data not used to fit a direction, kept for checking what the direction predicts."
  },
  "eigenvector": {
    "name": "Eigenvector",
    "short": "A nonzero vector that a square matrix only scales: A v = λ v.",
    "def": "A nonzero vector that a square matrix only scales: A v = λ v."
  },
  "eigenvalue": {
    "name": "Eigenvalue",
    "short": "The scale factor λ attached to an eigenvector.",
    "def": "The scale factor λ attached to an eigenvector."
  },
  "symmetric-matrix": {
    "name": "Symmetric matrix",
    "short": "A square matrix equal to its transpose; its eigenvectors can be chosen orthonormal and its eigenvalues are real.",
    "def": "A square matrix equal to its transpose; its eigenvectors can be chosen orthonormal and its eigenvalues are real."
  },
  "covariance-matrix": {
    "name": "Covariance matrix",
    "short": "The (d, d) matrix of covariances between pairs of coordinates across the rows; its diagonal holds variances.",
    "def": "The (d, d) matrix of covariances between pairs of coordinates across the rows; its diagonal holds variances."
  },
  "variance": {
    "name": "Variance",
    "short": "The average squared deviation from the mean; along a unit direction, the variance of the projection coefficients.",
    "def": "The average squared deviation from the mean; along a unit direction, the variance of the projection coefficients."
  },
  "pca": {
    "name": "PCA",
    "short": "Principal component analysis: the orthonormal directions of greatest variance in a centred data matrix, which are the eigenvectors of its covariance.",
    "def": "Principal component analysis: the orthonormal directions of greatest variance in a centred data matrix, which are the eigenvectors of its covariance."
  },
  "principal-component": {
    "name": "Principal component",
    "short": "One of the PCA directions, ordered by variance explained.",
    "def": "One of the PCA directions, ordered by variance explained."
  },
  "variance-explained": {
    "name": "Variance explained",
    "short": "The fraction of total variance lying along a component; the component’s eigenvalue divided by the sum of all eigenvalues.",
    "def": "The fraction of total variance lying along a component; the component’s eigenvalue divided by the sum of all eigenvalues."
  },
  "scree-plot": {
    "name": "Scree plot",
    "short": "Variance explained plotted against component number, used to see how quickly the components stop mattering.",
    "def": "Variance explained plotted against component number, used to see how quickly the components stop mattering."
  },
  "svd": {
    "name": "SVD",
    "short": "Singular value decomposition: A = U Σ Vᵀ with orthonormal U and V and non-negative singular values in Σ, for any matrix.",
    "def": "Singular value decomposition: A = U Σ Vᵀ with orthonormal U and V and non-negative singular values in Σ, for any matrix."
  },
  "singular-value": {
    "name": "Singular value",
    "short": "A diagonal entry of Σ: how much the matrix stretches along the matching right singular vector.",
    "def": "A diagonal entry of Σ: how much the matrix stretches along the matching right singular vector."
  },
  "low-rank-approximation": {
    "name": "Low-rank approximation",
    "short": "Keeping only the k largest singular triples; the best rank-k approximation in the least-squares sense.",
    "def": "Keeping only the k largest singular triples; the best rank-k approximation in the least-squares sense."
  },
  "gradient": {
    "name": "Gradient",
    "short": "The vector of partial derivatives of a scalar function; the direction of steepest increase.",
    "def": "The vector of partial derivatives of a scalar function; the direction of steepest increase."
  },
  "gradient-ascent": {
    "name": "Gradient ascent",
    "short": "Repeatedly stepping along the gradient to increase a scalar function.",
    "def": "Repeatedly stepping along the gradient to increase a scalar function."
  },
  "correlation": {
    "name": "Correlation",
    "short": "The cosine similarity of two centred sequences; between −1 and 1, zero when unrelated in the linear sense.",
    "def": "The cosine similarity of two centred sequences; between −1 and 1, zero when unrelated in the linear sense."
  },
  "permutation-test": {
    "name": "Permutation test",
    "short": "Recomputing a statistic many times with the labels shuffled, to see what values arise when there is no relation.",
    "def": "Recomputing a statistic many times with the labels shuffled, to see what values arise when there is no relation."
  },
  "baseline": {
    "name": "Baseline",
    "short": "A comparison that would also score well if the claim were empty, such as a random direction or shuffled labels.",
    "def": "A comparison that would also score well if the claim were empty, such as a random direction or shuffled labels."
  },
  "centering": {
    "name": "Centering",
    "short": "Subtracting the mean row from every row, so that the data have mean zero before PCA or covariance.",
    "def": "Subtracting the mean row from every row, so that the data have mean zero before PCA or covariance."
  },
  "outer-product": {
    "name": "Outer product",
    "short": "The (n, m) matrix u vᵀ formed from an n-vector and an m-vector; every rank-one matrix is one.",
    "def": "The (n, m) matrix u vᵀ formed from an n-vector and an m-vector; every rank-one matrix is one."
  },
  "identity-matrix": {
    "name": "Identity matrix",
    "short": "The square matrix I with ones on the diagonal; the map that changes nothing.",
    "def": "The square matrix I with ones on the diagonal; the map that changes nothing."
  },
  "attention-head-weights": {
    "name": "Attention head weights",
    "short": "For one head, the matrices W_Q, W_K, W_V of shape (d_model, d_head) and W_O of shape (d_head, d_model); the products W_Q W_Kᵀ and W_V W_O have rank at most d_head.",
    "def": "For one head, the matrices W_Q, W_K, W_V of shape (d_model, d_head) and W_O of shape (d_head, d_model); the products W_Q W_Kᵀ and W_V W_O have rank at most d_head."
  }
};
