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


def update_pawn_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_pawn'):
        if (
                (col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ + 1) or
                (col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ + 2 and
                 selected_piece_positionY_ == 1)
        ):
            # Valid pawn move
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))
    elif selected_piece_.startswith('black_pawn'):
        if (
                (col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ - 1) or
                (col_ == selected_piece_positionX_ and row_ == selected_piece_positionY_ - 2 and
                 selected_piece_positionY_ == 6)
        ):
            # Valid pawn move
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))


def update_king_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_king') or selected_piece_.startswith('black_king'):
        if abs(col_ - selected_piece_positionX_) <= 1 and abs(row_ - selected_piece_positionY_) <= 1:
            # Valid king move
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))


def update_queen_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_queen') or selected_piece_.startswith('black_queen'):
        if (col_ == selected_piece_positionX_ or row_ == selected_piece_positionY_ or
                abs(col_ - selected_piece_positionX_) == abs(row_ - selected_piece_positionY_)):
            # Valid queen move
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))


def update_bishop_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_bishop') or selected_piece_.startswith('black_bishop'):
        if abs(col_ - selected_piece_positionX_) == abs(row_ - selected_piece_positionY_):
            # Valid bishop move
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))


def update_knight_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_knight') or selected_piece_.startswith('black_knight'):
        if (
                (abs(col_ - selected_piece_positionX_) == 1 and abs(row_ - selected_piece_positionY_) == 2) or
                (abs(col_ - selected_piece_positionX_) == 2 and abs(row_ - selected_piece_positionY_) == 1)
        ):
            # Valid knight move
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))


def update_rook_positions(col_, row_, selected_piece_, selected_piece_positionX_, selected_piece_positionY_):
    if selected_piece_.startswith('white_rook') or selected_piece_.startswith('black_rook'):
        if col_ == selected_piece_positionX_ or row_ == selected_piece_positionY:
            # Valid rook move
            piece_positions[selected_piece_].remove((selected_piece_positionX_, selected_piece_positionY_))
            piece_positions[selected_piece_].append((col_, row_))


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
