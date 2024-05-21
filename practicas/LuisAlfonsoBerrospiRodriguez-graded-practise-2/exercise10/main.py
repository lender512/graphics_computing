def getNumberOfTriangulations(n):
    # By the theory class we know that the number of triangulations of a convex polygon with n vertices
    # is given by the n-th Catalan number.
    # this is because the number of triangulations of a convex polygon with n vertices is given by the 
    # following recursive formula:
    # T(n) = T(0) * T(n-1) + T(1) * T(n-2) + ... + T(n-1) * T(0)
    # witch can be simplified to:
    # T(n) = C(n) = (2n)! / ((n + 1)! * n!)
    # https://francis.naukas.com/files/2014/08/Dibujo20140827-catalan-numbers-polygon-decomposition-in-triangles.png
    if n < 3:
        return 0
    # we can achieve a complexity of O(n^2) and prunning the search space by using dynamic programming
    # to calculate the factorials
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    dp[2] = 1
    for i in range(3, n + 1):
        for j in range(i):
            dp[i] += dp[j] * dp[i - j - 1]
    return dp[n]