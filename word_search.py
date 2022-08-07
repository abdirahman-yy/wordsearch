'''
Abdirahman Mohamed's Word Search Project that generates a pseudo-random 2D grid of characters such 
that user inputted words can be found in the generated grid

'''

import random
import string
import copy
import math


RIGHT = (1, 0)
DOWN = (0, 1)
RIGHT_DOWN = (1, 1)
RIGHT_UP = (1, -1)
DIRECTIONS = (RIGHT, DOWN, RIGHT_DOWN, RIGHT_UP)

def get_size(grid):
    ''' this function takes in a letter grid (list) and returns a tuple of width and height (in that order) '''
    return (len(grid[0]), len(grid))

def print_word_grid(grid):
    ''' this function takes in a letter grid (list) and prints out the grid (string)'''
    for i in range(len(grid)):
        print(''.join(grid[i]))

def copy_word_grid(grid):
    ''' this function simply copies the grid for later use '''
    copy_grid = []
    for i in range(len(grid)):
        copy_grid.append(grid[i].copy())
    return copy_grid

def extract(grid, position, direction, max_len):
    ''' this function takes in 4 parameters: the grid list, the positon of the first word, the direction we are moving, and the max_len of movement. 
    from there we try to derive the form using simple addition of elements in tuple to get, while simultaneously adding to the string output for each letter we hit. 
    we return a string in the end '''
    str_output = ''
    #location
    x = position[1]
    y = position[0]
    #5.1 handling try and accept python
    try: 
        for i in range(max_len):
            if x == -1 or y == -1:
                return str_output
            else:
                str_output += grid[x][y]
                x += direction[1]
                y += direction[0]
        return str_output
    except IndexError:
        return str_output

def show_solution(grid, word, solution):
    ''' this function check if solution is false; if not, it moves through a grid copy changing each letter it hits to be in all_CAPS '''
    if solution == False:
        word = word.lower()
        print(str(word) + ' is not found in this word search')
    else:
        print(str(word).upper() + ' can be found as below')
        copy = copy_word_grid(grid)
        x = solution[0][1]
        y = solution[0][0]
        for i in range(len(word)):
            copy[x][y] = copy[x][y].upper()
            x += solution[1][1]
            y += solution[1][0]
        print_word_grid(copy)

def find(grid, word):
    size_tuple = get_size(grid)
    #write a for loop to get the amount of time we want to check i.e. height * length
    x = 0
    y = 0
    tracker_tuple = (x,y)
    #(size_tuple[0] + 1 * size_tuple[1] +1)-1 --> means the each possible location
    for i in range(((size_tuple[0]) * (size_tuple[1]))):
        word_right = extract(grid, tracker_tuple, RIGHT, len(word))
        word_down = extract(grid, tracker_tuple, DOWN, len(word))
        word_right_down = extract(grid, tracker_tuple, RIGHT_DOWN, len(word))
        word_right_up = extract(grid, tracker_tuple, RIGHT_UP, len(word))
        if word_right == word:
            return (tracker_tuple, RIGHT)
        elif word_down == word:
            return (tracker_tuple, DOWN)
        elif word_right_down == word:
            return (tracker_tuple, RIGHT_DOWN)
        elif word_right_up == word:
            return (tracker_tuple, RIGHT_UP)
        else:
            if y == 4:
                x += 1
                y = 0
                tracker_tuple = (x,y)
            elif x > 4:
                x = 0
                tracker_tuple = (x,y)
            else:
                y += 1
                tracker_tuple = (x,y)
    return False

def find_all(grid, list_of_words):
    word_dict = {}
    for i in range(len(list_of_words)):
        find_tuple = find(grid, list_of_words[i])
        word_dict[list_of_words[i]] = find_tuple
    return word_dict

def generate(width, height, words):
    ''' 
    This function returns a tuple with two elements. The first element is a letter grid composed of lower-case English
    letters with the correct width and height (as per the two parameters) The second element is list of words that
    were actually put into the letter grid 
    '''
    grid = [["." for i in range(width)] for j in range(height)]

    # directions
    RIGHT = (1, 0)
    DOWN = (0, 1)
    RIGHT_DOWN = (1, 1)
    RIGHT_UP = (1, -1)

    # list of directions
    directions = [RIGHT, DOWN, RIGHT_DOWN, RIGHT_UP]

    # locations
    positions = []

    for i in range(0, height):
        for x in range(0, width):
            positions.append((x, i))
    placed_words = []
    for word in words:
        if find(grid, word) == False:
            for i in range(5):
                direction = random.choice(directions)
                position = random.choice(positions)

                placement = extract(grid, position, direction, len(word))
                placement_list = [x for x in placement]
                if len(placement) == len(word) and len(set(placement_list)) == 1:
                    placed_words.append(word)
                    # print(grid, position, direction)
                    n = 0
                    while n < len(word):
                        if (
                            position[1] == len(grid)
                            or position[0] == len(grid[1])
                            or position[0] == -1
                            or position[1] == -1
                        ):
                            break
                        elif direction == RIGHT:
                            grid[position[1]][position[0]] = word[n]
                            position = (position[0] + 1, position[1])
                            n = n + 1
                        elif direction == RIGHT_UP:
                            grid[position[1]][position[0]] = word[n]
                            position = (position[0] + 1, position[1] - 1)
                            n = n + 1
                        elif direction == DOWN:
                            grid[position[1]][position[0]] = word[n]
                            position = (position[0], position[1] + 1)
                            n = n + 1
                        elif direction == RIGHT_DOWN:
                            grid[position[1]][position[0]] = word[n]
                            position = (position[0] + 1, position[1] + 1)
                            n = n + 1
                else:
                    continue
                break
        else:
            continue

    for i in range(0, height):
        for w in range(0, width):
            if grid[i][x] == ".":
                grid[i][x] = random.choice(string.ascii_letters).lower()

    return grid, placed_words


# Driver program
if __name__ == "__main__":
    grid, placed_words = generate(6, 6, ["dog", "den", "wolf"])
    print_word_grid(grid)
    print("Correctly placed words:", placed_words)