import pygame

# Define constants for the board
WIDTH, HEIGHT = 500, 500
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 255, 255)
GREY = (192, 192, 192)
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

# Initialize piece positions using lists
piece_positions = {
    'white_king': [(4, 0)],
    'black_king': [(4, 7)],
    'white_queen': [(3, 0)],
    'black_queen': [(3, 7)],
    'white_bishop': [(2, 0), (5, 0)],
    'black_bishop': [(2, 7), (5, 7)],
    'white_knight': [(1, 0), (6, 0)],
    'black_knight': [(1, 7), (6, 7)],
    'white_rook': [(0, 0), (7, 0)],
    'black_rook': [(0, 7), (7, 7)],
    'white_pawn': [(i, 1) for i in range(8)],
    'black_pawn': [(i, 6) for i in range(8)]
}
removed_white_pieces = []
removed_black_pieces = []

check_if_moved = {
    'white_king': False,
    'black_king': False,
    'white_rook': False,
    'black_rook': False
}

# Initialize Pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")


def draw_board_cell(col_, row_):
    xx = col_ * SQUARE_SIZE
    yy = row_ * SQUARE_SIZE
    color_ = WHITE if (row_ + col_) % 2 == 0 else GREY
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


def update_pawn_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    piece_at_new_position = piece_at_position(col_, row_)
    if selected_piece_.startswith('white_pawn'):
        if col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ + 2 and \
                selected_piece_positionY_ == 1:
            # Initial move: two steps forward
            if (piece_at_new_position is None and
                    piece_at_position(col_, selected_piece_positionY_ + 1) is None):
                piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
                piece_positions[selected_piece_].append((col_, row_))
        elif (
                col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ + 1 and
                piece_at_new_position is None
        ) or (
                piece_at_new_position is not None and piece_at_new_position.startswith('black_') and
                (col_ == selected_piece_positionX_ + 1 or col_ == selected_piece_positionX_ - 1) and
                row_ == selected_piece_positionY_ + 1
        ):
            # Valid pawn move (one step forward or capturing diagonally)
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))
            if piece_at_new_position is not None:
                remove_piece_at_new_position(piece_at_new_position, col_, row_, selected_piece_)
    elif selected_piece_.startswith('black_pawn'):
        if col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ - 2 and \
                selected_piece_positionY_ == 6:
            # Initial move: two steps forward
            if (piece_at_new_position is None and
                    piece_at_position(col_, selected_piece_positionY_ - 1) is None):
                piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
                piece_positions[selected_piece_].append((col_, row_))
        elif (
                col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ - 1 and
                piece_at_new_position is None
        ) or (
                piece_at_new_position is not None and piece_at_new_position.startswith('white_') and
                (col_ == selected_piece_positionX_ + 1 or col_ == selected_piece_positionX_ - 1) and
                row_ == selected_piece_positionY_ - 1
        ):
            # Valid pawn move (one step forward or capturing diagonally)
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))
            if piece_at_new_position is not None:
                remove_piece_at_new_position(piece_at_new_position, col_, row_, selected_piece_)


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
    elif piece_at_new_position is not None and is_opposite_color(selected_piece_, piece_at_new_position) and big_check:
        piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
        piece_positions[selected_piece_].append((col_, row_))
        remove_piece_at_new_position(piece_at_new_position, col_, row_, selected_piece_)


def update_king_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_king') or selected_piece_.startswith('black_king'):
        if abs(col_ - selected_piece_positionX_) <= 1 and abs(row_ - selected_piece_positionY_) <= 1:
            # Valid king move
            update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                          selected_piece_positionY_)
            if not check_if_moved[selected_piece_]:
                check_if_moved[selected_piece_] = True


def update_queen_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_queen') or selected_piece_.startswith('black_queen'):
        if (col_ == selected_piece_positionX_ or row_ == selected_piece_positionY_ or
                abs(col_ - selected_piece_positionX_) == abs(row_ - selected_piece_positionY_)):
            # Valid queen move
            update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                          selected_piece_positionY_)


def update_bishop_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_bishop') or selected_piece_.startswith('black_bishop'):
        if abs(col_ - selected_piece_positionX_) == abs(row_ - selected_piece_positionY_):
            # Valid bishop move
            update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                          selected_piece_positionY_)


