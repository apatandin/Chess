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

# piece_rectangles = {}

for color in ['white', 'black']:
    for piece in piece_names:
        piece_images[f'{color}_{piece}'] = pygame.transform.smoothscale(
            pygame.image.load(f'{rep}/{color}_{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE)
        )
        # piece_images[f'{color}_{piece}'].convert()
        # # Draw rectangle around the image
        # piece_rectangles[f'{color}_{piece}'] = piece_images[f'{color}_{piece}'].get_rect()
        # piece_rectangles[f'{color}_{piece}'].center = SQUARE_SIZE // 2, SQUARE_SIZE // 2


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
    piece_image = piece_images[piece_name]
    xx, yy = col_ * SQUARE_SIZE, row_ * SQUARE_SIZE
    screen.blit(piece_image, (xx, yy))


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
                # Remove the piece from its old position
                piece_positions[selected_piece].remove((selected_piece_positionX, selected_piece_positionY))

                # Add the piece to its new position
                piece_positions[selected_piece].append((col, row))

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
