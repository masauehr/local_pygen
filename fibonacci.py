import numpy as np

def fibonacci_matrix(n):
    """
    フィボナッチ数列から n×n 行列を生成
    """
    if n <= 0:
        return np.array([])

    # フィボナッチ数列
    f = np.zeros(n, dtype=int)
    f[0] = 0
    if n > 1:
        f[1] = 1

    for i in range(2, n):
        f[i] = f[i-1] + f[i-2]

    # 行列化（ずらして配置）
    mat = np.zeros((n, n), dtype=int)
    for i in range(n):
        mat[i, :n-i] = f[:n-i]

    return mat


def display_matrix(matrix):
    print("フィボナッチ行列")
    for row in matrix:
        print(" ".join(map(str, row)))


# 実行
n = 5
matrix = fibonacci_matrix(n)
display_matrix(matrix)

