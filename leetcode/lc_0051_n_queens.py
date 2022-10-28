 # LeetCode 51: N-Queens
 
 # https://leetcode.com/problems/n-queens/
 
 
"""
The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.
 
"""

from typing import List

class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
            board = [[['.'] for _ in range(n)] for _ in range(n)]
            print(board)
            return self.place_next_queen(board)
            
    def possible_queen(self, board:List[List[str]], x, y) -> bool:
        """Returns True if a queen can be placed in (x, y)."""
        # Check if another queen in the same row
        for col in board[x]:
            if col == 'Q':
                return False
        # Check if another queen in the same column            
        for row in board: 
            if row[y] == 'Q':
                return False
        # Check diagonals
            # TODO
                
        return True
        
    def place_next_queen(self, board:List[List[str]]) -> List[List[str]]:
        dim = len(board)
        if self.count_queens(board) == dim:
            return board
        for x in range(dim):
            for y in range(dim):
                if self.possible_queen(board, x, y):
                    board[x][y] = 'Q'
                    print(board)
                    if self.count_queens(board) == dim:
                        return board
                    else:
                        board = self.place_next_queen(board)
                        if self.count_queens(board) == dim:
                            return board
                        else:
                            board[x][y] = '.'
                        print(board)
        return board
    
    def count_queens(self, board):
        count = 0
        for row in board:
            for col in row:
                if col == 'Q':
                    count += 1
        return count
    
s = Solution()
s.solveNQueens(4)
# print(
# s.count_queens([['Q', ['.'], ['.'], ['.']],
#                 [['.'], 'Q', ['.'], ['.']],
#                 [['.'], ['.'], 'Q', ['.']],
#                 [['.'], ['.'], ['.'], 'Q']])
# )