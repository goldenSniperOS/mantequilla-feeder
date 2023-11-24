from m5stack import *
from m5ui import *
from uiflow import *
import ntptime
import time
import machine
import urequests
from easyIO import *


setScreenColor(0x111111)


duty_from = None
duty_to = None
Time = None
DUTY_OPENED = None
DUTY_CLOSED = None
direction = None
i = None



circle0 = M5Circle(39, 80, 10, 0x111111, 0x111111)
label0 = M5TextBox(0, 144, "B", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label1 = M5TextBox(0, 0, "H", lcd.FONT_Default, 0xFFFFFF, rotate=0)


# Describe this function...
def feed():
  global duty_from, duty_to, Time, DUTY_OPENED, DUTY_CLOSED, direction, i, PWM0
  move_from_to(DUTY_CLOSED, DUTY_OPENED)
  wait(3)
  move_from_to(DUTY_OPENED, DUTY_CLOSED)
  send_telegram_notification()

def upRange(start, stop, step):
  while start <= stop:
    yield start
    start += abs(step)

def downRange(start, stop, step):
  while start >= stop:
    yield start
    start -= abs(step)

# Describe this function...
def move_from_to(duty_from, duty_to):
  global Time, DUTY_OPENED, DUTY_CLOSED, direction, i, PWM0
  if duty_from > duty_to:
    direction = -1
  else:
    direction = 1
  for i in (float(duty_from) <= float(duty_to)) and upRange(float(duty_from), float(duty_to), float(direction)) or downRange(float(duty_from), float(duty_to), float(direction)):
    PWM0.duty(i)
    wait_ms(100)

# Describe this function...
def send_telegram_notification():
  global duty_from, duty_to, Time, DUTY_OPENED, DUTY_CLOSED, direction, i, PWM0
  circle0.setBgColor(0xff9966)
  circle0.setBorderColor(0xff9966)
  try:
    req = urequests.request(method='POST', url='https://api.telegram.org/bot6434050040:AAGvN066o1xnTGWN1HjSV8TyS-fiwsYZSGI/sendMessage',json={'chat_id':'-4009263944','text':((str('Mantequilla correctamente alimentada a las : ') + str((ntp.formatTime(':')))))}, headers={})
    circle0.setBgColor(0x33ff33)
    circle0.setBorderColor(0x33ff33)
    gc.collect()
    req.close()
  except:
    circle0.setBorderColor(0xff0000)
    circle0.setBgColor(0xff0000)

# Describe this function...
def checkAlarm():
  global duty_from, duty_to, Time, DUTY_OPENED, DUTY_CLOSED, direction, i, PWM0
  Time = ntp.formatTime(':')
  if Time == '06:30:00' or Time == '10:30:00' or Time == '14:30:00' or Time == '19:00:00':
    feed()

# Describe this function...
def show_screen():
  global duty_from, duty_to, Time, DUTY_OPENED, DUTY_CLOSED, direction, i, PWM0
  axp.setLcdBrightness(100)
  wait(3)
  axp.setLcdBrightness(0)


def buttonA_wasPressed():
  global Time, DUTY_OPENED, DUTY_CLOSED, direction, duty_from, duty_to, i, PWM0
  feed()
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  global Time, DUTY_OPENED, DUTY_CLOSED, direction, duty_from, duty_to, i, PWM0
  show_screen()
  pass
btnB.wasPressed(buttonB_wasPressed)


ntp = ntptime.client(host='cn.pool.ntp.org', timezone=(-5))
DUTY_OPENED = 7
DUTY_CLOSED = 12
PWM0 = machine.PWM(26, freq=50, duty=DUTY_CLOSED, timer=0)
show_screen()
while True:
  label0.setText(str((str('%') + str((map_value((axp.getBatVoltage()), 3.7, 4.1, 0, 100))))))
  label1.setText(str(ntp.formatTime(':')))
  checkAlarm()
  wait_ms(2)
