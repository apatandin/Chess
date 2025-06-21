import pygame

# Define constants for the board
WIDTH, HEIGHT = 700, 700
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
FONT_SIZE = 36

# Load piece images
rep = "resources/chesspieces"
piece_images = {}
piece_names = [
    'king', 'queen', 'bishop', 'knight', 'rook', 'pawn'
]

for color in ['white', 'black']:
    for piece in piece_names:
        piece_images[f'{color}_{piece}'] = pygame.transform.smoothscale(
            pygame.image.load(f'{rep}/{color}_{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE)
        )

# Initialize piece positions using lists with white as player 1
piece_positions = {
    'black_king': [(4, 0)],
    'white_king': [(4, 7)],
    'black_queen': [(3, 0)],
    'white_queen': [(3, 7)],
    'black_bishop': [(2, 0), (5, 0)],
    'white_bishop': [(2, 7), (5, 7)],
    'black_knight': [(1, 0), (6, 0)],
    'white_knight': [(1, 7), (6, 7)],
    'black_rook': [(0, 0), (7, 0)],
    'white_rook': [(0, 7), (7, 7)],
    'black_pawn': [(i, 1) for i in range(8)],
    'white_pawn': [(i, 6) for i in range(8)]
}
white_first_player = True

removed_white_pieces = []
removed_black_pieces = []

check_if_moved = {
    'white_king': False,
    'black_king': False,
    'white_rook': False,
    'black_rook': False
}

# Check if pawns are initially moved 2 steps forward
check_if_moved_pawns = {
    'black_pawn': [False for i in range(8)],
    'white_pawn': [False for i in range(8)]
}

# Keep track of checks
king_is_on_check = {
    'white_king': False,
    'black_king': False
}

# Initialize Pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")


def draw_board_cell(col_, row_):
    xx = col_ * SQUARE_SIZE
    yy = row_ * SQUARE_SIZE
    color_ = WHITE if (row_ + col_) % 2 == 0 else LIGHT_BROWN
    pygame.draw.rect(screen, color_, (xx, yy, SQUARE_SIZE, SQUARE_SIZE))


def draw_board():
    for row_ in range(8):
        for col_ in range(8):
            draw_board_cell(col_, row_)


def draw_pieces():
    for piece_, positions in piece_positions.items():
        for col_, row_ in positions:
            draw_piece(piece_, col_, row_)


def draw_piece(piece_name, col_, row_):
    piece_image_ = piece_images[piece_name]
    xx, yy = col_ * SQUARE_SIZE, row_ * SQUARE_SIZE
    screen.blit(piece_image_, (xx, yy))


def piece_at_position(col_, row_):
    # Function to get the piece at a specific position on the chessboard
    for piece_, positions in piece_positions.items():
        if (col_, row_) in positions:
            return piece_
    return None  # Return None if there's no piece at the specified position


def is_opposite_color(piece1, piece2):
    # Helper function to check if two pieces are of opposite colors
    return (piece1.startswith('white_') and piece2.startswith('black_')) or \
           (piece1.startswith('black_') and piece2.startswith('white_'))


def remove_piece_at_new_position(piece_at_new_position, col_, row_, selected_piece_):
    if piece_at_new_position is not None and is_opposite_color(selected_piece_, piece_at_new_position):
        piece_positions[piece_at_new_position].remove((col_, row_))
        if piece_at_new_position.startswith('black_'):
            removed_black_pieces.append(piece_at_new_position)
        else:
            removed_white_pieces.append(piece_at_new_position)


def en_passant_helper(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_, y_offset):
    potential_opposite_pawn_left, potential_opposite_pawn_right = get_potential_pawns_en_passant(
        selected_piece_positionX_, selected_piece_positionY_)
    if col_ == selected_piece_positionX_ - 1 and row_ == selected_piece_positionY_ + y_offset and \
            potential_opposite_pawn_left is not None and potential_opposite_pawn_left.endswith('pawn'):
        if is_opposite_color(selected_piece_, potential_opposite_pawn_left) and \
                check_if_moved_pawns[potential_opposite_pawn_left][selected_piece_positionX_ - 1]:
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))

            remove_opposite_pawn_en_passant(potential_opposite_pawn_left, selected_piece_positionX_ - 1,
                                            selected_piece_positionY_)
            return True
        else:
            return False
    if col_ == selected_piece_positionX_ + 1 and row_ == selected_piece_positionY_ + y_offset and \
            potential_opposite_pawn_right is not None and potential_opposite_pawn_right.endswith('pawn'):
        if is_opposite_color(selected_piece_, potential_opposite_pawn_right) and \
                check_if_moved_pawns[potential_opposite_pawn_right][selected_piece_positionX_ + 1]:
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))

            remove_opposite_pawn_en_passant(potential_opposite_pawn_right, selected_piece_positionX_ + 1,
                                            selected_piece_positionY_)
            return True
        else:
            return False
    else:
        return False


