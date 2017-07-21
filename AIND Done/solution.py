assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]


#Naming pards of Sudoku table
rows = 'ABCDEFGHI'
cols = '123456789'

#Getting nacessery parameters used throughout the program
keys = cross(rows, cols)
colums = [cross(rows, num) for num in cols]
rows_ = [cross(num, cols) for num in rows]
squares = [cross(a, b) for a in ('ABC', 'DEF', 'GHI') for b in ('123', '456', '789')]
diag_units = [[rows[i] + cols[i] for i in range(9)], [rows[::-1][i] + cols[i] for i in range(9)]]
unitlist = rows_ + colums + squares + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in keys)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in keys)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    for key in keys:
        #Step 1. : Check if it's 2 char long
        if len(values[key]) == 2:
            #Step 2. : Get it's peers
            part_row = rows_[rows.index(key[0])]
            part_colum = colums[cols.index(key[1])]
            part_sqers = []
            for sqare in squares:
                if key in sqare:
                    part_sqers = sqare
                    break

            row_twin = False
            colum_twin = False
            sqr_twin = False
            for i in range(len(part_row)):
                if part_row[i] != key:
                    if values[part_row[i]] == values[key]:
                        row_twin = True
                if part_colum[i] != key:       
                    if values[part_colum[i]] == values[key]:
                        colum_twin = True
                if part_sqers[i] != key: 
                    if values[part_sqers[i]] == values[key]:
                        sqr_twin = True

            #Now to delete some numbers
            if sqr_twin:
                for i in values[key]:
                    for sqr in part_sqers:
                        if values[sqr] != values[key]:
                            if len(values[sqr]) > 1:
                                values[sqr] = values[sqr].replace(i, "")
            if row_twin:
                for i in values[key]:
                    for row in part_row:
                        if values[row] != values[key]:
                            if len(values[row]) > 1:
                                values[row] = values[row].replace(i, "")

            if colum_twin:
                for i in values[key]:
                    for col in part_colum:
                        if values[col] != values[key]:
                            if len(values[col]) > 1:
                                values[col] = values[col].replace(i, "")


    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """

    nan_value = '123456789'

    # assert len(keys) == len(grid)

    grid_dict = {}
    for key in range(len(keys)):
        if grid[key] == '.':
            # assign_value(grid_dict, keys[key], nan_value)
            grid_dict[keys[key]] = nan_value
        else:
            # assign_value(grid_dict, keys[key], grid[key])
            grid_dict[keys[key]] = grid[key]

    return grid_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in keys)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return



def eliminate(values):
    all_singles = []
    for i in keys:
        if len(values[i]) == 1:
            all_singles.append(i)
    for single in all_singles:
        for peer in peers[single]:
            values = assign_value(values, peer, values[peer].replace(values[single], ""))
    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)

    return values

def reduce_puzzle(values):
    
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        #Use the Naked twin Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)

    if values == False:
        return False

    if all(len(values[box]) == 1 for box in keys):
        return values

    min_value = 9
    min_cell = 'A1'

    for box in keys:
        if len(values[box]) > 1:
            if len(values[box]) < min_value:
                min_value = len(values[box])
                min_cell = box

    for value in values[min_cell]:
        new_vals = values.copy()

        new_vals[min_cell] = value
        try_it = search(new_vals)
        if try_it:
            return try_it


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid = grid_values(grid)
    solved = search(grid)

    return solved
    

if __name__ == '__main__':
    diag_sudoku_grid ='2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
