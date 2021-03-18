import numpy as np, PySimpleGUI as sg

X = 'img/X.png'
X_WIN = 'img/X_WIN.png'
O = 'img/O.png'
O_WIN = 'img/O_WIN.png'
GAME_ICON = 'img/TicTacToe.ico'

GAME_BOARD = None
START_GAME: bool = False
CHECK_FOR_WINNER: bool = False
MAIN_DIAGONAL_IS_WINNER: bool = False
CONTINUE_WITH_NEXT_GAME: str = ''
STEP_COUNTER: int = 0
PLAYER_SWITCH = True

PLAYER1_NAME = ''
PLAYER1_MARKER = 'X'
PLAYER2_NAME = ''
PLAYER2_MARKER = 'O'

ROWS, COLS = (3, 3)
GAME_PROGRESS_ARRAY = [['' for i in range(COLS)] for j in range(ROWS)]
GAME_PROGRESS_ARRAY = np.array(GAME_PROGRESS_ARRAY, dtype=str)

def split(word):
    return [int(char) for char in word]

def progress_game(key: str, player_marker: str):
    
    global GAME_PROGRESS_ARRAY

    continue_with_next_game: str = ''

    row, column = split(key)
    GAME_PROGRESS_ARRAY[row][column] = player_marker

    if CHECK_FOR_WINNER:
        game_won, winning_marker = is_winning()
        if game_won:
            continue_with_next_game = display_winner_and_continue(winning_marker=winning_marker)
        else:
            
            if np.all((GAME_PROGRESS_ARRAY != '')):
                continue_with_next_game = display_winner_and_continue(winning_marker='')

    return continue_with_next_game

def is_row_column_diagonal_complete(row_col_num: int = -1, is_row: bool = True, is_diagonal: bool = False):
    
    is_complete: bool = False

    if is_diagonal is False and row_col_num != -1:
        if is_row:
            row = row_col_num
            is_complete = GAME_PROGRESS_ARRAY[row][0] != '' and \
                          GAME_PROGRESS_ARRAY[row][1] != '' and \
                          GAME_PROGRESS_ARRAY[row][2] != ''
        else:
            col = row_col_num
            is_complete = GAME_PROGRESS_ARRAY[0][col] != '' and \
                          GAME_PROGRESS_ARRAY[1][col] != '' and \
                          GAME_PROGRESS_ARRAY[2][col] != ''
    else:
        if GAME_PROGRESS_ARRAY[0][0] != '' and \
            GAME_PROGRESS_ARRAY[1][1] != '' and \
                GAME_PROGRESS_ARRAY[2][2] != '':
            is_complete = True

        if GAME_PROGRESS_ARRAY[2][0] != '' and \
                GAME_PROGRESS_ARRAY[1][1] != '' and \
                    GAME_PROGRESS_ARRAY[0][2] != '':
            is_complete = True

    return is_complete

