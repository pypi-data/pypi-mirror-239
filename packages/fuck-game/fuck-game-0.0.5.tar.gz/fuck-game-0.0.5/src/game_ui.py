import curses
from curses.textpad import rectangle
import re
import time
import json
import os
from game_level import dispatcher


class GameUI:

    def __init__(self):
        level = 1
        curr_path = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = os.path.join(curr_path, os.path.pardir, 'game.json')
        print(self.conf_path)
        if os.path.exists(self.conf_path):
            with open(self.conf_path, 'r') as f:
                conf = json.load(f)
                level = conf.get('level', 1)
        self.level = level
        self.game_level = dispatcher.get(level)(self)
        self.stdscr = None
        curses.wrapper(self.init_screen)

    
    def init_screen(self, stdscr):
        self.stdscr = stdscr
        
        # Init colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

        try:
            k = 0
            while k != ord('='):
                self.controller(k)
                try:
                    self.refresh_screen()
                except curses.error as e:
                    if str(e) == 'addwstr() returned ERR':
                        raise Exception('Error screen to small')
                    else:
                        raise e
                # level up
                if self.game_level.input_text == 'fuck':
                    self.game_level.end()
                    self.level_up_animation()
                    curses.flushinp()   
                    k = 127
                    self.level += 1
                    dispatcher_key = self.level
                    with open(self.conf_path, 'w') as f:
                        json.dump({'level': self.level}, f)
                    if dispatcher_key not in dispatcher:
                        raise NotImplementedError(f'{dispatcher_key} not implented yet')
                    self.game_level = dispatcher.get(dispatcher_key)(self)
                    continue
                # Wait for next input
                k = self.stdscr.getch()
        except Exception as e:
            self.game_level.end()
            raise e
    
    
    def refresh_screen(self):
        # Initialization
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()
        x_center = int(width / 2)
        y_center = int(height / 2)
        
        # Render rectangle
        rectangle(self.stdscr, y_center-1,x_center-15, y_center+1, x_center+15)
        # Render input text
        start_x_input_text = x_center-15 + 1
        self.stdscr.addstr(y_center, start_x_input_text, self.game_level.input_text)

        # Render info
        info = "Try to write fuck"
        start_x_info= x_center - int(len(info)/2)
        self.stdscr.addstr(y_center+2, start_x_info, info)

        # Render level
        status_bar_str = f'Level {str(self.level).rjust(2)} | Press \'=\' to exit | beta version (dev in progress)'
        self.stdscr.addstr(height-1, 0, status_bar_str)

        # cursor
        self.stdscr.move(y_center, start_x_input_text+len(self.game_level.input_text))

        # Refresh the screen
        self.stdscr.refresh()


    def controller(self, k):
        c = chr(k)

        # Allow input characters
        if re.match(r'[A-Za-z0-9 ,?;.:!]', c):
            c = c.lower()
            self.game_level.on_key_press(c)
            self.refresh_screen()
        # Delete key
        elif k == 127:  
            self.game_level.on_key_del()
            self.refresh_screen()


    def level_up_animation(self):

        height, width = self.stdscr.getmaxyx()
        x_center = int(width / 2)
        y_center = int(height / 2)

        for i in range(15):
            # Turning on attributes for title
            self.stdscr.attron(curses.color_pair(i%2+1))
            # Render rectangle
            rectangle(self.stdscr, y_center-1,x_center-15, y_center+1, x_center+15)
            # Render input text
            start_x_input_text = x_center-15 + 1
            self.stdscr.addstr(y_center, start_x_input_text, self.game_level.input_text)
            # Refresh the screen
            self.stdscr.refresh()
            time.sleep(0.1)
            
        # Clear and refresh the screen for a blank canvas
        self.stdscr.clear()
        self.stdscr.refresh()

        # Turning on attributes for title
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.attron(curses.A_BOLD)

        # make cursor invisible
        curses.curs_set(0)

        # Render input text
        level_up_text = "Level up motherfucker 🖕🖕"
        start_x_level_up_text = x_center-15 + 1
        self.stdscr.addstr(y_center, start_x_level_up_text, level_up_text)

        # Turning off attributes for title
        self.stdscr.attroff(curses.color_pair(2))
        self.stdscr.attroff(curses.A_BOLD)
    
        # Refresh the screen
        self.stdscr.refresh()
        time.sleep(3)

        # make cursor visible
        curses.curs_set(1)