from math import floor
# from servo import Servo
from time import sleep
from monomepi128 import Monome, Button, ButtonHandler

BPM = 120
STEP_TIME = '10'    # in milliseconds
STEP_AMT = '1'
RIGHT_X = '5'
RIGHT_Y = '7'
LEFT_X = '2'
LEFT_Y = '7'
SWEEP_X = '4'
SWEEP_Y = '7'
EXIT_X = 'f'
EXIT_Y = '7'


def check_if_exit(monome):
    if monome.get_led(EXIT_X, EXIT_Y) == '1':
        monome.call_exit()
    return monome.exit_flag


def do_sweep(monome):
    if monome.get_led(SWEEP_X, SWEEP_Y) == '1':
        return True
    else:
        return False


def do_left(monome):
    if monome.get_led(RIGHT_X, RIGHT_Y) == '1':
        return True
    else:
        return False


def do_right(monome):
    if monome.get_led(LEFT_X, LEFT_Y) == '1':
        return True
    else:
        return False


def step_left(servo):
    if int(servo.currentpos) < int(servo.maxpos):
        step = [(str(int(servo.currentpos) + int(STEP_AMT)), STEP_TIME)]
        servo.move(step)
        led_animate(m, servo)


def step_right(servo):
    if int(servo.currentpos) >= 0:
        step = [(str(int(servo.currentpos) - int(STEP_AMT)), STEP_TIME)]
        servo.move(step)
        led_animate(m, servo)


def led_animate(monome, servo):
    lin = round((int(servo.currentpos) / 4), 0)
    loc_x = int(int(lin) % 8)
    loc_y = int(floor(int(lin) / 8))
    # print 'LOC: ' + str(loc_x) + ',' + str(loc_y) + '   ' + servo.currentpos
    for y in range(7):
        for x in range(8):
            if (x == loc_x) and (y == loc_y):
                if monome.get_led(str(x), str(y)) == '0':
                    monome.set_led('11', str(x), str(y))
            else:
                if monome.get_led(str(x), str(y)) == '1':
                    monome.set_led('10', str(x), str(y))

# INIT
#
# a = Servo('COM5')
# a.open_servo()

m = Monome('/dev/ttyUSB0')

# Make all buttons toggle buttons
buttons = []
for xbutt in range(16):
    for ybutt in range(8):
        buttons.append(Button(m, int(xbutt), int(ybutt), 'toggle'))

m.open_serial()
button_thread = ButtonHandler(m, buttons)
button_thread.start()


# MAIN
#
# led_animate(m, a)
col = 0
prevcol = 0
enabled_rows = []

while not check_if_exit(m):

    # Light up column and reset previous column LEDs
    m.set_col(str(format(int(col), '01x')), 'FF')
    for row in enabled_rows:
        m.set_led_nostate('11', str(format(prevcol, '01x')), str(row))

    # Delay (based on BPM)
    sleep(float(60) / float(BPM))

    # Store current column's LED states
    enabled_rows = []
    for row in range(8):
        if m.get_led(str(format(col, '01x')), str(row)) == '1':
            enabled_rows.append(row)

    # Turn off column LEDs and move to next
    m.set_col(str(format(int(col), '01x')), '00')
    prevcol = col
    col = (col + 1) % 16


# EXIT
#
sleep(1)
m.close_serial()
# a.reset()
# a.close()


# motions = [('70','100'), ('50','250'), ('80','200'), ('40','250'),
#            ('90','500'), ('30','300'), ('100','1000'), ('20','500'),
#            ('110','1000'), ('10','1200')]
# motions = [('0','500'), ('60','500'), ('120','500')]
# a.move(motions)
# sleep(5)
# a.reset()
# a.move([('20','500')])

# print "Done."