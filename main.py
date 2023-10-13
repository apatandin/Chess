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


def draw_board():
    for row in range(8):
        for col in range(8):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            color = WHITE if (row + col) % 2 == 0 else GREY
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces():
    for piece, positions in piece_positions.items():
        for col, row in positions:
            draw_piece(piece, col, row)


def draw_piece(piece_name, col, row):
    piece_image = piece_images[piece_name]
    x, y = col * SQUARE_SIZE, row * SQUARE_SIZE
    screen.blit(piece_image, (x, y))


# Helper function to check if a move is valid for a pawn
def is_valid_move(start, end, color):
    if start[0] == end[0] and (end[1] - start[1] == 1 or (end[1] - start[1] == 2 and start[1] == 1)):
        if color == "white":
            return all(piece_positions.get(f"white_pawn", []) != [end[0], end[1]]) and all(
                piece_positions.get(f"black_pawn", []) != [end[0], end[1]]
            )
        elif color == "black":
            return all(piece_positions.get(f"black_pawn", []) != [end[0], end[1]]) and all(
                piece_positions.get(f"white_pawn", []) != [end[0], end[1]]
            )
    else:
        return False


# Main game loop
selected_piece = None
dragging = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not dragging:
            # TODO
            pass
            # x, y = pygame.mouse.get_pos()
            # col = x // SQUARE_SIZE
            # row = y // SQUARE_SIZE
            # for piece in piece_positions.keys():
            #     if (col, row) in piece_positions[piece] and piece.startswith("white" if piece[0] == "w" else "black"):
            #         selected_piece = piece
            #         dragging = True
            #         break
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            # TODO
            pass
            # x, y = pygame.mouse.get_pos()
            # col = x // SQUARE_SIZE
            # row = y // SQUARE_SIZE
            # if is_valid_move(piece_positions[selected_piece][0], (col, row), selected_piece.split("_")[0]):
            #     piece_positions[selected_piece] = [(col, row)]
            # else:
            #     col, row = piece_positions[selected_piece][0]
            # selected_piece = None
            # dragging = False

    # screen.fill((0, 0, 0))
    draw_board()
    draw_pieces()

    if dragging and selected_piece:
        x, y = pygame.mouse.get_pos()
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        draw_piece(selected_piece, col, row)

    pygame.display.flip()

# Quit Pygame
pygame.quit()