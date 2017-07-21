assignments = []

def cross(A, B):
    """
    This method is used to create all necessary lists for sudoku problem.
        Args: A, B are two strings

        Outputs: List made of pairs of characters made with cross product of elements in A and B
    """
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

#Setting all params that we will need
rows = 'ABCDEFGHI'
cols = '123456789'

#Getting values for all our boxes
boxes = cross(rows, cols)
assert  len(boxes) == 81

#Getting values for rows, diags, colums, squares
rows_units = [cross(row, cols) for row in rows]
cols_units = [cross(rows, number) for number in cols]
square_units = [cross(a, b) for a in ('ABC', 'DEF', 'GHI') for b in ('123', '456', '789')]
diags_units = [[rows[i] + cols[i] for i in range(9)], [rows[8-i] + cols[i] for i in reversed(range(9))]]

#Units list used to incorporate constraints
#NOTE: If we want to do diagonal sudoku we are adding here diag units as well
#      by adding this term we are adding more constraints to our agent
unitlist = rows_units + cols_units + square_units + diags_units
#Adding just those units in which we have appearance of looked box
units = {box: [unit for unit in unitlist if box in unit] for box in boxes}
#Cleaning those units and creating peers.
#Use of set is to assure that we have unique peers 
peers = {box: set(sum(units[box],[])) - set([box]) for box in boxes}

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

        Outputs:
            The resulting sudoku in dictionary form.
    """

    ######################################
    #First implementation of Naked twins.
    # This implementation is faster of 0.01s !
    ######################################
    # for key in boxes:
    #     #Checking if the lenght of box is 2
    #     if len(values[key]) == 2:
    #         #Getting peers from box which has lenght of 2
    #         part_row = rows_units[rows.index(key[0])]
    #         part_colum = cols_units[cols.index(key[1])]
    #         part_sqers = []
    #         for sqare in square_units:
    #             if key in sqare:
    #                 part_sqers = sqare
    #                 break

    #         #setting our detection booleans to False
    #         row_twin = False
    #         colum_twin = False
    #         sqr_twin = False
    #         #going through colums, rows ans squares which we consider as peers and checking if twin exist in each of these
    #         for i in range(len(part_row)):
    #             if part_row[i] != key:
    #                 if values[part_row[i]] == values[key]:
    #                     row_twin = True
    #             if part_colum[i] != key:       
    #                 if values[part_colum[i]] == values[key]:
    #                     colum_twin = True
    #             if part_sqers[i] != key: 
    #                 if values[part_sqers[i]] == values[key]:
    #                     sqr_twin = True

    #         #Now to delete some numbers
    #         #if we detect twins in squares
    #         if sqr_twin:
    #             #for each digit in the value of our twins
    #             for i in values[key]:
    #                 #going through all boxes in square with twins
    #                 for sqr in part_sqers:
    #                     if values[sqr] != values[key]:
    #                         #Important: we don't want to delete that digit from boxes which lenght is one
    #                         if len(values[sqr]) > 1:
    #                             values = assign_value(values, sqr, values[sqr].replace(i, ""))
            
    #         #if we detect twins in rows
    #         if row_twin:
    #             #for each digit in the value of our twins
    #             for i in values[key]:
    #                 #going through all boxes in row with twins
    #                 for row in part_row:
    #                     if values[row] != values[key]:
    #                         #Important: we don't want to delete that digit from boxes which lenght is one
    #                         if len(values[row]) > 1:
    #                             values = assign_value(values, row, values[row].replace(i, ""))

    #         #if we detect twins in colums
    #         if colum_twin:
    #             #for each digit in the value of our twins
    #             for i in values[key]:
    #                 #going through all boxes in colum with twins
    #                 for col in part_colum:
    #                     if values[col] != values[key]:
    #                         #Important: we don't want to delete that digit from boxes which lenght is one
    #                         if len(values[col]) > 1:
    #                             values = assign_value(values, col, values[col].replace(i, ""))


    ######################################
    #Second implementation of Naked twins.#
    ######################################
    #Going through each unit in the table [Unit == row, colum, square, diagonal]
    for unit in unitlist:
        #For each box in that unit
        for box in unit:
            #going through other boxes in the current unit
            for other_boxes in unit:
                #Check if we are NOT looking at the same box as we started with
                if box != other_boxes:
                    #For naked twins strategy we should have just 2 values possible
                    if len(values[box]) == 2:
                        #Here we check if we have the twin in the unit
                        if values[box] == values[other_boxes]:
                            #for each digit in the twin we are deleting it from other boxes in the unit
                            for digit in values[box]:
                                for u in unit:
                                    #check if the box from which we are deleting digits is not one of twins
                                    if u != box and u != other_boxes:
                                        values = assign_value(values, u, values[u].replace(digit, ''))

    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
        Args:
            grid(string) - A grid in string form.
        Outputs:
            A grid in dictionary form
                Keys: The boxes, e.g., 'A1'
                Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    #This value will be placed to boxes which have dot (boxes for which we don't know the value yet)
    nan_value = '123456789'

    assert len(grid) == len(boxes)
    values_dict = {}

    for i in range(len(grid)):
        #Check if the value is '.'
        if grid[i] == '.':
            values_dict[boxes[i]] =  nan_value
        else:
            values_dict[boxes[i]] = grid[i]

    return values_dict


def display(values):
    """
    Display the values as a 2-D grid.
        Args:
            values(dict): The sudoku in dictionary form
    """
    #Calculating width depending on longest number through out boxes
    width = 1+max(len(values[s]) for s in boxes)
    #For creting separating line printed after 3rd and 6th line
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        #Statement for printing boxes and separation line after 3rd and 6th number
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
        Args: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
    #Going through all the boxes in our table
    for box in boxes:
        #getting peer of current box 
        current_peers = peers[box]
        #getting value of the current box
        value = values[box]
        #if the value of the current box is 'fixed' or it lenght is one
        if len(value) == 1:
            #deleting that number from all boxes considered as peers for the current box
            for pr in current_peers:
                values = assign_value(values, pr, values[pr].replace(value, ""))

    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
        Args: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
    #Going through all units
    for unit in unitlist:
        #Going through each possible digit used in sudoku
        for digit in '123456789':
            #getting all boxes that have current digit in current unit
            dplaces = [box for box in unit if digit in values[box]]
            #If there is only one box using that number in a possible results
            if len(dplaces) == 1:
                #setting new value of that box to be the current digit
                values = assign_value(values, dplaces[0], digit)

    return values

def reduce_puzzle(values):
    """
    For current setup of sudoku table, trying to reduce number of possible on each of boxes to one using sudoku strategies.

        Args: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
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
    """
    Using depth-first search and propagation, try all possible values.
    
        Args: A sudoku in dictionary form.

        Output: 1. False - if there is no possible result
                2. Solved sudoku table in dictionary form
    """
    
    values = reduce_puzzle(values)

    #case that we cannot solve sudoku, and return false as a result
    if values == False:
        return False

    #If lenght of values in all boxes are one, we solved sudoku and return that result
    if all(len(values[box])== 1 for box in boxes):
        return values

    #Setting starting min value and box with the min value
    min_value = 9
    min_box = 'A1'

    #looping through boxes and changing global min value also position of the box with the min value
    for box in boxes:
        #We are not considering boxes with lenght of one (just one number in them)
        if len(values[box]) > 1:
            if len(values[box]) < min_value:
                min_value = len(values[box])
                min_box = box

    #Magic of Deep-first search algorith, recursion
    #Looping through each number in value which is in min_box
    for val in values[min_box]:
        #Creating copy of our table
        new_vals = values.copy()
        #Setting digit from min_box to be new value of 
        new_vals[min_box] = val
        #trying to solve sudoku with new setup by calling search function recursively
        try_to_solve = search(new_vals)
        if try_to_solve:
            return try_to_solve

def solve(grid):
    """
    Find the solution to a Sudoku grid.
        Args:
            grid(string): a string representing a sudoku grid.
                Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        Outputs:
            The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #geting dict for input values
    grid = grid_values(grid)
    #solving sudoku
    solved = search(grid)

    return solved

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