def mark_the_winner(row_is_winner: bool, row_column_index: int = -1,
                    diagonal_is_winner: bool = False):

    if not diagonal_is_winner and row_column_index != -1:
        if row_is_winner:
            row = row_column_index
            if GAME_PROGRESS_ARRAY[row][0] == 'X':
                GAME_BOARD.Element(str(row)+str(0)).update(image_filename=X_WIN)
                GAME_BOARD.Element(str(row)+str(1)).update(image_filename=X_WIN)
                GAME_BOARD.Element(str(row)+str(2)).update(image_filename=X_WIN)
            else:
                GAME_BOARD.Element(str(row)+str(0)).update(image_filename=O_WIN)
                GAME_BOARD.Element(str(row)+str(1)).update(image_filename=O_WIN)
                GAME_BOARD.Element(str(row)+str(2)).update(image_filename=O_WIN)
        else:
            col = row_column_index
            if GAME_PROGRESS_ARRAY[0][col] == 'X':
                GAME_BOARD.Element(str(0)+str(col)).update(image_filename=X_WIN)
                GAME_BOARD.Element(str(1)+str(col)).update(image_filename=X_WIN)
                GAME_BOARD.Element(str(2)+str(col)).update(image_filename=X_WIN)
            else:
                GAME_BOARD.Element(str(0)+str(col)).update(image_filename=O_WIN)
                GAME_BOARD.Element(str(1)+str(col)).update(image_filename=O_WIN)
                GAME_BOARD.Element(str(2)+str(col)).update(image_filename=O_WIN)
    else:
        if MAIN_DIAGONAL_IS_WINNER:
            if GAME_PROGRESS_ARRAY[1][1] == 'X':
                GAME_BOARD.Element(str(0)+str(0)).update(image_filename=X_WIN)
                GAME_BOARD.Element(str(1)+str(1)).update(image_filename=X_WIN)
                GAME_BOARD.Element(str(2)+str(2)).update(image_filename=X_WIN)
            else:
                GAME_BOARD.Element(str(0)+str(0)).update(image_filename=O_WIN)
                GAME_BOARD.Element(str(1)+str(1)).update(image_filename=O_WIN)
                GAME_BOARD.Element(str(2)+str(2)).update(image_filename=O_WIN)
        else:
            if GAME_PROGRESS_ARRAY[1][1] == 'X':
                GAME_BOARD.Element(str(0)+str(2)).update(image_filename=X_WIN)
                GAME_BOARD.Element(str(1)+str(1)).update(image_filename=X_WIN)
                GAME_BOARD.Element(str(2)+str(0)).update(image_filename=X_WIN)
            else:
                GAME_BOARD.Element(str(0)+str(2)).update(image_filename=O_WIN)
                GAME_BOARD.Element(str(1)+str(1)).update(image_filename=O_WIN)
                GAME_BOARD.Element(str(2)+str(0)).update(image_filename=O_WIN)

def is_winning():

    global GAME_PROGRESS_ARRAY
    global CHECK_FOR_WINNER
    global MAIN_DIAGONAL_IS_WINNER

    for row in range(ROWS):
        if is_row_column_diagonal_complete(row_col_num=row, is_row=True):
            if GAME_PROGRESS_ARRAY[row][0] == GAME_PROGRESS_ARRAY[row][1] == GAME_PROGRESS_ARRAY[row][2]:
                mark_the_winner(row_is_winner=True, row_column_index=row)
                CHECK_FOR_WINNER = False
                return True, GAME_PROGRESS_ARRAY[row][0]

    for col in range(COLS):
        if is_row_column_diagonal_complete(row_col_num=col, is_row=False):
            if GAME_PROGRESS_ARRAY[0][col] == GAME_PROGRESS_ARRAY[1][col] == GAME_PROGRESS_ARRAY[2][col]:
                mark_the_winner(row_is_winner=False, row_column_index=col)
                CHECK_FOR_WINNER = False
                return True, GAME_PROGRESS_ARRAY[0][col]

    if is_row_column_diagonal_complete(is_diagonal=True):
        if GAME_PROGRESS_ARRAY[0][0] == GAME_PROGRESS_ARRAY[1][1] == GAME_PROGRESS_ARRAY[2][2]:
            MAIN_DIAGONAL_IS_WINNER = True
            mark_the_winner(row_column_index=-1, row_is_winner=False, diagonal_is_winner=True)
            CHECK_FOR_WINNER = False
            return True, GAME_PROGRESS_ARRAY[1][1]

        elif GAME_PROGRESS_ARRAY[2][0] == GAME_PROGRESS_ARRAY[1][1] == GAME_PROGRESS_ARRAY[0][2]:
            mark_the_winner(row_column_index=-1, row_is_winner=False, diagonal_is_winner=True)
            CHECK_FOR_WINNER = False
            return True, GAME_PROGRESS_ARRAY[1][1]

    return False, ''