def update_upper_pawns(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_, focus_color):
    piece_at_new_position = piece_at_position(col_, row_)
    if col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ + 2 and \
            selected_piece_positionY_ == 1:
        # Initial move: two steps forward
        if (piece_at_new_position is None and
                piece_at_position(col_, selected_piece_positionY_ + 1) is None):
            check_if_moved_pawns[selected_piece_][selected_piece_positionX_] = True
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))
            return True
        else:
            return False
    elif (
            col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ + 1 and
            piece_at_new_position is None
    ) or (
            piece_at_new_position is not None and piece_at_new_position.startswith(focus_color) and
            (col_ == selected_piece_positionX_ + 1 or col_ == selected_piece_positionX_ - 1) and
            row_ == selected_piece_positionY_ + 1
    ):
        # Valid pawn move (one step forward or capturing diagonally)
        piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
        piece_positions[selected_piece_].append((col_, row_))
        if piece_at_new_position is not None:
            remove_piece_at_new_position(piece_at_new_position, col_, row_, selected_piece_)

        # check for pawn promotion
        if row_ == 7:
            pawn_promotion(col_, row_, selected_piece_)
        return True

    elif piece_at_new_position is None and selected_piece_positionY_ == 4:
        # En passant: take pawn of opposite color if it is adjacent to this selected pawn and if
        # it has just been initially moved 2 steps forward
        return en_passant_helper(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_, 1)
    else:
        return False


def update_lower_pawns(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_, focus_color):
    piece_at_new_position = piece_at_position(col_, row_)
    if col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ - 2 and \
            selected_piece_positionY_ == 6:
        # Initial move: two steps forward
        if (piece_at_new_position is None and
                piece_at_position(col_, selected_piece_positionY_ - 1) is None):
            check_if_moved_pawns[selected_piece_][selected_piece_positionX_] = True
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))
            return True
        else:
            return False
    elif (
            col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ - 1 and
            piece_at_new_position is None
    ) or (
            piece_at_new_position is not None and piece_at_new_position.startswith(focus_color) and
            (col_ == selected_piece_positionX_ + 1 or col_ == selected_piece_positionX_ - 1) and
            row_ == selected_piece_positionY_ - 1
    ):
        # Valid pawn move (one step forward or capturing diagonally)
        piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
        piece_positions[selected_piece_].append((col_, row_))
        if piece_at_new_position is not None:
            remove_piece_at_new_position(piece_at_new_position, col_, row_, selected_piece_)

        # check for pawn promotion
        if row_ == 0:
            pawn_promotion(col_, row_, selected_piece_)
        return True
    elif piece_at_new_position is None and selected_piece_positionY_ == 3:
        # En passant: take pawn of opposite color if it is adjacent to this selected pawn and if
        # it has just been initially moved 2 steps forward
        return en_passant_helper(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_, -1)
    else:
        return False


def pawn_promotion(col_, row_, selected_piece_):
    piece_color = selected_piece_.split("_")[0]
    piece_positions[selected_piece_].remove((col_, row_))
    piece_positions[f'{piece_color}_queen'].append((col_, row_))


def get_potential_pawns_en_passant(selected_piece_positionX_, selected_piece_positionY_):
    potential_opposite_pawn_left = None
    if selected_piece_positionX_ in range(1, 8):
        potential_opposite_pawn_left = piece_at_position(selected_piece_positionX_ - 1, selected_piece_positionY_)
    potential_opposite_pawn_right = None
    if selected_piece_positionX_ in range(0, 7):
        potential_opposite_pawn_right = piece_at_position(selected_piece_positionX_ + 1, selected_piece_positionY_)
    return potential_opposite_pawn_left, potential_opposite_pawn_right


def remove_opposite_pawn_en_passant(potential_opposite_pawn, opposite_pawn_positionX_, opposite_pawn_positionY_):
    piece_positions[potential_opposite_pawn].remove((opposite_pawn_positionX_, opposite_pawn_positionY_))
    if potential_opposite_pawn.startswith('black_'):
        removed_black_pieces.append(potential_opposite_pawn)
    else:
        removed_white_pieces.append(potential_opposite_pawn)


