# Draws the main game grid, takes parameters for the surface to draw to, color, x & y position, width, height and cell size
def drawGrid(
        pygame, 
        surface, 
        color: list[int], 
        x: float,
        y: float,
        width: int,
        height: int,
        cell_size: float,
        debug: bool
    ) -> None:

    if debug:
        for i in range(width):
            for j in range(height):
                pygame.draw.rect(
                    surface, 
                    color, 
                    pygame.Rect(
                        2 + x + i * cell_size, 
                        2 + y + j * cell_size, 
                        cell_size - 4, 
                        cell_size - 4
                    ), 
                    1
                )

    pygame.draw.rect(
        surface,
        color,
        pygame.Rect(x, y, cell_size * width, cell_size * height),
        1
    )