def display_winner_and_continue(winning_marker: str):

    if winning_marker == PLAYER1_MARKER:
        popup_result = sg.PopupYesNo('The winner is ' + PLAYER1_NAME + '.\nDo you want to play another game with the current players?',
                                     title='Winner!', text_color='white', icon=GAME_ICON, grab_anywhere=True)
    elif winning_marker == PLAYER2_MARKER:
        popup_result = sg.PopupYesNo('The winner is ' + PLAYER2_NAME + '.\nDo you want to play another game with the current players?',
                                     title='Winner!', text_color='white', icon=GAME_ICON, grab_anywhere=True)
    else: # game drawn
        popup_result = sg.PopupYesNo('The Game is drawn.\nDo you want to play another game with the current players?',
                                     title='Drawn!', text_color='white', icon=GAME_ICON, grab_anywhere=True)

    return popup_result

def init_game_window():

    init_game_layout = [[sg.Text('Player X Name: ', size=(12, 1)),
                         sg.InputText('', key='-P1_NAME-')],
                        [sg.Text('Player O Name: ', size=(12, 1)),
                         sg.InputText('', key='-P2_NAME-')],
                        [sg.Button("Start Game", key='-START-'), sg.Button('Exit', key='-EXIT-')]]

    return sg.Window('Tic Tac Toe', init_game_layout, icon=GAME_ICON, finalize=True)

def reset_game_board(reset_board: str):

    global GAME_PROGRESS_ARRAY
    global STEP_COUNTER
    global CONTINUE_WITH_NEXT_GAME
    global CHECK_FOR_WINNER
    global GAME_BOARD
    global PLAYER_SWITCH
    global MAIN_DIAGONAL_IS_WINNER

    if reset_board == 'Yes':
        GAME_BOARD = initialize_game_board()

    GAME_PROGRESS_ARRAY = [['' for i in range(COLS)] for j in range(ROWS)]
    GAME_PROGRESS_ARRAY = np.array(GAME_PROGRESS_ARRAY, dtype=str)
    STEP_COUNTER = 0
    CHECK_FOR_WINNER = False
    CONTINUE_WITH_NEXT_GAME = ''
    PLAYER_SWITCH = True
    MAIN_DIAGONAL_IS_WINNER = False

def start_next_session(user_choice: str):

    global INIT_WINDOW
    global GAME_BOARD

    if user_choice == 'Yes':
        GAME_BOARD.Close()
        GAME_BOARD = None
        reset_game_board(reset_board='Yes')
    elif user_choice == 'No':
        GAME_BOARD.Close()
        GAME_BOARD = None
        reset_game_board(reset_board='No')
        INIT_WINDOW = init_game_window()

def initialize_game_board():

    global PLAYER1_NAME
    global PLAYER1_NAME
    global PLAYER1_MARKER
    global PLAYER2_MARKER

    GAME_BOARD_LAYOUT = [[sg.Text('Player X: ' + PLAYER1_NAME, key='-P1-', text_color='red')],
                        [sg.Text('Player O: ' + PLAYER2_NAME, key='-P2-', text_color='white')],
                        [sg.Text('')]]

    GAME_BOARD_LAYOUT += [[sg.Button(' ', size=(8, 4), key=str(j)+str(i))
                            for i in range(3)] for j in range(3)]

    GAME_BOARD_LAYOUT += [[sg.Button("Reset Game", key="-RESET-", tooltip='Resets the current session.')]]

    BOARD = sg.Window('Tic Tac Toe', GAME_BOARD_LAYOUT, icon=GAME_ICON, finalize=True)

    BOARD.TKroot.protocol("WM_DESTROY_WINDOW", lambda: BOARD.write_event_value("WIN_CLOSE", ()))
    BOARD.TKroot.protocol("WM_DELETE_WINDOW", lambda: BOARD.write_event_value("WIN_CLOSE", ()))

    return BOARD