def update_pawn_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if not white_first_player:
        if selected_piece_.startswith('white_pawn'):
            return update_upper_pawns(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_,
                                      'black')
        elif selected_piece_.startswith('black_pawn'):
            return update_lower_pawns(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_,
                                      'white')
        else:
            return False
    else:
        if selected_piece_.startswith('black_pawn'):
            return update_upper_pawns(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_,
                                      'white')
        elif selected_piece_.startswith('white_pawn'):
            return update_lower_pawns(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_,
                                      'black')
        else:
            return False


def check_if_no_pieces_present_between_old_and_new_queen_move(col_, row_, selected_piece_positionX_,
                                                              selected_piece_positionY_):
    if col_ == selected_piece_positionX_ and row_ != selected_piece_positionY_:
        for y_pos in range(min(selected_piece_positionY_, row_) + 1, max(selected_piece_positionY_, row_)):
            curr_piece_at_y_pos = piece_at_position(col_, y_pos)
            if curr_piece_at_y_pos is not None:
                return False
    elif row_ == selected_piece_positionY_ and col_ != selected_piece_positionX_:
        for x_pos in range(min(selected_piece_positionX_, col_) + 1, max(selected_piece_positionX_, col_)):
            curr_piece_at_x_pos = piece_at_position(x_pos, row_)
            if curr_piece_at_x_pos is not None:
                return False
    elif abs(col_ - selected_piece_positionX_) == abs(row_ - selected_piece_positionY_):
        x_dir = 1 if col_ > selected_piece_positionX_ else -1
        y_dir = 1 if row_ > selected_piece_positionY_ else -1
        x_pos = selected_piece_positionX_ + x_dir
        y_pos = selected_piece_positionY_ + y_dir
        while x_pos != col_ and y_pos != row_:
            curr_piece_at_x_y_pos = piece_at_position(x_pos, y_pos)
            if curr_piece_at_x_y_pos is not None:
                return False
            x_pos += x_dir
            y_pos += y_dir
    return True


def check_if_no_pieces_present_between_old_and_new_bishop_move(col_, row_, selected_piece_positionX_,
                                                               selected_piece_positionY_):
    x_dir = 1 if col_ > selected_piece_positionX_ else -1
    y_dir = 1 if row_ > selected_piece_positionY_ else -1
    x_pos = selected_piece_positionX_ + x_dir
    y_pos = selected_piece_positionY_ + y_dir
    while x_pos != col_ and y_pos != row_:
        curr_piece_at_x_y_pos = piece_at_position(x_pos, y_pos)
        if curr_piece_at_x_y_pos is not None:
            return False
        x_pos += x_dir
        y_pos += y_dir
    return True


def check_if_no_pieces_present_between_old_and_new_rook_move(col_, row_, selected_piece_positionX_,
                                                             selected_piece_positionY_):
    if col_ == selected_piece_positionX_ and row_ != selected_piece_positionY_:
        for y_pos in range(min(selected_piece_positionY_, row_) + 1, max(selected_piece_positionY_, row_)):
            curr_piece_at_y_pos = piece_at_position(col_, y_pos)
            if curr_piece_at_y_pos is not None:
                return False
    elif row_ == selected_piece_positionY_ and col_ != selected_piece_positionX_:
        for x_pos in range(min(selected_piece_positionX_, col_) + 1, max(selected_piece_positionX_, col_)):
            curr_piece_at_x_pos = piece_at_position(x_pos, row_)
            if curr_piece_at_x_pos is not None:
                return False
    return True


def update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                  selected_piece_positionY_):
    piece_at_new_position = piece_at_position(col_, row_)
    big_check = selected_piece_.endswith('king') or selected_piece_.endswith('knight') or \
                (selected_piece_.endswith('queen') and check_if_no_pieces_present_between_old_and_new_queen_move(
                    col_, row_, selected_piece_positionX_, selected_piece_positionY_)) or \
                (selected_piece_.endswith('bishop') and check_if_no_pieces_present_between_old_and_new_bishop_move(
                    col_, row_, selected_piece_positionX_, selected_piece_positionY_)) or \
                (selected_piece_.endswith('rook') and check_if_no_pieces_present_between_old_and_new_rook_move(
                    col_, row_, selected_piece_positionX_, selected_piece_positionY_))
    if piece_at_new_position is None and big_check:
        piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
        piece_positions[selected_piece_].append((col_, row_))
        return True
    elif piece_at_new_position is not None and is_opposite_color(selected_piece_, piece_at_new_position) and big_check:
        piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
        piece_positions[selected_piece_].append((col_, row_))
        remove_piece_at_new_position(piece_at_new_position, col_, row_, selected_piece_)
        return True
    else:
        return False


