import unittest
import puzzle

import random
import copy


class TestCube(unittest.TestCase):

    def generate_random_moves(self, num_moves, min_repeat, max_repeat):
        move_types = ["r", "R", "c", "C", "f", "F", "x", "X", "y", "Y"]

        moves = []

        for i in range(num_moves):
            repeats = random.randint(min_repeat, max_repeat)
            move = random.choice(move_types)

            moves.append(str(repeats)+move)
        
        return moves
    

    def verify_cube_colors(self, puzzle):
        colors = {'W': 0, 'Y': 0, 'B': 0, 'G': 0, 'R': 0, 'O': 0}

        for face in [puzzle.top, puzzle.bottom, puzzle.left, puzzle.right, puzzle.front, puzzle.back]:
            for row in face:
                for color in row:
                    colors[color] += 1

        for count in colors.values():
            if count != 9:
                return False

        return True
    

    def verify_crosses(self, puzzle):
        for face in [puzzle.top, puzzle.bottom, puzzle.left, puzzle.right, puzzle.front, puzzle.back]:
            if face[0][1] != face[1][1] or face[1][0] != face[1][1] or face[2][1] != face[1][1] or face[1][2] != face[1][1]:
                return False
        
        return True


    def cube_state_to_string(self, puzzle):
        return f'''Top:\n{puzzle.top[0]}\n{puzzle.top[1]}\n{puzzle.top[2]}\n Bottom:\n{puzzle.bottom[0]}\n{puzzle.bottom[1]}\n{puzzle.bottom[2]}\n
        Front:\n{puzzle.front[0]}\n{puzzle.front[1]}\n{puzzle.front[2]}\n
        Back:\n{puzzle.back[0]}\n{puzzle.back[1]}\n{puzzle.back[2]}\n
        Left:\n{puzzle.left[0]}\n{puzzle.left[1]}\n{puzzle.left[2]}\n
        Right:\n{puzzle.right[0]}\n{puzzle.right[1]}\n{puzzle.right[2]}
        -----------------------------------'''

    
    def test_solve_cube(self):
        for i in range(10000):
            cube = puzzle.Puzzle(top=[[]], bottom=[[]], left=[[]], right=[[]], back=[[]], front=[[]])

            cube.top = [
                    ['W', 'W', 'W'],
                    ['W', 'W', 'W'],
                    ['W', 'W', 'W']]
            cube.bottom = [
                    ['Y', 'Y', 'Y'],
                    ['Y', 'Y', 'Y'],
                    ['Y', 'Y', 'Y']]
            cube.front = [
                    ['B', 'B', 'B'],
                    ['B', 'B', 'B'],
                    ['B', 'B', 'B']]
            cube.back = [
                    ['G', 'G', 'G'],
                    ['G', 'G', 'G'],
                    ['G', 'G', 'G']]
            cube.left = [
                    ['R', 'R', 'R'],
                    ['R', 'R', 'R'],
                    ['R', 'R', 'R']]
            cube.right = [
                    ['O', 'O', 'O'],
                    ['O', 'O', 'O'],
                    ['O', 'O', 'O']]
            
            cube.apply_algorithm(self.generate_random_moves(50, 2, 3))

            puzzle_scrambled = copy.deepcopy(cube)

            cube.solve_cube()

            self.assertTrue(self.verify_cube_colors(cube) and self.verify_crosses(cube), f'Failed test {i}:\n{self.cube_state_to_string(puzzle_scrambled)}')


if __name__ == '__main__':
    unittest.main()
