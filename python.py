import sys, pygame as pg

def is_safe(num, pos, grid, coloured_diagonals):
    # Ellenőrizze, hogy a szám nem ismétlődik-e a sorban és az oszlopban.
    for i in range(6):
        if grid[pos[0]][i] == num or grid[i][pos[1]] == num:
            return False

    # Ellenőrizze a színezett átlókat, ha a pozíció része azoknak.
    for diag_cells in coloured_diagonals.values():
        if pos in diag_cells and num in [grid[x][y] for x, y in diag_cells]:
            return False

    return True

def solve_sudoku(grid, coloured_diagonals):
    # Keressen üres helyet a rácsban.
    empty = find_empty_location(grid)
    # Ha nincs több üres hely, a feladvány megoldódott.
    if not empty:
        return True
    else:
        row, col = empty

    # Próbáljon ki minden lehetséges számot (1-től 6-ig) az adott pozícióban.
    for num in range(1, 7):
        if is_safe(num, (row, col), grid, coloured_diagonals):
            grid[row][col] = num

            # Folytassa a következő üres hely kitöltésével.
            if solve_sudoku(grid, coloured_diagonals):
                return True

            # Ha nem vezetett eredményre, állítsa vissza az aktuális helyet üresre (visszalépés).
            grid[row][col] = 0

    # Ha egyik szám sem működik, térjen vissza a visszalépéssel.
    return False

def find_empty_location(grid):
    # Végigmegy a rács minden celláján és visszaadja az első üres hely pozícióját.
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                return (i, j)
    # Ha nincs üres hely, térjen vissza None-nal.
    return None
#megrajzolja a gridet
def draw_grid():
    #kitölti a képernyőt feketére-> ez adja majd a mezők keretét
    screen.fill(pg.Color("black"))
    for row in range(rows):
        for col in range(cols):
            # megnézzük hogy fő vagy mellék átlóba kerülne-e az adott mező a mivel a ciklus 0-5ig megy így a fő átló kordinátái a (0,0),(1,1),stb tehát ha az x és y koordináta egyenlő, a mellékátlók pedig az (5,0),(4,1), stb. tehát a a két koordináta összege megegyezik a az oszlopok/sorok száma -1 el a 0-tól induló ciklus miatt.
            if (row == col or row+col==5):  # átlók
                color = yellow
            else:

                color = white
            #a mező kalkulált méreténél egy kicsit kisebbett rajzolok hogy a fekete háttér átlátszódjon mellette ezzel adva a keret látszatát
            pg.draw.rect(screen, color, (col * square_size + 1, row * square_size + 1, square_size - 2, square_size - 2))
            #gridbe kiszámolt értékeket vizualizálom a pygame modulal
            number_text=font.render(str(grid[row][col]),True,black)
            #bepozicíionálom a az adott mező közepére a számot
            text_rect = number_text.get_rect(center=((col + 0.5) * square_size, (row + 0.5) * square_size))
            #a vizualizált számot berakja a kiszámolt pozicióba
            screen.blit(number_text, text_rect)
    
    
#maga a fő loop ami nyitva tartja a programot bezárásik
def game_loop():
    for event in pg.event.get():
        if event.type==pg.QUIT: sys.exit()
    draw_grid()
    pg.display.flip()


# A rács definíciója, az előre meghatározott értékekkel.
grid = [
    [0, 0, 6, 0, 0, 4],
    [0, 2, 0, 6, 0, 0],
    [0, 4, 0, 0, 0, 5],
    [2, 0, 0, 0, 6, 0],
    [0, 0, 4, 0, 5, 0],
    [5, 0, 0, 3, 0, 0]
]


# A színezett átlók definíciója, ahol minden átlót egy cellák listájával ábrázolunk.
coloured_diagonals = {
    'main': [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    'anti': [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)]
}
# Indítsa el a Sudoku megoldót, és nyomtassa ki az eredményt.
if solve_sudoku(grid, coloured_diagonals):
    for row in grid:
        print(row)
    pg.init()
    width, height = 600, 600
    screen = pg.display.set_mode((width, height))
    cols, rows = 6, 6
    square_size = width // cols

    yellow = (255, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    font = pg.font.Font(None, 36)
    while 1:
        game_loop()
else:
    print("Nincs megoldás")
