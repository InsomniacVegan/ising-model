# import argparse
import curses
import time
import numpy as np
from modules.ising import IsingModel

# Parse command line documents
# parser = argparse.ArgumentParser(description='An Ising model code for scientific outreach.')
# parser.add_argument('')

# print('Work')


model = IsingModel()
model.update_params(3.5, 0.0)



def main(stdscr):
    curses.curs_set(False)
    stdscr.nodelay(True)
    stdscr.clear()

    while True:
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        stdscr.addstr(0, 0, 'Ising Model Curses Demonstration - Luke Elliott')
        for index, site in np.ndenumerate(model.state_matrix):
            if site == 1:
                txt = '+'
                att = curses.A_BOLD | curses.color_pair(1)

            elif site == -1:
                txt = '-'
                att = curses.A_DIM

            stdscr.addstr((index[-1]+2), (index[0]*2), txt, att)

        stdscr.addstr(28,0, ('T: '+ str(model.temp)))
        stdscr.addstr(29,0, ('H: '+ str(model.ext_field)))
        stdscr.addstr(30,0, ('M: '+str(int(np.sum(model.state_matrix)))))

        stdscr.addstr(32,0, ('UP/DOWN: T +/-'))
        stdscr.addstr(33,0, ('RIGHT/LEFT: H +/-'))
        stdscr.addstr(34,0, ('Q: Quit'))

        time.sleep(0.01)
        stdscr.refresh()

        c = stdscr.getch()
        if c == curses.KEY_UP:
            model.update_params(np.around(model.temp+0.1, 1), model.ext_field)
        elif c == curses.KEY_DOWN:
            if model.temp == 0.1: continue
            model.update_params(np.around(model.temp-0.1,1 ), model.ext_field)
        elif c == curses.KEY_RIGHT:
            model.update_params(model.temp, np.around(model.ext_field+0.1,1))
        elif c == curses.KEY_LEFT:
            model.update_params(model.temp, np.around(model.ext_field-0.1,1))
        elif c == ord('q'):
            exit()

        model.evolve_model()


curses.wrapper(main)