def update_knight_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_knight') or selected_piece_.startswith('black_knight'):
        if (
                (abs(col_ - selected_piece_positionX_) == 1 and abs(row_ - selected_piece_positionY_) == 2) or
                (abs(col_ - selected_piece_positionX_) == 2 and abs(row_ - selected_piece_positionY_) == 1)
        ):
            # Valid knight move
            update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                          selected_piece_positionY_)


def update_rook_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_rook') or selected_piece_.startswith('black_rook'):
        if col_ == selected_piece_positionX_ or row_ == selected_piece_positionY:
            # Valid rook move
            update_helper(col_, row_, selected_piece_, selected_piece_positionX_,
                          selected_piece_positionY_)
            if not check_if_moved[selected_piece_]:
                check_if_moved[selected_piece_] = True


def long_castle(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if (col_, row_) in [(0, selected_piece_positionY_), (2, selected_piece_positionY_)] and \
            (selected_piece_positionX_, selected_piece_positionY_) == (4, selected_piece_positionY_):
        no_piece_in_between = True
        for x_pos in range(1, 4):
            piece_in_between = piece_at_position(x_pos, selected_piece_positionY_)
            if piece_in_between is not None:
                no_piece_in_between = False
        if no_piece_in_between:
            rook_color = selected_piece_.split("_")[0]
            # Bring king to (2, y_idx)
            piece_positions[selected_piece_].remove((4, selected_piece_positionY_))
            piece_positions[selected_piece_].append((2, selected_piece_positionY_))
            # Bring rook to (3, y_idx)
            piece_positions[f'{rook_color}_rook'].remove((0, selected_piece_positionY_))
            piece_positions[f'{rook_color}_rook'].append((3, selected_piece_positionY_))


def short_castle(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if (col_, row_) in [(6, selected_piece_positionY_), (7, selected_piece_positionY_)] and \
            (selected_piece_positionX_, selected_piece_positionY_) == (4, selected_piece_positionY_):
        no_piece_in_between = True
        for x_pos in range(5, 7):
            piece_in_between = piece_at_position(x_pos, selected_piece_positionY_)
            if piece_in_between is not None:
                no_piece_in_between = False
        if no_piece_in_between:
            rook_color = selected_piece_.split("_")[0]
            # Bring king to (6, y_idx)
            piece_positions[selected_piece_].remove((4, selected_piece_positionY_))
            piece_positions[selected_piece_].append((6, selected_piece_positionY_))
            # Bring rook to (5, y_idx)
            piece_positions[f'{rook_color}_rook'].remove((7, selected_piece_positionY_))
            piece_positions[f'{rook_color}_rook'].append((5, selected_piece_positionY_))


def castling(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if (selected_piece_.startswith('white_king') and not check_if_moved[selected_piece_]
        and not check_if_moved['white_rook']) or \
            (selected_piece_.startswith('black_king') and not check_if_moved[selected_piece_] and not check_if_moved[
                'black_rook']):
        long_castle(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_)
        short_castle(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_)


# Main game loop
selected_piece = None
selected_piece_positionX, selected_piece_positionY = -1, -1
dragging = False

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
                break
            else:

                # Check and update piece movements
                update_pawn_positions(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)
                update_king_positions(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)
                update_queen_positions(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)
                update_bishop_positions(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)
                update_knight_positions(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)
                update_rook_positions(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)

                # Check and update special piece movements
                castling(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)
                # pawn_promotion(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)
                # en_passant(col, row, selected_piece, selected_piece_positionX, selected_piece_positionY)

                draw_board()  # Redraw the board to clear old and update new positions
                draw_pieces()  # Redraw the pieces with the updated positions

                selected_piece = None
                selected_piece_positionX, selected_piece_positionY = -1, -1
                dragging = False

    draw_board()
    draw_pieces()

    if dragging and selected_piece:
        x, y = pygame.mouse.get_pos()
        piece_image = piece_images[selected_piece]
        screen.blit(piece_image, (x - SQUARE_SIZE // 2, y - SQUARE_SIZE // 2))
    pygame.display.flip()

# Quit Pygame
pygame.quit()