GAME_BOARD = None
INIT_WINDOW = init_game_window()

while True:

    WINDOW, EVENT, VALUES = sg.read_all_windows()

    if EVENT in (sg.WIN_CLOSED, '-EXIT-') and WINDOW == INIT_WINDOW:
        break

    if EVENT == '-START-' and not GAME_BOARD:

        if VALUES['-P1_NAME-'] == '' or VALUES['-P2_NAME-'] == '':
            sg.popup_ok("Error. Please enter both the players name before proceeding.",
                        title='Tic Tac Toe', icon=GAME_ICON)

        else:
            PLAYER1_NAME, PLAYER2_NAME = VALUES['-P1_NAME-'], VALUES['-P2_NAME-']
            
            if EVENT == '-START-':
                if VALUES['-P1_NAME-'] is not None and VALUES['-P2_NAME-'] is not None:
                    START_GAME = True
                    INIT_WINDOW.close()
                    GAME_BOARD = initialize_game_board()

    if WINDOW == GAME_BOARD and (EVENT in ('WIN_CLOSE', '-EXIT-')):
        GAME_BOARD.close()
        GAME_BOARD = None
        INIT_WINDOW = init_game_window()

    if START_GAME and EVENT != '-RESET-':

        if EVENT not in ('-START-', 'WIN_CLOSE', '-EXIT-'):

            CURRENT_MARKER = GAME_BOARD.Element(EVENT).get_text()
            GAME_BOARD.Element(EVENT).update(PLAYER1_MARKER if CURRENT_MARKER == ' ' and\
                                             PLAYER_SWITCH is True else PLAYER2_MARKER if CURRENT_MARKER == ' ' and\
                                             PLAYER_SWITCH is False else PLAYER1_MARKER if CURRENT_MARKER == PLAYER1_MARKER
                                             else PLAYER2_MARKER if CURRENT_MARKER == PLAYER2_MARKER else ' ')

            if GAME_BOARD.Element(EVENT).get_text() == PLAYER1_MARKER:
                STEP_COUNTER += 1
                PLAYER_SWITCH = False

                GAME_BOARD.Element('-P1-').update(text_color='white')
                GAME_BOARD.Element('-P2-').update(text_color='red')

                if PLAYER1_MARKER == 'X':
                    GAME_BOARD.Element(EVENT).update(image_filename=X)
                else:
                    GAME_BOARD.Element(EVENT).update(image_filename=O)

                GAME_BOARD.Element(EVENT).update(disabled=True)

                CONTINUE_WITH_NEXT_GAME = progress_game(EVENT, PLAYER1_MARKER)

                start_next_session(CONTINUE_WITH_NEXT_GAME)

            elif GAME_BOARD.Element(EVENT).get_text() == PLAYER2_MARKER:
                STEP_COUNTER += 1
                PLAYER_SWITCH = True

                GAME_BOARD.Element('-P1-').update(text_color='red')
                GAME_BOARD.Element('-P2-').update(text_color='white')

                if PLAYER2_MARKER == 'X':
                    GAME_BOARD.Element(EVENT).update(image_filename=X)
                else:
                    GAME_BOARD.Element(EVENT).update(image_filename=O)

                GAME_BOARD.Element(EVENT).update(disabled=True)

                CONTINUE_WITH_NEXT_GAME = progress_game(EVENT, PLAYER2_MARKER)

                start_next_session(CONTINUE_WITH_NEXT_GAME)

            if STEP_COUNTER == 4:
                CHECK_FOR_WINNER = True

    if EVENT == '-RESET-' and WINDOW == GAME_BOARD:
        RESET_GAME = sg.popup_yes_no('Do you want to reset the current board?',
                                     title='Game Reset', icon=GAME_ICON, grab_anywhere=True)
        if RESET_GAME == 'Yes':
            GAME_BOARD.Close()
            GAME_BOARD = None
            reset_game_board(reset_board='Yes')