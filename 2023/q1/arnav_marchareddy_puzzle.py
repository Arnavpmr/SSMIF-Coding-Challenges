from enum import Enum
import re


"""
Position Schema (Array indexes in flattened out rubiks cube diagram)

                             Back
                      | 0,0 | 0,1 | 0,2 | <- Ex: self.Back[0][2]
                      -------------------
                      | 1,0 | 1,1 | 1,2 |
                      -------------------
                      | 2,0 | 2,1 | 2,2 |

       Left                  Top                   Right                 Bottom
| 0,0 | 0,1 | 0,2 |   | 0,0 | 0,1 | 0,2 |   | 0,0 | 0,1 | 0,2 |   | 0,0 | 0,1 | 0,2 |
-------------------   -------------------   -------------------   -------------------
| 1,0 | 1,1 | 1,2 |   | 1,0 | 1,1 | 1,2 |   | 1,0 | 1,1 | 1,2 |   | 1,0 | 1,1 | 1,2 |
-------------------   -------------------   -------------------   -------------------
| 2,0 | 2,1 | 2,2 |   | 2,0 | 2,1 | 2,2 |   | 2,0 | 2,1 | 2,2 |   | 2,0 | 2,1 | 2,2 |

                             Front
                      | 0,0 | 0,1 | 0,2 |
                      -------------------
                      | 1,0 | 1,1 | 1,2 |
                      -------------------
                      | 2,0 | 2,1 | 2,2 |
"""


