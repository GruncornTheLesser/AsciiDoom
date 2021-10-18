
"""
# sets up windows curses
will pip install windows-curses automatically
contains a Screen class which handles resizing
"""


"""
try:
    from pip._internal import main as _pip_main
except ImportError:
    from pip import main as _pip_main
_pip_main(["install", "windows-curses"])
"""
import curses

class Screen:
    
    def init(): # singleton
        try:
            Screen.scr = curses.initscr() # initiate curses
        except AttributeError as e:
            print("""you are probably trying to run this code from IDLE or similar. python is weird. try running it directly or in vscode??? vscode works for me. you can also try running it from cmd. This is the Error: """)
            print(e)
            print("""its are trying to access a attribute on stdout which is a none type. why is it a none type??? who can know. not me thats for sure""")
            input()
            exit()

        Screen.Height, Screen.Width = Screen.scr.getmaxyx()
        Screen.scr.keypad(True)
        Screen.scr.nodelay(True)
        Screen.scr.timeout(0)

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        curses.start_color()
    
    def terminate():
        curses.reset_shell_mode()

    def Refresh():
        Screen.scr.clear()
        Screen.Height, Screen.Width = Screen.scr.getmaxyx()
        if curses.is_term_resized(Screen.Height, Screen.Width):
            curses.resizeterm(Screen.Height + 1, Screen.Width + 1)

    def SetPixel(x, y, color_pair):
        Screen.scr.addch(y, x, ord(' '), color_pair)

    def RunProgram(main):
        curses.wrapper(main)


