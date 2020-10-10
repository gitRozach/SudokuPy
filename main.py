from SudokuMatrix import SudokuMatrix


def main():
    # grid1 = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
    #          [6, 8, 0, 0, 7, 0, 0, 9, 0],
    #          [1, 9, 0, 0, 0, 4, 5, 0, 0],
    #          [8, 2, 0, 1, 0, 0, 0, 4, 0],
    #          [0, 0, 4, 6, 0, 2, 9, 0, 0],
    #          [0, 5, 0, 0, 0, 3, 0, 2, 8],
    #          [0, 0, 9, 3, 0, 0, 0, 7, 4],
    #          [0, 4, 0, 0, 5, 0, 0, 3, 6],
    #          [7, 0, 3, 0, 1, 8, 0, 0, 0]]

    grid2 = [[9, 0, 6, 0, 7, 0, 4, 0, 3],
             [0, 0, 0, 4, 0, 0, 2, 0, 0],
             [0, 7, 0, 0, 2, 3, 0, 1, 0],
             [5, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 4, 0, 2, 0, 8, 0, 6, 0],
             [0, 0, 3, 0, 0, 0, 0, 0, 5],
             [0, 3, 0, 7, 0, 0, 0, 5, 0],
             [0, 0, 7, 0, 0, 5, 0, 0, 0],
             [4, 0, 5, 0, 1, 0, 7, 0, 8]]

    matrix = SudokuMatrix(grid2)
    print(matrix)
    results = matrix.solve()
    print('Found %i solutions:' % len(results))
    for res in results:
        print(res[6][2])
        print(res)
        print('Valid' if res.check() else 'Invalid')


if __name__ == '__main__':
    main()