def update_king_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_king') or selected_piece_.startswith('black_king'):
        if abs(col_ - selected_piece_positionX_) <= 1 and abs(row_ - selected_piece_positionY_) <= 1:
            if not is_king_in_check(selected_piece_.split("_")[0], col_, row_):
                # Valid king move
                valid_king_update_ = update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                                                   selected_piece_positionY_)
                if not check_if_moved[selected_piece_]:
                    check_if_moved[selected_piece_] = True
                if king_is_on_check[selected_piece_]:
                    king_is_on_check[selected_piece_] = False
                return valid_king_update_
    return False


def update_queen_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_queen') or selected_piece_.startswith('black_queen'):
        if (col_ == selected_piece_positionX_ or row_ == selected_piece_positionY_ or
                abs(col_ - selected_piece_positionX_) == abs(row_ - selected_piece_positionY_)):
            # Valid queen move
            valid_queen_update_ = update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                                                selected_piece_positionY_)
            return valid_queen_update_
    else:
        return False


def update_bishop_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_bishop') or selected_piece_.startswith('black_bishop'):
        if abs(col_ - selected_piece_positionX_) == abs(row_ - selected_piece_positionY_):
            # Valid bishop move
            valid_bishop_update_ = update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                                                 selected_piece_positionY_)
            return valid_bishop_update_
    else:
        return False


def update_knight_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_knight') or selected_piece_.startswith('black_knight'):
        if (
                (abs(col_ - selected_piece_positionX_) == 1 and abs(row_ - selected_piece_positionY_) == 2) or
                (abs(col_ - selected_piece_positionX_) == 2 and abs(row_ - selected_piece_positionY_) == 1)
        ):
            # Valid knight move
            valid_knight_update_ = update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                                                 selected_piece_positionY_)
            return valid_knight_update_
    else:
        return False


def update_rook_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_rook') or selected_piece_.startswith('black_rook'):
        if col_ == selected_piece_positionX_ or row_ == selected_piece_positionY:
            # Valid rook move
            valid_rook_update_ = update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                                               selected_piece_positionY_)
            if not check_if_moved[selected_piece_]:
                check_if_moved[selected_piece_] = True
            return valid_rook_update_
    else:
        return False