class Puzzle:

    """
    The purpose of this schema is to store the ordering of indexes as represented
    in the position schema diagram above for all rows and columns with respect to the front face
    """
    __positions_schema = {
        "rows": [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)]
        ],
        "cols": [
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)]
        ]
    }

    def __init__(self, top, bottom, left, right, back, front):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.back = back
        self.front = front

    """
    Given 4 faces as well as their corresponding indices to swap, this function will swap
    the indices in order from face1 to face4. The turn of a row, column or face could be done
    with this function through changing the order of the faces passed and passing different indices
    for each face as necessary.
    """

    def __swap_layers(self, face1, layer1, face2, layer2, face3, layer3, face4, layer4):
        faces = [face2, face3, face4, face1]
        layers = [layer2, layer3, layer4, layer1]
        temp_layer = [face1[i][j] for (i, j) in layer1]

        for item in zip(faces, layers):
            new_temp_layer = [item[0][i][j] for (i, j) in item[1]]

            for i, pos in enumerate(item[1]):
                item[0][pos[0]][pos[1]] = temp_layer[i]

            temp_layer = new_temp_layer

    def rotate_row_right(self, row_num):
        if row_num == 0:
            # Any faces are rotated as well if the row isnt a middle row
            self.__rotate_face_anti_clockwise(self.top)

            # From the order of the parameters, front's row indices replace right's row indices.
            # Right's row indices, replace back's row indices, etc.
            # The indices to pass is based off the position schema at the top of the file
            # This same process is used in all other rotation methods.
            self.__swap_layers(self.front, self.__positions_schema["rows"][row_num],
                               self.right, self.__positions_schema["cols"][row_num][::-1],
                               self.back, self.__positions_schema["rows"][2][::-1],
                               self.left, self.__positions_schema["cols"][2])

        elif row_num == 2:
            self.__rotate_face_clockwise(self.bottom)
            self.__swap_layers(self.front, self.__positions_schema["rows"][row_num],
                               self.right, self.__positions_schema["cols"][row_num][::-1],
                               self.back, self.__positions_schema["rows"][0][::-1],
                               self.left, self.__positions_schema["cols"][0])

        else:
            self.__swap_layers(self.front, self.__positions_schema["rows"][row_num],
                               self.right, self.__positions_schema["cols"][row_num][::-1],
                               self.back, self.__positions_schema["rows"][row_num][::-1],
                               self.left, self.__positions_schema["cols"][row_num])

    def rotate_row_left(self, row_num):
        if row_num == 0:
            self.__rotate_face_clockwise(self.top)
            self.__swap_layers(self.front, self.__positions_schema["rows"][row_num],
                               self.left, self.__positions_schema["cols"][2],
                               self.back, self.__positions_schema["rows"][2][::-1],
                               self.right, self.__positions_schema["cols"][row_num][::-1])

        elif row_num == 2:
            self.__rotate_face_anti_clockwise(self.bottom)
            self.__swap_layers(self.front, self.__positions_schema["rows"][row_num],
                               self.left, self.__positions_schema["cols"][0],
                               self.back, self.__positions_schema["rows"][0][::-1],
                               self.right, self.__positions_schema["cols"][row_num][::-1])

        else:
            self.__swap_layers(self.front, self.__positions_schema["rows"][row_num],
                               self.left, self.__positions_schema["cols"][row_num],
                               self.back, self.__positions_schema["rows"][row_num][::-1],
                               self.right, self.__positions_schema["cols"][row_num][::-1])

    def rotate_col_up(self, col_num):
        if col_num == 0:
            self.__rotate_face_anti_clockwise(self.left)
            self.__swap_layers(self.front, self.__positions_schema["cols"][col_num][::-1],
                               self.top, self.__positions_schema["cols"][col_num][::-1],
                               self.back, self.__positions_schema["cols"][col_num][::-1],
                               self.bottom, self.__positions_schema["cols"][2])

        elif col_num == 2:
            self.__rotate_face_clockwise(self.right)
            self.__swap_layers(self.front, self.__positions_schema["cols"][col_num][::-1],
                               self.top, self.__positions_schema["cols"][col_num][::-1],
                               self.back, self.__positions_schema["cols"][col_num][::-1],
                               self.bottom, self.__positions_schema["cols"][0])

        else:
            self.__swap_layers(self.front, self.__positions_schema["cols"][col_num][::-1],
                               self.top, self.__positions_schema["cols"][col_num][::-1],
                               self.back, self.__positions_schema["cols"][col_num][::-1],
                               self.bottom, self.__positions_schema["cols"][col_num])

    def rotate_col_down(self, col_num):
        if col_num == 0:
            self.__rotate_face_clockwise(self.left)
            self.__swap_layers(self.front, self.__positions_schema["cols"][col_num][::-1],
                               self.bottom, self.__positions_schema["cols"][2],
                               self.back, self.__positions_schema["cols"][col_num][::-1],
                               self.top, self.__positions_schema["cols"][0][::-1])

        elif col_num == 2:
            self.__rotate_face_anti_clockwise(self.right)
            self.__swap_layers(self.front, self.__positions_schema["cols"][col_num][::-1],
                               self.bottom, self.__positions_schema["cols"][0],
                               self.back, self.__positions_schema["cols"][col_num][::-1],
                               self.top, self.__positions_schema["cols"][col_num][::-1])

        else:
            self.__swap_layers(self.front, self.__positions_schema["cols"][col_num],
                               self.bottom, self.__positions_schema["cols"][col_num][::-1],
                               self.back, self.__positions_schema["cols"][col_num],
                               self.top, self.__positions_schema["cols"][col_num])

    def rotate_face_right(self, face_num):
        if face_num == 0:
            self.__rotate_face_clockwise(self.front)
            self.__swap_layers(self.top, self.__positions_schema["rows"][2],
                               self.right, self.__positions_schema["rows"][2],
                               self.bottom, self.__positions_schema["rows"][2],
                               self.left, self.__positions_schema["rows"][2])

        elif face_num == 2:
            self.__rotate_face_anti_clockwise(self.back)
            self.__swap_layers(self.top, self.__positions_schema["rows"][0],
                               self.right, self.__positions_schema["rows"][0],
                               self.bottom, self.__positions_schema["rows"][0],
                               self.left, self.__positions_schema["rows"][0])

        else:
            self.__swap_layers(self.top, self.__positions_schema["rows"][face_num],
                               self.right, self.__positions_schema["rows"][face_num],
                               self.bottom, self.__positions_schema["rows"][face_num],
                               self.left, self.__positions_schema["rows"][face_num])

    def rotate_face_left(self, face_num):
        if face_num == 0:
            self.__rotate_face_anti_clockwise(self.front)
            self.__swap_layers(self.top, self.__positions_schema["rows"][2][::-1],
                               self.left, self.__positions_schema["rows"][2][::-1],
                               self.bottom, self.__positions_schema["rows"][2][::-1],
                               self.right, self.__positions_schema["rows"][2][::-1])

        elif face_num == 2:
            self.__rotate_face_clockwise(self.back)
            self.__swap_layers(self.top, self.__positions_schema["rows"][0][::-1],
                               self.left, self.__positions_schema["rows"][0][::-1],
                               self.bottom, self.__positions_schema["rows"][0][::-1],
                               self.right, self.__positions_schema["rows"][0][::-1])

        else:
            self.__swap_layers(self.top, self.__positions_schema["rows"][face_num][::-1],
                               self.left, self.__positions_schema["rows"][face_num][::-1],
                               self.bottom, self.__positions_schema["rows"][face_num][::-1],
                               self.right, self.__positions_schema["rows"][face_num][::-1])

    def rotate_cube_right(self):
        # Rotating the cube can be simplified to rotating each of its three rows in the corresponding direction
        for i in range(3):
            self.rotate_row_right(i)

    def rotate_cube_left(self):
        for i in range(3):
            self.rotate_row_left(i)

    def rotate_cube_up(self):
        for i in range(3):
            self.rotate_col_up(i)

    def rotate_cube_down(self):
        for i in range(3):
            self.rotate_col_down(i)

    # I used an enum class to represent the different faces as its needed for several helpers functions below
    class Faces(Enum):
        TOP = 1
        BOTTOM = 2
        LEFT = 3
        RIGHT = 4
        FRONT = 5
        BACK = 6

    # This enum represents the progress of the algorithm when its solving the cube.
    class SolveState(Enum):
        # Theres no aligned cross on the top layer (in progress)
        FIRST_LAYER = 1

        # The middle layer is being solved
        MIDDLE_LAYER = 2

        # Theres no cross on the bottom layer so a cross is being made
        BOTTOM_LAYER = 3

        # Theres a cross on the bottom layer, but the pieces arent aligned
        # Its in progress of aligning the edge pieces
        BOTTOM_LAYER_CROSS = 4

        # The cube has been solved with a cross on every face of the corresponding color
        FINISHED = 5

    def solve_cube(self):
        status = self.SolveState.FIRST_LAYER

        """
        A finite state machine is used here where the algorithm transitions from
        state to state based on the progress of the cube
        """
        while status != self.SolveState.FINISHED:

            if status == self.SolveState.FIRST_LAYER:
                if self.__top_layer_has_aligned_cross():
                    status = self.SolveState.MIDDLE_LAYER
                    continue

                # This function locates a misplaced top edge piece and puts it in the correct position
                self.__fix_next_top_edge_piece()

            if status == self.SolveState.MIDDLE_LAYER:
                if self.__is_middle_layer_solved():
                    status = self.SolveState.BOTTOM_LAYER

                    # The cube is flipped so the bottom layer becomes the new top layer
                    self.apply_algorithm(["2y"])
                    continue

                self.__fix_next_middle_edge_piece()

            if status == self.SolveState.BOTTOM_LAYER:
                if self.__has_cross(self.top):
                    status = self.SolveState.BOTTOM_LAYER_CROSS
                    continue

                # This function forms an "unaligned" cross on the bottom layer
                self.__form_bottom_layer_cross()

            if status == self.SolveState.BOTTOM_LAYER_CROSS:
                if self.__top_layer_has_aligned_cross():
                    status = self.SolveState.FINISHED
                    continue

                self.__align_bottom_layer_cross()

    """
    This function as well as my other solver helpers use state based pattern matching.
    It does this to look for specific patterns/orientations of pieces, then determines the algorithm
    to use to move it to place. Although if statements could've been used, defining a function to match these
    patterns against the cube adds a lot more flexibility and makes it much easier to define rules to match against
    in the other layers. It sort of abstracts that functionality a bit.
    Patterns:
    * - Means the piece could be any color
    W - Means the piece must only be white (other chars could be added next to it to include more possible colors)
    -W - (-) is the exclusion operator which means the piece cannot be the excluded colors
    """

    def __fix_next_top_edge_piece(self):
        while True:
            t_col = self.top[1][1]
            b_col = self.bottom[1][1]
            f_col = self.front[1][1]
            l_col = self.left[1][1]
            r_col = self.right[1][1]

            # Any faces not included in a state are assumed to be anything
            state1 = {
                self.Faces.TOP: [["*", "*", "*"],
                                 ["*", t_col, "*"],
                                 ["*", t_col, "*"]],

                self.Faces.FRONT: [["*", "-"+f_col, "*"],
                                   ["*", f_col, "*"],
                                   ["*", "*", "*"]]
            }
            state2 = {
                self.Faces.TOP: [["*", "*", "*"],
                                 ["*", t_col, "*"],
                                 ["*", "-"+t_col, "*"]],

                self.Faces.FRONT: [["*", t_col, "*"],
                                   ["*", f_col, "*"],
                                   ["*", "*", "*"]]
            }
            state3 = {
                self.Faces.LEFT: [["*", "*", "*"],
                                  ["*", l_col, "*"],
                                  ["*", "*", "*"]],

                self.Faces.FRONT: [["*", "*", "*"],
                                   [t_col, f_col, "*"],
                                   ["*", "*", "*"]]
            }
            state4 = {
                self.Faces.FRONT: [["*", "*", "*"],
                                   ["*", f_col, "*"],
                                   ["*", t_col, "*"]],

                self.Faces.BOTTOM: [["*", "*", "*"],
                                    ["*", b_col, "*"],
                                    ["*", "*", "*"]]
            }
            state5 = {
                self.Faces.RIGHT: [["*", "*", "*"],
                                   ["*", r_col, "*"],
                                   ["*", "*", "*"]],

                self.Faces.FRONT: [["*", "*", "*"],
                                   ["*", f_col, t_col],
                                   ["*", "*", "*"]]
            }
            state6 = {
                self.Faces.FRONT: [["*", "*", "*"],
                                   ["*", f_col, "*"],
                                   ["*", "*", "*"]],

                self.Faces.BOTTOM: [["*", "*", "*"],
                                    ["*", b_col, "*"],
                                    ["*", t_col, "*"]]
            }

            """
            Based on the state it matches to, it makes a decision of what
            set of moves to make or algorithms to use.
            The approach used is to check possible positions on the front face only.
            If no top edge pieces are present in those positions, it simply rotates the cube
            to check the new front face. This method drastically simplifies the range of positions to check.
            As soon as this function matches to a state and applies those moves, it exits regardless of whether
            the top layer is solved yet or not. All this function does is looks at the current cube state, then
            makes a move.
            """
            if self.__matches_state(state1):
                self.apply_algorithm(["2F0"])
                self.__align_bottom_edge_piece()
                self.apply_algorithm(["2F0"])
                return
            elif self.__matches_state(state2):
                self.apply_algorithm(["F0", "C0", "r2", "c0"])
                self.__align_bottom_edge_piece()
                self.apply_algorithm(["2F0"])
                return
            elif self.__matches_state(state3):
                self.apply_algorithm(["C0", "r2", "c0"])
                self.__align_bottom_edge_piece()
                self.apply_algorithm(["2F0"])
                return
            elif self.__matches_state(state4):
                self.apply_algorithm(["f0", "C0", "r2", "c0"])
                self.__align_bottom_edge_piece()
                self.apply_algorithm(["2F0"])
                return
            elif self.__matches_state(state5):
                self.apply_algorithm(["C2", "R2", "c2"])
                self.__align_bottom_edge_piece()
                self.apply_algorithm(["2F0"])
                return
            elif self.__matches_state(state6):
                self.__align_bottom_edge_piece()
                self.apply_algorithm(["2F0"])
                return
            else:
                self.rotate_cube_right()

    # A similiar philosophy is used for locating and fixing middle edge pieces as the previous function

    def __fix_next_middle_edge_piece(self):
        while True:
            t_col = self.top[1][1]
            b_col = self.bottom[1][1]
            f_col = self.front[1][1]
            l_col = self.left[1][1]
            r_col = self.right[1][1]

            # Excludes the top and bottom layer colors
            exclude_tb = "-"+t_col+b_col

            # These turnary conditions prevent the function from picking a piece thats already in the right position
            # Through conditionally setting which pieces to exclude when setting creating the state
            exclude_left = exclude_tb if self.front[1][0] != f_col else exclude_tb+l_col
            exclude_right = exclude_tb if self.front[1][2] != f_col else exclude_tb+r_col
            exclude_bottom = exclude_tb if self.front[2][1] != f_col else exclude_tb+b_col

            state1 = {
                self.Faces.LEFT: [["*", "*", "*"],
                                  ["*", l_col, l_col],
                                  ["*", exclude_left, "*"]],

                self.Faces.FRONT: [["*", f_col, "*"],
                                   [exclude_tb, f_col, "*"],
                                   ["*", "*", "*"]]
            }

            state2 = {
                self.Faces.FRONT: [["*", f_col, "*"],
                                   ["*", f_col, "*"],
                                   ["*", exclude_tb, "*"]],

                self.Faces.BOTTOM: [["*", "*", "*"],
                                    ["*", "*", "*"],
                                    ["*", exclude_bottom, "*"]]
            }

            state3 = {
                self.Faces.RIGHT: [["*", "*", "*"],
                                   [r_col, r_col, "*"],
                                   ["*", exclude_right, "*"]],

                self.Faces.FRONT: [["*", f_col, "*"],
                                   ["*", f_col, exclude_tb],
                                   ["*", "*", "*"]]
            }

            # The goal is to move the middle edge piece to the bottom layer, then align it with its corresponding face
            if self.__matches_state(state1):
                self.apply_algorithm(["C0", "r2", "c0"])
                self.__align_bottom_edge_piece()
            elif self.__matches_state(state2):
                self.__align_bottom_edge_piece()
            elif self.__matches_state(state3):
                self.apply_algorithm(["C2", "R2", "c2"])
                self.__align_bottom_edge_piece()
            else:
                self.rotate_cube_right()
                continue

            # These conditions decide which side the piece fits into (left or right face) and applies moves accordingly
            if self.bottom[2][1] == self.left[1][1]:
                self.apply_algorithm(
                    ["r2", "C0", "r2", "c0", "R2", "F0", "R2", "f0"])
            elif self.bottom[2][1] == self.right[1][1]:
                self.apply_algorithm(
                    ["R2", "C2", "R2", "c2", "r2", "f0", "r2", "F0"])

            return

    # Forms a cross on the bottom layer but again, doesnt do it in one function call. It progresses
    # through the stages across several calls with the mechanics of the finite state machine.

    def __form_bottom_layer_cross(self):
        while True:
            t_col = self.top[1][1]
            b_col = self.bottom[1][1]

            exclude_tb = "-"+t_col+b_col

            """
            There are so many states the bottom layer can be found in whether its face's color forms a dot, a hook or a line.
            This includes all their possible orientations too.
            """
            state1 = {
                self.Faces.TOP: [["*", exclude_tb, "*"],
                                 [exclude_tb, t_col, exclude_tb],
                                 ["*", exclude_tb, "*"]]
            }

            state2 = {
                self.Faces.TOP: [["*", exclude_tb, "*"],
                                 [exclude_tb, t_col, t_col],
                                 ["*", t_col, "*"]]
            }

            state3 = {
                self.Faces.TOP: [["*", t_col, "*"],
                                 [exclude_tb, t_col, t_col],
                                 ["*", exclude_tb, "*"]]
            }

            state4 = {
                self.Faces.TOP: [["*", t_col, "*"],
                                 [t_col, t_col, exclude_tb],
                                 ["*", exclude_tb, "*"]]
            }

            state5 = {
                self.Faces.TOP: [["*", exclude_tb, "*"],
                                 [t_col, t_col, exclude_tb],
                                 ["*", t_col, "*"]]
            }

            state6 = {
                self.Faces.TOP: [["*", exclude_tb, "*"],
                                 [t_col, t_col, t_col],
                                 ["*", exclude_tb, "*"]]
            }

            state7 = {
                self.Faces.TOP: [["*", t_col, "*"],
                                 [exclude_tb, t_col, exclude_tb],
                                 ["*", t_col, "*"]]
            }

            edge_flipping_algorithm = ["f0", "c2", "R0", "C2", "r0", "F0"]

            # The goal of these functions is to apply the corresponding algorithms based on the current state
            # to get the bottom layer to have a cross. Again this function doesnt form a cross in one go, it simply
            # makes a set of moves based on the current state of the cube to progress it to its next state
            # The bottom layer could progress from a dot, to a hook, to a line, then to a cross
            if self.__matches_state(state1) or self.__matches_state(state4) or self.__matches_state(state6):
                self.apply_algorithm(edge_flipping_algorithm)
            elif self.__matches_state(state2):
                self.apply_algorithm(["2R0"] + edge_flipping_algorithm)
            elif self.__matches_state(state3):
                self.apply_algorithm(["r0"] + edge_flipping_algorithm)
            elif self.__matches_state(state5):
                self.apply_algorithm(["R0"] + edge_flipping_algorithm)
            elif self.__matches_state(state7):
                self.apply_algorithm(["R0"] + edge_flipping_algorithm)

            return

    """
    This function uses a similiar philosophy as the previous 2 functions to decide moves to align the cross
    on the bottom layer based on its current state
    """

    def __align_bottom_layer_cross(self):
        while True:
            t_col = self.top[1][1]
            ba_col = self.back[1][1]
            f_col = self.front[1][1]
            l_col = self.left[1][1]
            r_col = self.right[1][1]

            match_top = [["*", t_col, "*"],
                         [t_col, t_col, t_col],
                         ["*", t_col, "*"]]

            match_front = [["*", f_col, "*"],
                           [f_col, f_col, f_col],
                           ["*", f_col, "*"]]

            match_back = [["*", ba_col, "*"],
                          [ba_col, ba_col, ba_col],
                          ["*", ba_col, "*"]]

            match_left = [["*", l_col, "*"],
                          [l_col, l_col, l_col],
                          ["*", l_col, "*"]]

            match_right = [["*", r_col, "*"],
                           [r_col, r_col, r_col],
                           ["*", r_col, "*"]]

            state1 = {
                self.Faces.TOP: match_top,

                self.Faces.FRONT: match_front,

                self.Faces.RIGHT: match_right
            }

            state2 = {
                self.Faces.TOP: match_top,

                self.Faces.RIGHT: match_right,

                self.Faces.BACK: match_back
            }

            state3 = {
                self.Faces.TOP: match_top,

                self.Faces.BACK: match_back,

                self.Faces.LEFT: match_left
            }

            state4 = {
                self.Faces.TOP: match_top,

                self.Faces.LEFT: match_left,

                self.Faces.FRONT: match_front
            }

            state5 = {
                self.Faces.TOP: match_top,

                self.Faces.FRONT: match_front,

                self.Faces.BACK: match_back
            }

            state6 = {
                self.Faces.TOP: match_top,

                self.Faces.LEFT: match_left,

                self.Faces.RIGHT: match_right
            }

            edge_rotation_algorithm = ["c2", "R0",
                                       "C2", "R0", "c2", "2R0", "C2", "R0"]

            if self.__matches_state(state1):
                self.rotate_cube_right()
                self.apply_algorithm(edge_rotation_algorithm)
            elif self.__matches_state(state2):
                self.apply_algorithm(edge_rotation_algorithm)
            elif self.__matches_state(state3):
                self.rotate_cube_left()
                self.apply_algorithm(edge_rotation_algorithm)
            elif self.__matches_state(state4):
                self.apply_algorithm(["2X"])
                self.apply_algorithm(edge_rotation_algorithm)
            elif self.__matches_state(state5):
                self.apply_algorithm(edge_rotation_algorithm)
            elif self.__matches_state(state6):
                self.rotate_cube_left()
                self.apply_algorithm(edge_rotation_algorithm)
            else:
                self.rotate_row_right(0)

            return

    """
    A state object has a list of faces which represent the states to match in the
    corresponding faces of the cube.
    * - Means the piece could be any color
    W - Means the piece must only be white (other chars could be added next to it to include more possible colors)
    -W - (-) is the exclusion operator which means the piece cannot be the excluded colors (other chars could be added next to it to further exclude)
    """

    def __matches_state(self, state):
        state_dict = {
            self.Faces.TOP: self.top,
            self.Faces.BOTTOM: self.bottom,
            self.Faces.LEFT: self.left,
            self.Faces.RIGHT: self.right,
            self.Faces.FRONT: self.front,
            self.Faces.BACK: self.back,
        }

        for face_key in state:
            for i in range(3):
                for j in range(3):
                    if state[face_key][i][j] == "*":
                        continue
                    elif state[face_key][i][j].startswith("-"):
                        if state_dict[face_key][i][j] in state[face_key][i][j]:
                            return False
                    elif state_dict[face_key][i][j] not in state[face_key][i][j]:
                        return False

        return True

    # Given a face, this method checks if it has a cross or not

    def __has_cross(self, face):
        face_color = face[1][1]

        return (face[0][1] == face_color and
                face[1][0] == face_color and
                face[1][2] == face_color and
                face[2][1] == face_color)

    def __top_layer_has_aligned_cross(self):
        return (self.__has_cross(self.top) and
                self.front[1][1] == self.front[0][1] and
                self.left[1][1] == self.left[1][2] and
                self.right[1][1] == self.right[1][0] and
                self.back[1][1] == self.back[2][1])

    # It aligns the bottom edge piece on the front face to its corresponding face through rotating
    # the top two rows.

    def __align_bottom_edge_piece(self):
        while self.front[2][1] != self.front[1][1]:
            self.apply_algorithm(["R0", "R1"])

    # This function checks if the middle layer is in a solved state

    def __is_middle_layer_solved(self):

        t_col = self.top[1][1]
        ba_col = self.back[1][1]
        f_col = self.front[1][1]
        l_col = self.left[1][1]
        r_col = self.right[1][1]

        solved_middle_layer_state = {
            self.Faces.TOP: [["*", t_col, "*"],
                             [t_col, t_col, t_col],
                             ["*", t_col, "*"]],

            self.Faces.FRONT: [["*", f_col, "*"],
                               [f_col, f_col, f_col],
                               ["*", "*", "*"]],

            self.Faces.LEFT:  [["*", l_col, "*"],
                               ["*", l_col, l_col],
                               ["*", l_col, "*"]],

            self.Faces.RIGHT: [["*", r_col, "*"],
                               [r_col, r_col, "*"],
                               ["*", r_col, "*"]],

            self.Faces.BACK:  [["*", "*", "*"],
                               [ba_col, ba_col, ba_col],
                               ["*", ba_col, "*"]],
        }

        return self.__matches_state(solved_middle_layer_state)

    """
    This function is super handy to have. Given a list of moves, it applies
    those moves one at a time to the cube.
    A move is defined by a number, followed by a character, followed by an index
    the first number defines how many times to repeat the move
    the character represents the type of move
    the index represents the index of the row/col/face to turn.
    Note: x and y turn the whole cube so they dont take an index
    """

    def apply_algorithm(self, moves: list[str]):
        for move in moves:
            repeats, turn, index = "", "", ""

            pattern = r'(\d*)([a-zA-Z])(\d?)'

            match = re.match(pattern, move)

            if match:
                repeats, turn, index = match.group(
                    1), match.group(2), match.group(3)

            if not repeats:
                repeats = "1"

            if not index:
                index = "0"

            index, repeats = int(index), int(repeats)

            for _ in range(repeats):
                if turn == "r":
                    self.rotate_row_right(index)
                elif turn == "R":
                    self.rotate_row_left(index)
                elif turn == "c":
                    self.rotate_col_up(index)
                elif turn == "C":
                    self.rotate_col_down(index)
                elif turn == "f":
                    self.rotate_face_right(index)
                elif turn == "F":
                    self.rotate_face_left(index)
                elif turn == "x":
                    self.rotate_cube_right()
                elif turn == "X":
                    self.rotate_cube_left()
                elif turn == "y":
                    self.rotate_cube_up()
                elif turn == "Y":
                    self.rotate_cube_down()

    # Rotates a face/matrix 90 degrees clockwise

    def __rotate_face_clockwise(self, face):
        n = len(face)

        # transpose matrix
        for i in range(n):
            for j in range(i, n):
                face[i][j], face[j][i] = face[j][i], face[i][j]

        # reverse rows
        for i in range(n):
            face[i] = face[i][::-1]

    # Rotates a face/matrix 90 degrees anticlockwise

    def __rotate_face_anti_clockwise(self, face):
        n = len(face)

        # swap elements along anti-diagonal axis
        for i in range(n):
            for j in range(n-i):
                face[i][j], face[n-j-1][n-i-1] = face[n-j-1][n-i-1], face[i][j]

        # reverse columns
        for i in range(n):
            face[i] = face[i][::-1]

    def __switch_to_optimal_orientation(self):
        """
        TODO Given the starting rubiks cube state, it would look to see if any layers are already solved or
        close to solved, then determine if it is more optimal to make those the top layer to start at.
        If thats the case, it would rotate the cube to the optimal top layer.
        This helper could not be implemented in time but would've been nice to have as a further optimization.
        """
        pass
