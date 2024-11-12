from uib_inf100_graphics.event_app import run_app
import copy

### 
#   START APP.
###
def app_started(app, rows=20, cols=20,START_FPS=1):
    #Number of rows/cols.
    app.num_rows = rows
    app.num_cols = cols
    app.timer_delay = int(1000/(START_FPS))

    #For placing new blocks.
    app.new_block_indicies = [0,0]

    #Generate grid.
    app.grid = []
    for col_i in range(cols):
        row = []
        for row_i in range(rows):
            row.append(False)
        app.grid.append(row)
    #If running.
    app.running = False


###
#   PLACING NEW BLOCKS.
### 
def mouse_click_grid_indicies(app,event):
    x = event.x
    y = event.y
    # As the grid fills the entire screen (at all times), one can use this with number of cols/rows to get indicies.
    row_index = int(((y / app.height)*app.num_rows)//1)
    col_index = int(((x / app.width)*app.num_cols)//1)
    return [col_index, row_index]

def mouse_pressed(app, event):
    indicies = mouse_click_grid_indicies(app,event)
    app.grid[indicies[0]][indicies[1]]=not app.grid[indicies[0]][indicies[1]]



###
#   PAUSING AND UNPAUSING SIMULATION.
###
def key_pressed(app, event):
    if event.key =="Space":
        app.running=not app.running
    elif event.key == "r":
        app_started(app, app.num_rows, app.num_cols)


###
#   UPDATE EACH FRAME.
###
def redraw_all(app, canvas):
    CELL_SIZE_X = app.width/app.num_cols
    CELL_SIZE_Y = app.height/app.num_rows

    #Go through all cells.
    for column_i in range(app.num_cols):
        for row_i, cell_state in enumerate(app.grid[column_i]):
            #Filling.
            fill = "black" if cell_state else "white"
            #Drawing the cells.
            canvas.create_rectangle(
                column_i*CELL_SIZE_X
                ,row_i*CELL_SIZE_Y
                ,(column_i+1)*CELL_SIZE_X,
                (row_i+1)*CELL_SIZE_Y,
                fill=fill)
    canvas.create_text(150,20,text=f"Space to pause/unpause. (Currently {"running" if app.running else "paused"})", font="Consolas", fill="blue")
    canvas.create_text(110,50,text="Left click to spawn/delete cell.", font="Consolas", fill="blue")


def timer_fired(app):
    update(app)


def update(app):
    if not app.running:
        return 
    next_grid = copy.deepcopy(app.grid)
    #Go through all cells.
    for col_index, col in enumerate(next_grid):
        for row_index, row in enumerate(col):
            cell_indicies = [col_index,row_index]
            next_grid[col_index][row_index] = next_state_cell_conway_rules(app,cell_indicies)        
    app.grid = next_grid



###
#   CONWAY'S GAME OF LIFE.
###
def get_cell_neighbour_count(app, indicies):
    col_index = indicies[0]
    row_index = indicies[1]
    
    num_neighbours = 0

    # Go through all in the nine cell chunk
    for cell_col_i in range(col_index-1, col_index+2):
        for cell_row_i in range(row_index-1, row_index+2):

            # If "neighbour" cell is outside the grid -> continue.
            if not ((0<=cell_col_i<app.num_cols) and (0<=cell_row_i<app.num_rows)):
                continue

            # Check if "neighbour" cell is current cell -> continue.
            if indicies == [cell_col_i,cell_row_i]:
                continue

            #If cell.
            if app.grid[cell_col_i][cell_row_i]==True:
                num_neighbours+=1

    return num_neighbours



def next_state_cell_conway_rules(app, indicies):
    num_neighbours = get_cell_neighbour_count(app, indicies)
    col_index, row_index = indicies
    current_state = app.grid[col_index][row_index]

    # Reproduction or Survival
    if num_neighbours == 3 or (current_state and num_neighbours == 2):
        return True
        
    # Death
    return False


###
#   START PROJECT.
###
if __name__ == "__main__":
    run_app(width=1280,height=720)