def long_castle(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if (col_, row_) in [(0, selected_piece_positionY_), (2, selected_piece_positionY_)] and \
            (selected_piece_positionX_, selected_piece_positionY_) == (4, selected_piece_positionY_):
        no_piece_in_between = True
        king_is_not_on_check_in_between = True
        king_color = selected_piece_.split("_")[0]
        for x_pos in range(1, 4):
            piece_in_between = piece_at_position(x_pos, selected_piece_positionY_)
            if piece_in_between is not None:
                no_piece_in_between = False
            king_is_not_on_check_in_between = king_is_not_on_check_in_between and \
                                              not is_king_in_check(king_color, x_pos, selected_piece_positionY_)
        if no_piece_in_between and king_is_not_on_check_in_between:
            rook_color = selected_piece_.split("_")[0]
            # Bring king to (2, y_idx)
            piece_positions[selected_piece_].remove((4, selected_piece_positionY_))
            piece_positions[selected_piece_].append((2, selected_piece_positionY_))
            # Bring rook to (3, y_idx)
            piece_positions[f'{rook_color}_rook'].remove((0, selected_piece_positionY_))
            piece_positions[f'{rook_color}_rook'].append((3, selected_piece_positionY_))
            return True
        else:
            return False
    else:
        return False


def short_castle(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if (col_, row_) in [(6, selected_piece_positionY_), (7, selected_piece_positionY_)] and \
            (selected_piece_positionX_, selected_piece_positionY_) == (4, selected_piece_positionY_):
        no_piece_in_between = True
        king_is_not_on_check_in_between = True
        king_color = selected_piece_.split("_")[0]
        for x_pos in range(5, 7):
            piece_in_between = piece_at_position(x_pos, selected_piece_positionY_)
            if piece_in_between is not None:
                no_piece_in_between = False
            king_is_not_on_check_in_between = king_is_not_on_check_in_between and \
                                              not is_king_in_check(king_color, x_pos, selected_piece_positionY_)
        if no_piece_in_between and king_is_not_on_check_in_between:
            rook_color = selected_piece_.split("_")[0]
            # Bring king to (6, y_idx)
            piece_positions[selected_piece_].remove((4, selected_piece_positionY_))
            piece_positions[selected_piece_].append((6, selected_piece_positionY_))
            # Bring rook to (5, y_idx)
            piece_positions[f'{rook_color}_rook'].remove((7, selected_piece_positionY_))
            piece_positions[f'{rook_color}_rook'].append((5, selected_piece_positionY_))
            return True
        else:
            return False
    else:
        return False


def castling(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if (selected_piece_.startswith('white_king') and not check_if_moved[selected_piece_]
        and not check_if_moved['white_rook']) or \
            (selected_piece_.startswith('black_king') and not check_if_moved[selected_piece_] and not check_if_moved[
                'black_rook']):
        long_castle_update_ = long_castle(col_, row_, selected_piece_, selected_piece_positionX_,
                                          selected_piece_positionY_)
        short_castle_update_ = short_castle(col_, row_, selected_piece_, selected_piece_positionX_,
                                            selected_piece_positionY_)
        return long_castle_update_ or short_castle_update_


def is_king_in_check(king_color, king_x, king_y):
    for piece_, positions in piece_positions.items():
        if piece_.split('_')[0] != king_color:
            for xx, yy in positions:
                if piece_can_attack(piece_, xx, yy, king_x, king_y):
                    return True
    return False


def piece_can_attack(piece_, col_, row_, target_col, target_row):
    piece_color = piece_.split('_')[0]

    if piece_.endswith('white_pawn') or piece_.endswith('black_pawn'):
        return pawn_can_attack(col_, row_, target_col, target_row, piece_color)
    if piece_.endswith('rook') and check_if_no_pieces_present_between_old_and_new_rook_move(target_col, target_row,
                                                                                            col_, row_):
        return rook_can_attack(col_, row_, target_col, target_row)
    if piece_.endswith('knight'):
        return knight_can_attack(col_, row_, target_col, target_row)
    if piece_.endswith('bishop') and check_if_no_pieces_present_between_old_and_new_bishop_move(target_col, target_row,
                                                                                                col_, row_):
        return bishop_can_attack(col_, row_, target_col, target_row)
    if piece_.endswith('queen') and check_if_no_pieces_present_between_old_and_new_queen_move(target_col, target_row,
                                                                                              col_, row_):
        return queen_can_attack(col_, row_, target_col, target_row)
    if piece_.endswith('king'):
        return king_can_attack(col_, row_, target_col, target_row)
    return False


def pawn_can_attack(col_, row_, target_col, target_row, piece_color):
    col_diff = abs(target_col - col_)
    row_diff = target_row - row_

    return col_diff == 1 and row_diff == 1 and piece_color == 'white' or \
           col_diff == 1 and row_diff == -1 and piece_color == 'black'


def rook_can_attack(col_, row_, target_col, target_row):
    return col_ == target_col or row_ == target_row


def knight_can_attack(col_, row_, target_col, target_row):
    return (abs(target_col - col_) == 2 and abs(target_row - row_) == 1) or \
           (abs(target_col - col_) == 1 and abs(target_row - row_) == 2)


def bishop_can_attack(col_, row_, target_col, target_row):
    return abs(target_col - col_) == abs(target_row - row_)


def queen_can_attack(col_, row_, target_col, target_row):
    return rook_can_attack(col_, row_, target_col, target_row) or bishop_can_attack(col_, row_, target_col, target_row)


def king_can_attack(col_, row_, target_col, target_row):
    return abs(target_col - col_) <= 1 and abs(target_row - row_) <= 1


# Main game loop
selected_piece = None
selected_piece_positionX, selected_piece_positionY = -1, -1
dragging = False

white_to_move = True
selected_piece_moved = False  # Track if the selected piece has moved
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not dragging:
            x, y = pygame.mouse.get_pos()
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            for piece in piece_positions.keys():
                if (col, row) in piece_positions[piece]:
                    if (white_to_move and piece.startswith('white_')) or (
                            not white_to_move and piece.startswith('black_')):
                        selected_piece = piece
                        selected_piece_positionX, selected_piece_positionY = col, row
                        dragging = True
                    break

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            x, y = pygame.mouse.get_pos()
            col = x // SQUARE_SIZE
            row = y // SQUARE_SIZE
            if col not in range(0, 8) or row not in range(0, 8):
                selected_piece = None
                selected_piece_positionX, selected_piece_positionY = -1, -1
                dragging = False
                selected_piece_moved = False  # Reset the flag when the piece is not moved
                break
            else:
                if selected_piece_positionX == col and selected_piece_positionY == row:
                    # Piece didn't move; deselect it and continue the same player's turn
                    selected_piece = None
                    dragging = False
                else:
                    # Check and update piece movements
                    valid_move_exists = False
                    current_color = selected_piece.split("_")[0]
                    ## Selected piece is not a king but the king of its color is on check
                    if king_is_on_check[f"{current_color}_king"] and not selected_piece.endswith(
                            f"{current_color}_king"):
                        selected_piece = None
                        dragging = False
                    ## Selected piece is a king and is on check
                    elif king_is_on_check[f"{current_color}_king"] and selected_piece.endswith(f"{current_color}_king"):
                        ## Can only bring king to a cell where the king will not be on check.
                        possible_king_moves = []
                        for cl_ in [selected_piece_positionX - 1, selected_piece_positionX,
                                    selected_piece_positionX + 1]:
                            for rw_ in [selected_piece_positionY - 1, selected_piece_positionY,
                                        selected_piece_positionY + 1]:
                                if cl_ != selected_piece_positionX and rw_ != selected_piece_positionY:
                                    if not is_king_in_check(current_color, cl_, rw_):
                                        possible_king_moves.append((cl_, rw_))
                        ## TODO: this case does not include the correct possible king moves
                        print(f"({col}, {row}) is in {possible_king_moves}")
                        if (col, row) in possible_king_moves:
                            valid_king_update = update_king_positions(col, row, selected_piece,
                                                                      selected_piece_positionX,
                                                                      selected_piece_positionY)
                    # if (king_is_on_check["white_king"] and not selected_piece.endswith("white_king")) or \
                    #         (king_is_on_check["black_king"] and not selected_piece.endswith("black_king")):
                    #     # King piece is on check but another piece was selected;
                    #     # Deselect other piece and continue same player's turn
                    #     #TODO: keep track of a list of pieces that attack the king. And if the selected_piece is not a king,
                    #     # then it can still be moved to a position that blocks the attacking pieces.
                    #     selected_piece = None
                    #     dragging = False
                    else:

                        valid_pawn_update = update_pawn_positions(col, row, selected_piece, selected_piece_positionX,
                                                                  selected_piece_positionY)

                        valid_king_update = update_king_positions(col, row, selected_piece, selected_piece_positionX,
                                                                  selected_piece_positionY)

                        valid_queen_update = update_queen_positions(col, row, selected_piece, selected_piece_positionX,
                                                                    selected_piece_positionY)
                        valid_bishop_update = update_bishop_positions(col, row, selected_piece,
                                                                      selected_piece_positionX,
                                                                      selected_piece_positionY)
                        valid_knight_update = update_knight_positions(col, row, selected_piece,
                                                                      selected_piece_positionX,
                                                                      selected_piece_positionY)
                        valid_rook_update = update_rook_positions(col, row, selected_piece, selected_piece_positionX,
                                                                  selected_piece_positionY)

                        valid_castling = castling(col, row, selected_piece, selected_piece_positionX,
                                                  selected_piece_positionY)

                        valid_move_exists = valid_pawn_update or valid_king_update or valid_queen_update or \
                                            valid_bishop_update or valid_knight_update or valid_rook_update or valid_castling

                        if valid_move_exists:
                            king_piece = "white_king" if current_color == "black" else "black_king"
                            king_positionX = piece_positions[king_piece][0][0]
                            king_positionY = piece_positions[king_piece][0][1]

                            if piece_can_attack(selected_piece, col, row, king_positionX, king_positionY):
                                king_is_on_check[king_piece] = True
                                print(king_is_on_check)

                    draw_board()  # Redraw the board to clear old and update new positions
                    draw_pieces()  # Redraw the pieces with the updated positions

                    selected_piece = None
                    dragging = False
                    selected_piece_moved = True  # Set the flag to true when the piece is moved

                    # Toggle player turn if the piece has moved
                    if selected_piece_moved:
                        if valid_move_exists:
                            white_to_move = not white_to_move

    draw_board()
    draw_pieces()

    if dragging and selected_piece:
        x, y = pygame.mouse.get_pos()
        piece_image = piece_images[selected_piece]
        screen.blit(piece_image, (x - SQUARE_SIZE // 2, y - SQUARE_SIZE // 2))
    pygame.display.flip()

# Quit Pygame
pygame.quit()
