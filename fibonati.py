# セットアップ

import numpy as np

def fibonacci_matrix(n):
    """
    フィボナッチ行列の生成と表示を行う関数。
    
    引数:
        n (int): 行列の大きさ
    
    返り値:
        None: 何も返却しない
    """
    # 初期化: n = 1,2 のフィボナッチ数を 0, 1 で初期化する
    f0, f1 = 0, 1

    # フィボナッチ行列を生成する
    fib_matrix = np.array([[f0, f1], [f1, f0 + f1]])

    # 行列のサイズ n 倍に拡張する
    expanded_fib_matrix = np.tile(fib_matrix, (n, 1))

    return expanded_fib_matrix

# 行列を表示する関数
def display_matrix(matrix):
    """
    マトリックスを表示する関数
    
    引数:
        matrix (ndarray): 行列データ
        
    返り値:
        None: 何も返却しない
    """
    print("フィボナッチ行列")
    for row in matrix:
        row_str = ' '.join([f"{x:.2g}" if isinstance(x, float) else str(x)
                            for x in row])
        print(row_str)

# フィボナッチ行列の作成と表示
matrix_size = 5
result_matrix = fibonacci_matrix(matrix_size)
display_matrix(result_matrix)