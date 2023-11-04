from machine import Pin, SPI, Timer, ADC
from micropython import const
import framebuf
from config import *
import random, string
from picozero import LED, Button, Buzzer
import max7219
_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)
import time, urandom
buzzer = Buzzer(BUZZER_PIN)
ldr = ADC(Pin(LDR_PIN))
xAxis = ADC(Pin(JOY_X))
yAxis = ADC(Pin(JOY_Y))
button = Button(JOY_SW)
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(MATRIX_CLK), mosi=Pin(MATRIX_DIN))
ss = Pin(MATRIX_CS, Pin.OUT)
xValue = 0
yValue = 0
timer_lock=False
left = False
right = False
up = False
down = False
def timer_tick(timer):
    global xValue, yValue, timer_lock
    if(timer_lock):
        return
    timer_lock=True
    Config.xValue = xAxis.read_u16()
    Config.yValue = yAxis.read_u16()
    if Config.xValue > 60000: #60000
        Config.last_debounce_time = time.ticks_ms() # If the logic level has changed, reset the debounce timer
        Config.left = True
        Config.right = False
        Config.up = False
        Config.down = False
        Config.power_on=False
    if Config.xValue < 600: #600
        Config.last_debounce_time = time.ticks_ms() # If the logic level has changed, reset the debounce timer
        Config.left = False
        Config.right = True
        Config.up = False
        Config.down = False
        Config.power_on=False
    if Config.yValue < 600: #60000
        Config.last_debounce_time = time.ticks_ms() # If the logic level has changed, reset the debounce timer
        Config.left = False
        Config.right = False
        Config.up = True
        Config.down = False
        Config.power_on=False
    if Config.yValue > 60000: #600
        Config.last_debounce_time = time.ticks_ms() # If the logic level has changed, reset the debounce timer
        Config.left = False
        Config.right = False
        Config.up = False
        Config.down = True
        Config.power_on=False
    timer_lock=False
timer = Timer(period=100, mode=Timer.PERIODIC, callback=timer_tick)
left_button = Button(LEFT_BUTTON_PIN)
right_button = Button(RIGHT_BUTTON_PIN)
up_button = Button(UP_BUTTON_PIN)
down_button = Button(DOWN_BUTTON_PIN)
def beep(t=0.1):
    global buzzer
    buzzer = Buzzer(BUZZER_PIN)
    buzzer.on()
    time.sleep(0.1)
    buzzer.off()
button_lock=False
def left_button_pressed():
    global button_lock
    Config.power_on=False
    if button_lock:
        return
    button_lock=True
    print("Left button pressed")
    show("Left")
    button_lock=False
def right_button_pressed():
    global button_lock
    Config.power_on=False
    if button_lock:
        return
    button_lock=True
    print("Right button pressed")
    show("Right")
    button_lock=False
def up_button_pressed():
    global button_lock
    Config.power_on=False
    if button_lock:
        return
    button_lock=True
    print("Up button pressed")
    show("Up")
    button_lock=False
def down_button_pressed():
    Config.power_on=False
    global button_lock
    if button_lock:
        return
    button_lock=True
    print("Down button pressed")
    button_lock=False
def button_pressed():
    if time.ticks_diff(time.ticks_ms(), Config.last_debounce_time) > DEBOUNCE_DELAY:
        if Config.left or Config.right or Config.up or Config.down or Config.button_pressed:
            print("Restting Joystick")
            Config.left = False
            Config.right = False
            Config.up = False
            Config.down = False
            Config.button_pressed = False
            return
    Config.power_on=False
    global button_lock #, MENU_INDEX, menu_selected
    if button_lock:
        return
    button_lock=True
    print("Button pressed " + Config.menu_index)
    Config.selected_menu_index=Config.menu_index
    Config.button_pressed=True
    Config.last_debounce_time = time.ticks_ms()
    button_lock=False
left_button.when_pressed = left_button_pressed
right_button.when_pressed = right_button_pressed
up_button.when_pressed = up_button_pressed
down_button.when_pressed = down_button_pressed
button.when_pressed = button_pressed
def menu_reset():
    import uos
    beep()
    try:
        uos.remove("menu.txt")
    except OSError:
        pass
    try:
        uos.remove("menu_index.txt")
    except OSError:
        pass
    time.sleep(1)
    print("Menu reset")
    while any_button():
        buttons_reset()
        time.sleep(0.2)
    buttons_reset()
    print("Menu reset return")
def factory_reset():
    import uos
    time.sleep(0.2)
    beep()
    while any_button():
        buttons_reset()
        time.sleep(0.2)
    while True:
        scroll("Factory reset? up=yes down=no")
        time.sleep(0.5)
        if Config.up:
            print("Resetting...")
            for filename in uos.listdir():
                if filename.endswith('.txt'):
                    uos.remove(filename)
                    print(f"Deleted: {filename}")
                if filename.startswith('project_L'):
                    uos.remove(filename)
                    print(f"Deleted: {filename}")
            beep(5)
            break
        if Config.down:
            print("Not resetting...")
            break
        time.sleep(0.2)
    buttons_reset()
def any_button():
    if Config.left or Config.right or Config.up or Config.down or Config.button_pressed:
        return True
    return False
def buttons_reset():
    Config.left = False
    Config.right = False
    Config.up = False
    Config.down = False
    Config.button_pressed=False
    time.sleep(1)
def display_reset():
    global display
    display = max7219.Matrix8x8(spi, ss, 4)
    display.brightness(MATRIX_BRIGHTNESS)
    display.fill(0)
    display.show()
def self_test():
    beep()
    display_bitmap(all_on,0)
    display_bitmap(all_on,8)
    display_bitmap(all_on,16)
    display_bitmap(all_on,24)
    time.sleep(2)
    beep()
    display_bitmap(all_off,0)
    display_bitmap(all_off,8)
    display_bitmap(all_off,16)
    display_bitmap(all_off,24)
    time.sleep(2)
    display_reset()
    beep()
    display_bitmap(all_on,0)
    display_bitmap(all_on,8)
    display_bitmap(all_on,16)
    display_bitmap(all_on,24)
    time.sleep(2)
    beep()
    display_bitmap(all_off,0)
    display_bitmap(all_off,8)
    display_bitmap(all_off,16)
    display_bitmap(all_off,24)
    time.sleep(2)
    display_reset()
    beep()
    display_bitmap(all_on,0)
    display_bitmap(all_on,8)
    display_bitmap(all_on,16)
    display_bitmap(all_on,24)
    time.sleep(2)
    beep()
    display_bitmap(all_off,0)
    display_bitmap(all_off,8)
    display_bitmap(all_off,16)
    display_bitmap(all_off,24)
    time.sleep(2)
    display_reset()
    beep()
    display_bitmap(all_on,0)
    display_bitmap(all_on,8)
    display_bitmap(all_on,16)
    display_bitmap(all_on,24)
    time.sleep(2)
    beep()
    display_bitmap(all_off,0)
    display_bitmap(all_off,8)
    display_bitmap(all_off,16)
    display_bitmap(all_off,24)
    time.sleep(2)
    display_reset()
    beep()
    L304_LightMeter()
    show(" Up ")
    while True:
        if Config.up:
            time.sleep(0.2)
            Config.up = False
            beep()
            break
    show(" Up ")
    while True:
        if Config.up:
            time.sleep(0.2)
            Config.up = False
            beep()
            break
    show("Down ")
    while True:
        if Config.down:
            time.sleep(0.2)
            Config.down = False
            beep()
            break
    show("--->")
    while True:
        if Config.right:
            time.sleep(0.2)
            Config.right = False
            beep()
            break
    show("<---")
    while True:
        if Config.left:
            time.sleep(0.2)
            Config.left = False
            beep()
            break
display_reset()
def az0018(n): #n is already a STRING
    with open('menu.txt', 'w') as file:
        file.write(n)   #str(n))
def load_menu():
    try:
        with open('menu.txt', 'r') as file:
            n = file.read()
    except OSError:
        n = "L000" #START
    return n
def save_menu_index(n): #n is already a STRING!
    with open('menu_index.txt', 'w') as file:
        file.write(n)    #str(n))
def load_menu_index():
    try:
        with open('menu_index.txt', 'r') as file:
            n = file.read()
    except OSError:
        n = "" #EMPTY STRING TO START WITH
    return n
def show(message):
    display_reset()
    display.text(message, 0, 0, 1)
    display.show()
    if FLIP_DISPLAY:
        show_flipped()
    else:
        show_normal()
def scroll(scrolling_message,need_up=False, need_down=False, need_left=False, need_right=False, need_pressed=False):
    display_reset()
    length = len(scrolling_message)
    column = (length * 8)
    for x in range(32, -column, -1):  
        display.fill(0)
        display.text(scrolling_message,x,0,1)
        display.show()
        time.sleep(SCROLL_SPEED)
        if need_pressed and Config.button_pressed: #or Config.right
            print("Scroll pressed")
            beep()
            while any_button():
                buttons_reset()
                time.sleep(0.2)
            Config.button_pressed = True
            break
        if need_left and Config.left: #or Config.right
            beep()
            while any_button():
                buttons_reset()
                time.sleep(0.2)
            Config.left = True
            break
        if need_right and Config.right: #or Config.right
            beep()
            while any_button():
                buttons_reset()
                time.sleep(0.2)
            Config.right = True
            break
        if need_up and Config.up: #or Config.right
            beep()
            while any_button():
                buttons_reset()
                time.sleep(0.2)
            Config.up = True
            break
        if need_down and Config.down: #or Config.right
            beep()
            while any_button():
                buttons_reset()
                time.sleep(0.2)
            Config.down = True
            break
        if Config.left or Config.button_pressed: #or Config.right
            beep()
            while any_button():
                buttons_reset()
                time.sleep(0.2)
            break
def show_normal():
    for y in range(8):
        display.cs(0)
        for m in range(display.num):
            display.spi.write(bytearray([_DIGIT0 + y, display.buffer[(y * display.num) + m]]))
        display.cs(1)
def show_flipped():
    for y in range(8):
        display.cs(0)
        for m in range(display.num):
            byte = display.buffer[(y * display.num) + m]
            byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
            byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
            byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
            display.spi.write(bytearray([_DIGIT0 + y, byte]))
        display.cs(1)
def set_pixel(x, y, value):
        """
        Set the value of a specific pixel at coordinates (x, y).
        :param x: X-coordinate (0-7)
        :param y: Y-coordinate (0-7)
        :param value: 0 for off, 1 for on
        """
        if 0 <= x < 8 * 4 and 0 <= y < 8:
            display.framebuf.pixel(x, y, value)
def display_bitmap(bitmap_data,column):
    for row, data in enumerate(bitmap_data):
        for col in range(32):
            pixel2 = (data >> col) & 0x01
            set_pixel(col+column, row, pixel2)
    display.show()
def display_row(value, row):
    for col in range(32):
        set_pixel(col, row, value)
    display.show()
def display_col(value, col):
    for row in range(8):
        set_pixel(col, row, value)
    display.show()
def az0001():
    pass
def welcome():
    ob = False
    try:
        print("TRY - OB")
        az0001()
    except:
        print("TRY - OB - EXCEPT")
        ob = False
    else:
        print("TRY - OB - ELSE")
        ob = True
    if not ob:
        beep()
        time.sleep(0.5)
        beep()
        time.sleep(0.5)
        beep()
        time.sleep(0.5)
        scroll("Yes.. do run ob, speed: " + str(SCROLL_SPEED))        
    scroll(Config.welcome + " " + Config.version)
def L102_Car():
    previous_high_score = read_file("abhi_car.txt")
    az0003 = 3  # Car's vertical position (0 or 1)
    az0016 = 0  # Obstacle's vertical position (0 to 2)
    obstacle_x = 31  # Initial horizontal position of the obstacle
    score = 0
    az0017 = []  # List to store active az0017
    az0011 = False
    current_score = 0 #Sree
    def az0006(position):
        display.fill(0)
        display.pixel(0, position, 1)
        display.pixel(0, position + 1, 1)
        display.pixel(1, position, 1)
        display.pixel(1, position + 1, 1)
        display.pixel(2, position, 1)
        display.pixel(2, position + 1, 1)
        display.show()
    def az0007(x, position, length, width):
        obstacle_length = random.randint(2, 3)
        for i in range(length):
            display.pixel(x, position + i, 1)
            for j in range(width):
                display.pixel(x+j, position + i, 1)
        display.show()
    def az0004():
        for obstacle in az0017:
            if (az0003 <= obstacle[1] <= az0003 + 1) and obstacle[0] <= 3:
                return True
        return False
    while not az0011:
        if Config.up:  # Button for moving up
            az0003 = max(0, az0003 - 1)
            time.sleep(0.2) #Sree
            Config.up = False
        if Config.down:  # Button for moving down
            az0003 = min(6, az0003 + 1)
            time.sleep(0.2) #Sree
            Config.down = False
        az0017 = [(x - 1, y, length, width) for x, y, length, width in az0017 if x > 0]
        if random.random() < 0.1:
            az0017.append((obstacle_x, random.randint(0, 7), 1, random.randint(2, 3)))
        if az0004():
            az0011 = True
            az0007(obstacle_x, az0016, 1, random.randint(2, 3))  # Show the collision obstacle
            beep()
            time.sleep(0.5)
            beep()
            time.sleep(0.5)
            beep()
            time.sleep(0.5)
            beep()
            time.sleep(0.5)
            beep()
            current_score=score*10
        else:
            az0006(az0003)
            for obstacle in az0017:
                az0007(obstacle[0], obstacle[1], obstacle[2], obstacle[3])
                if obstacle[0] == 0:
                    beep()
                    score += 1
        time.sleep(0.2)  # Adjust the speed of the game
        if Config.left:
            az0011 = True
            break
    while any_button():
        buttons_reset()
        time.sleep(0.2)
    if (current_score > previous_high_score):
        print("NEW HIGH SCORE")
        write_to_file("abhi_car.txt", current_score)
        scroll("Game Over. Your Score: " + str(current_score) + " New High Score!!! ")
    else:
        scroll("Game Over. Your Score: " + str(current_score) + " - High Score: " + str(previous_high_score))
    print("Ending Car 1")
    Config.left = True
    print("Ending Car 2")
snake=[]
def write_to_file(file_name,file_content):
    with open(file_name, "w") as file:
        file.write(str(file_content))  # Convert to string if it's an integer
def write_string_to_file(file_name,file_content):
    with open(file_name, "w") as file:
        file.write(file_content)  # Convert to string if it's an integer
def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            data_read = file.read()
            int_data_read = int(data_read)
    except OSError:
        int_data_read = 0
    return int_data_read
def read_string_from_file(file_name):
    try:
        with open(file_name, "r") as file:
            data_read = file.read()
    except OSError:
        data_read = ""
    return data_read
def az0012():
    global snake
    while True:
        x = random.randint(0, 30)
        y = random.randint(0, 7)
        if (x, y) not in snake:
            return x, y
def L101_Snake():
    global snake
    filename = "abhi.txt"
    previous_high_score = read_file(filename)
    print("Previous High Score:", previous_high_score)
    snake = [(4, 4)]  # Initial position of the Snake
    az0019 = (1, 0)  # Initial direction (right)
    food = (22, 3)  # Initial position of the food
    az0011 = False
    head_visible = True  # Initialize as visible
    blink_interval = 500  # Adjust as needed (e.g., 500 milliseconds)
    last_blink_time = time.ticks_ms()
    blink_counter = 0  # Number of blinks
    while not az0011:
        if blink_counter == 0:
            az0020 = (-10,-10)
            if Config.right:
                Config.right = False
                az0020 = (snake[0][0] + 1, snake[0][1] + 0)
                if (len(snake) > 1 and az0020 == snake[1]):
                    continue
                az0019 = (1, 0)
            elif Config.left:
                Config.left = False
                az0020 = (snake[0][0] - 1, snake[0][1] + 0)
                if (len(snake) > 1 and az0020 == snake[1]):
                    continue
                az0019 = (-1, 0)
            elif Config.up:
                Config.up = False
                az0020 = (snake[0][0] + 0, snake[0][1] - 1)
                if (len(snake) > 1 and az0020 == snake[1]):
                    continue
                az0019 = (0, -1)
            elif Config.down:
                Config.down = False
                az0020 = (snake[0][0] + 0, snake[0][1] + 1)
                if (len(snake) > 1 and az0020 == snake[1]):
                    continue
                az0019 = (0, 1)
            az0014 = (snake[0][0] + az0019[0], snake[0][1] + az0019[1])
            if (
                az0014[0] < 0
                or az0014[0] > 31
                or az0014[1] < 0
                or az0014[1] > 7
                or az0014 in snake[2:]
            ):
                az0011 = True
                continue
            if az0014 == food:
                beep()
                snake.insert(0, az0014)
                food = az0012()
            else:
                snake.insert(0, az0014)
                snake.pop()
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_blink_time) >= blink_interval:
            last_blink_time = current_time
            head_visible = not head_visible
        blink_counter += 1
        display_reset()
        if head_visible:
            display.pixel(snake[0][0], snake[0][1], 1)
        for segment in snake[1:]:
            display.pixel(segment[0], segment[1], 1)
        display.pixel(food[0], food[1], 1)
        display.show()
        if blink_counter >= 8:
            head_visible = True  # Ensure the head is visible
            blink_counter = 0
        time.sleep(0.1)
        if Config.button_pressed: 					# Back
            print("Breaking snake")
            az0011 = True
    display_reset()
    while any_button():
        buttons_reset()
        time.sleep(0.2)
    current_score=len(snake) * 10
    if (current_score > previous_high_score):
        print("NEW HIGH SCORE")
        beep()
        beep()
        beep()
        scroll("Game Over. Your Score: " + str(current_score) + " New High Score!!! ")
        write_to_file(filename, current_score)
    else:
        beep()
        beep()
        scroll("Game Over. Your Score: " + str(current_score) + " - High Score: " + str(previous_high_score))
    Config.left = True
    print("Exiting snake")
def showMenu(m):
    first_time=True
    if m in menu:
        menu_keys=sorted(menu[m])
    else:
        return m
    if Config.menu_index in menu_keys:
        Config.menu_key_index = menu_keys.index(Config.menu_index)
    else:
        Config.menu_key_index = 0
    prev_menu=""
    counter=0
    az0018(m)
    while True:
        if Config.down:
            first_time = False
            Config.menu_key_index = Config.menu_key_index+1
            if Config.menu_key_index>(len(menu_keys)-1):
                Config.menu_key_index = 0
            time.sleep(0.5)
            Config.down = False
        if Config.up:
            first_time = False
            Config.menu_key_index = Config.menu_key_index-1
            if Config.menu_key_index==-1:
                Config.menu_key_index = len(menu_keys)-1
            time.sleep(0.5)
            Config.up = False
        Config.menu_index = menu_keys[Config.menu_key_index]
        if prev_menu=="" or prev_menu!=Config.menu_index:
            show(Config.menu_index)
            prev_menu=Config.menu_index
            counter=0
        if counter > 10 and m=="L000" and first_time:
            scroll(Config.help_text)
            counter=0
            show(Config.menu_index)
        if counter > 10 or Config.right:
            scroll(Config.menu_index+ " " + menu[m][Config.menu_index])
            show(Config.menu_index)
            counter=0
            first_time = False
            Config.right = False
        if Config.power_on and Config.menu_index in auto_run:
            print("AUTO_RUN")
            Config.power_on = False
            Config.program_menu = m
            run_it()
            show(Config.menu_index)
        if Config.button_pressed:
            first_time = False
            Config.button_pressed=False
            save_menu_index(Config.menu_index)
            if Config.menu_index not in menu:
                print("Trying to run: " + Config.menu_index)
                Config.program_menu = m
                run_it()
                show(Config.menu_index)
            else:
                print("Not running: " + Config.menu_index)
                return Config.menu_index
        if Config.left: 					# Back
            first_time = False
            Config.left=False
            number = int(Config.menu_index.replace("L", ""))
            balance = number % 100
            if balance>0:
                balance=balance-1 # THIS IS POSITION TO THE CORRECT TOP LEVEL MENU eg back from 202 goes to 200
            rounded_number = (number // 100) * 100
            Config.menu_index = "L"+f"{rounded_number:03}"
            time.sleep(0.2)
            Config.left=False
            return "L000"
        time.sleep(0.1)
        counter = counter+0.1
    return n
def L104_AZ():
    random.seed(Config.xValue)
    letter = random.choice(string.ascii_uppercase)
    show(letter)   
    while True:
         if Config.button_pressed:
            letter = random.choice(string.ascii_uppercase)
            show(letter)
            time.sleep(0.2)
            Config.button_pressed=False
         if Config.left: 					# Back
            break
         time.sleep(0.2)
def L103_16():
    random.seed(Config.xValue)
    number = random.randint(1, 6)
    show(str(number))  
    while True:
         if Config.button_pressed:
            number = random.randint(1, 6)
            show(str(number))
            beep()
            time.sleep(0.2)
            Config.button_pressed=False
         if Config.left: 					# Back
            break
         time.sleep(0.2)
def L105_Timer():
    number = 60
    while True:
         if number <= 0:
             show("Done")
             beep(0.5)
         else:
             show(str(number))
         if Config.button_pressed:
            number = 60
            show(str(number))
            beep()
            time.sleep(0.2)
            Config.button_pressed=False
         if Config.left: 					# Back
            break
         number = number - 1
         time.sleep(1)
def L106_StopWatch():
    number = 0
    started=True
    while True:
         if not started:
            scroll(str(number) + " Seconds")
         if Config.button_pressed:
            if started:
                beep(0.5)
                started=False
            else:
                number = 0
                started = True
                beep()
            Config.button_pressed = False
         if started:
             show(str(number))
             number = number + 1
         if Config.left: 					# Back
            Config.button_pressed=False
            break
         time.sleep(1)
def L217_BoomBox():
    while True:  # Main loop for the animation
        display_reset()
        print("Reset")
        for col in range(32):  # Loop through all 32 columns (0-31)
            value = random.randint(0, 7)  # Generate a random 8-bit value for the column
            for row in range(8):
                value1=0
                if value<=row:
                    value1=1
                set_pixel(col, row, value1)
        display.show()
        time.sleep(0.07)
        if Config.left: 					# Back
            break 
def L218_MoveADot():
    x, y = 16, 4
    display_reset()
    while True:
        if Config.up and y > 0:
            set_pixel(x, y, 0) #old led
            y -= 1
            time.sleep(0.5)
            Config.up = False
        if Config.down and y < 7:
            set_pixel(x, y, 0) #old led
            y += 1
            time.sleep(0.5)
            Config.down = False
        if Config.left and x > 0:
            set_pixel(x, y, 0) #old led
            x -= 1
            time.sleep(0.5)
            Config.left = False
        else:
            if Config.left and x == 0: #left end
                scroll("Left end, exiting!")
                break
        if Config.right and x < 31:
            set_pixel(x, y, 0) #old led
            x += 1
            time.sleep(0.5)
            Config.right = False
        set_pixel(x, y, 1) #new led
        display.show()
        time.sleep(0.5)
        if Config.button_pressed: 					# Back
            break
    Config.left = True
    Config.button_pressed = False
def L219_MoveADotAround():
    col = 0
    row = 0
    while True:
        set_pixel(col, row, 1)
        display.show()
        time.sleep(0.1)
        set_pixel(col, row, 0)
        display.show()
        if col < 31 and row == 0:
            col += 1
        elif col == 31 and row < 7:
            row += 1
        elif col > 0 and row == 7:
            col -= 1
        elif col == 0 and row > 0:
            row -= 1
        else:
            break
        if Config.left: 					# Back
            break
    Config.left = True
    Config.button_pressed = False
def L220_CountryCapital():
    current_country = urandom.choice(list(countries_and_capitals.keys()))
    while True:
        scroll(f"Country: {current_country}", need_left=True, need_up=True, need_down=True, need_right=True, need_pressed=True)
        if Config.up or Config.down:
            print("Up/Down")
            Config.up = False
            Config.down = False
            current_country = urandom.choice(list(countries_and_capitals.keys()))
            beep(0.8)
            scroll(f"Next Country: {current_country}", need_left=True, need_up=True, need_down=True, need_right=True, need_pressed=True)
        if Config.right or Config.button_pressed:
            print("Press/Right")
            Config.right = False
            Config.button_pressed = False
            beep()
            scroll(f"Capital is: {countries_and_capitals[current_country]}", need_left=True, need_up=True, need_down=True, need_right=True, need_pressed=True)
        time.sleep(1)
        if Config.left:
            time.sleep(0.2)
            Config.button_pressed = False
            Config.left = False
            break
def L221_WordOpposite():
    current_word = urandom.choice(list(opposites_dict.keys()))
    while True:
        scroll(f"Word: {current_word.upper()}", need_left=True, need_up=True, need_down=True, need_right=True, need_pressed=True)
        if Config.up or Config.down:
            Config.up = False
            Config.down = False
            current_word = urandom.choice(list(opposites_dict.keys()))
            beep(0.8)
            scroll(f"Next Word: {current_word.upper()}", need_left=True, need_up=True, need_down=True, need_right=True, need_pressed=True)
        if Config.right or Config.button_pressed:
            Config.right = False
            Config.button_pressed = False
            beep()
            scroll(f"Opposite is: {opposites_dict[current_word].upper()}", need_left=True, need_up=True, need_down=True, need_right=True, need_pressed=True)
        time.sleep(1)
        if Config.left:
            Config.button_pressed = False
            break
def L108_PartyQuiz():
    l108_filename = "L108_partyquiz.txt"
    l108_previous_high_score = read_file(l108_filename)
    l108_current_score = 0
    buttons_reset()
    az0015 = True
    msg=""
    random.seed(Config.xValue)
    while True:
        if az0015:
            az0015 = False
            qa_pair = random.choice(questions_and_answers)
            print("NEXT:")
            print(qa_pair)
            question = qa_pair["question"]
            correct_answer = qa_pair["answer"]
            az0009 = qa_pair["az0009"]
            fake_answer = random.choice(az0009)
            if random.randint(1, 2)==1:
                fake_answer=correct_answer
            msg=question + " IS IT: " + fake_answer +"?"
            time.sleep(0.2)
            Config.up = False
            Config.down = False
        scroll(msg, need_up = True, need_down = True, need_left = True)
        if Config.up:  # correct
            Config.up = False
            display_reset()
            if fake_answer == correct_answer:
                scroll("VERY GOOD!", need_up = True, need_down = True, need_left = True)
                beep()
                l108_current_score = l108_current_score+1
                print("A CUR SCORE = " + str(l108_current_score))
            else:
                scroll("SORRY NO!! IT IS: " + correct_answer, need_up = True, need_down = True, need_left = True)
                beep()
                time.sleep(0.2)
                beep()
            time.sleep(0.2)
            az0015 = True
        elif Config.down:  # WRONG
            Config.down = False
            display_reset()
            if fake_answer != correct_answer:
                beep()
                scroll("VERY GOOD! IT IS: " + correct_answer, need_up = True, need_down = True, need_left = True)
                l108_current_score = l108_current_score+1
                print("A CUR SCORE = " + str(l108_current_score))
            else:
                beep()
                time.sleep(0.2)
                beep()
                scroll("SORRY " + correct_answer + " IS CORRECT!", need_up = True, need_down = True, need_left = True)
            time.sleep(0.2)
            az0015 = True
        time.sleep(0.2)  # To avoid button debouncing issues
        if Config.left:  # Assuming "left" button quits the game
            time.sleep(0.2)
            buttons_reset()
            print("CUR SCORE = " + str(l108_current_score))
            l108_current_score= l108_current_score * 10
            if (l108_current_score > l108_previous_high_score):
                print("NEW HIGH SCORE")
                beep()
                beep()
                beep()
                scroll("Game Over. Your Score: " + str(l108_current_score) + " New High Score!!! ")
                write_to_file(l108_filename, l108_current_score)
            else:
                beep()
                beep()
                scroll("Game Over. Your Score: " + str(l108_current_score) + " - High Score: " + str(l108_previous_high_score))
            Config.left = True
            break
def L109_IndiaQuiz():
    l109_filename = "L109_mentalmath.txt"
    l109_previous_high_score = read_file(l109_filename)
    l109_current_score = 0
    buttons_reset()
    az0015 = True
    msg=""
    random.seed(Config.xValue)
    while True:
        if az0015:
            az0015 = False
            qa_pair = random.choice(indian_states_questions_and_answers)
            print("NEXT:")
            print(qa_pair)
            question = qa_pair["question"]
            correct_answer = qa_pair["answer"]
            az0009 = qa_pair["az0009"]
            fake_answer = random.choice(az0009)
            if random.randint(1, 2)==1:
                fake_answer=correct_answer
            msg=question + " IS IT: " + fake_answer +"?"
            time.sleep(0.2)
            Config.up = False
            Config.down = False
        scroll(msg, need_up = True, need_down = True, need_left = True)
        if Config.up:  # correct
            Config.up = False
            display_reset()
            if fake_answer == correct_answer:
                scroll("VERY GOOD!", need_up = True, need_down = True, need_left = True)
                beep()
                l109_current_score = l109_current_score+1
                print("A CUR SCORE = " + str(l109_current_score))
            else:
                scroll("SORRY NO!! IT IS: " + correct_answer, need_up = True, need_down = True, need_left = True)
                beep()
                time.sleep(0.2)
                beep()
            time.sleep(0.2)
            az0015 = True
        elif Config.down:  # WRONG
            Config.down = False
            display_reset()
            if fake_answer != correct_answer:
                beep()
                scroll("VERY GOOD! IT IS: " + correct_answer, need_up = True, need_down = True, need_left = True)
                l109_current_score = l109_current_score+1
                print("A CUR SCORE = " + str(l109_current_score))
            else:
                beep()
                time.sleep(0.2)
                beep()
                scroll("SORRY " + correct_answer + " IS CORRECT!", need_up = True, need_down = True, need_left = True)
            time.sleep(0.2)
            az0015 = True
        time.sleep(0.2)  # To avoid button debouncing issues
        if Config.left:  # Assuming "left" button quits the game
            time.sleep(0.2)
            buttons_reset()
            print("CUR SCORE = " + str(l109_current_score))
            l109_current_score= l109_current_score * 10
            if (l109_current_score > l109_previous_high_score):
                print("NEW HIGH SCORE")
                beep()
                beep()
                beep()
                scroll("Game Over. Your Score: " + str(l109_current_score) + " New High Score!!! ")
                write_to_file(l109_filename, l109_current_score)
            else:
                beep()
                beep()
                scroll("Game Over. Your Score: " + str(l109_current_score) + " - High Score: " + str(l109_previous_high_score))
            Config.left = True
            break
def L107_MentalMath():
    l07_filename = "107_mentalmath.txt"
    l07_previous_high_score = read_file(l07_filename)
    l07_current_score = 0
    buttons_reset()
    az0015=True
    while True:
        if az0015:
            az0015 = False
            operators = ['+', '-']
            op = random.choice(operators)
            num1 = random.randint(1, 9)
            num2 = random.randint(1, 9)
            if random.randint(1, 2)==1:
                if op == '/':
                    if num1<num2:
                        x=num1
                        num1=num2
                        num2=x
                    x=num1%num2
                    num1=num1-x
                if op == '-':
                    if num1<num2:
                        x=num1
                        num1=num2
                        num2=x
                question = f"{num1}{op}{num2}"
            else:
                if op == '/':
                    if num2<num1:
                        x=num2
                        num2=num1
                        num1=x
                    x=num2%num1
                    num2=num2-x
                if op == '-':
                    if num2<num1:
                        x=num2
                        num2=num1
                        num1=x
                question = f"{num2}{op}{num1}"
            answer = int(eval(question))
            x = random.randint(-1, 1)
            if answer+x <0:
                fake_answer = int(answer + random.randint(0, 2))
            else:
                fake_answer = int(answer + x)
        scroll(f"Is {question} = {fake_answer}?", need_up=True, need_down=True, need_left=True)
        if Config.up: # Button is pressed
            if fake_answer == answer:
                show("GOOD")
                l07_current_score = l07_current_score+1
                print("A CUR SCORE = " + str(l07_current_score))
                beep()
            else:
                show("NO!!")
                beep()
                time.sleep(0.2)
                beep()
            time.sleep(0.2)
            Config.up=False
            az0015=True
            continue
        elif Config.down: # Button is pressed
            if fake_answer != answer:
                show("GOOD")
                l07_current_score = l07_current_score+1
                print("B CUR SCORE = " + str(l07_current_score))
                beep()
            else:
                show("NO!!")
                beep()
                time.sleep(0.2)
                beep()
            time.sleep(0.2)
            Config.down=False
            az0015=True
            continue
        time.sleep(0.2) # To avoid button debouncing issues
        if Config.left:
            time.sleep(0.2)
            buttons_reset()
            print("CUR SCORE = " + str(l07_current_score))
            l07_current_score= l07_current_score * 10
            if (l07_current_score > l07_previous_high_score):
                print("NEW HIGH SCORE")
                beep()
                beep()
                beep()
                scroll("Game Over. Your Score: " + str(l07_current_score) + " New High Score!!! ")
                write_to_file(l07_filename, l07_current_score)
            else:
                beep()
                beep()
                scroll("Game Over. Your Score: " + str(l07_current_score) + " - High Score: " + str(l07_previous_high_score))
            Config.left = True
            Config.button_pressed = False
            break        
def L222_MentalMath():
    l222_filename = "222_mentalmath.txt"
    l222_previous_high_score = read_file(l222_filename)
    l222_current_score = 0
    buttons_reset()
    az0015=True
    while True:
        if az0015:
            az0015 = False
            operators = ['+', '-', '*', '/']
            op = random.choice(operators)
            num1 = random.randint(1, 9)
            num2 = random.randint(1, 9)
            if random.randint(1, 2)==1:
                if op == '/':
                    if num1<num2:
                        x=num1
                        num1=num2
                        num2=x
                    x=num1%num2
                    num1=num1-x
                if op == '-':
                    if num1<num2:
                        x=num1
                        num1=num2
                        num2=x
                question = f"{num1}{op}{num2}"
            else:
                if op == '/':
                    if num2<num1:
                        x=num2
                        num2=num1
                        num1=x
                    x=num2%num1
                    num2=num2-x
                if op == '-':
                    if num2<num1:
                        x=num2
                        num2=num1
                        num1=x
                question = f"{num2}{op}{num1}"
            answer = int(eval(question))
            x = random.randint(-1, 1)
            if answer+x <0:
                fake_answer = int(answer + random.randint(0, 2))
            else:
                fake_answer = int(answer + x)
        scroll(f"Is {question} = {fake_answer}?", need_up=True, need_down=True, need_left=True)
        if Config.up: # Button is pressed
            if fake_answer == answer:
                show("GOOD")
                l222_current_score = l222_current_score+1
                print("A CUR SCORE = " + str(l222_current_score))
                beep()
            else:
                show("NO!!")
                beep()
                time.sleep(0.2)
                beep()
            time.sleep(0.2)
            Config.up=False
            az0015=True
        elif Config.down: # Button is pressed
            if fake_answer != answer:
                show("GOOD")
                beep()
                l222_current_score = l222_current_score+1
                print("A CUR SCORE = " + str(l222_current_score))
            else:
                show("NO!!")
                beep()
                time.sleep(0.2)
                beep()
            time.sleep(0.2)
            Config.down=False
            az0015=True
        time.sleep(1) # To avoid button debouncing issues
        if Config.left:
            time.sleep(0.2)
            buttons_reset()
            print("CUR SCORE = " + str(l222_current_score))
            l222_current_score= l222_current_score * 10
            if (l222_current_score > l222_previous_high_score):
                print("NEW HIGH SCORE")
                beep()
                beep()
                beep()
                scroll("Game Over. Your Score: " + str(l222_current_score) + " New High Score!!! ")
                write_to_file(l222_filename, l222_current_score)
            else:
                beep()
                beep()
                scroll("Game Over. Your Score: " + str(l222_current_score) + " - High Score: " + str(l222_previous_high_score))
            Config.left = True
            Config.button_pressed = False
            break        
def L223_Tambola():
    generated_numbers = set()
    first_time=True
    while True:
        if Config.button_pressed or Config.right or first_time:
            time.sleep(0.2)
            first_time=False
            Config.button_pressed = False
            Config.right = False
            while True:
                new_number = random.randint(0, 99)
                if new_number not in generated_numbers:
                    break
            generated_numbers.add(new_number)
            show(f"{new_number:02d}")
            beep()
            time.sleep(0.2)
            Config.button_pressed = False
            Config.right = False        
        time.sleep(0.01)
        if len(generated_numbers) == 100:
            scroll("All numbers have been generated!")
            time.sleep(1)
            Config.left=True
            break  # or you can reset generated_numbers and continue
        if Config.left:
            Config.button_pressed = False
            break        
def L110_Greetings():
    current_greeting_index = read_file("greetings_index.txt") #0
    while True:
         scroll(greetings[current_greeting_index], need_down=True, need_up=True, need_left=True)
         if Config.down:
             Config.down = False
             current_greeting_index += 1
             if current_greeting_index == len(greetings):
                 current_greeting_index = 0
             scroll(greetings[current_greeting_index], need_down=True, need_up=True, need_left=True)
             write_to_file("greetings_index.txt", current_greeting_index)
         if Config.up:
             Config.up = False
             current_greeting_index -= 1
             if current_greeting_index < 0:
                 current_greeting_index = len(greetings) - 1
             scroll(greetings[current_greeting_index], need_down=True, need_up=True, need_left=True)
             write_to_file("greetings_index.txt", current_greeting_index)
         if Config.left: 					# Back
            Config.button_pressed=False
            break
         time.sleep(0.2)
def L213_Shooting():
    display_reset()
    az0002 = 0
    bullet_y = random.randint(0, 7)  # Assume bullet starts at row 3 (adjust as needed)
    display.pixel(az0002, bullet_y, 1)
    display.show()
    print("START SHOOTING")
    while True:
        if Config.button_pressed:  # Check the flag
            time.sleep(0.2)
            buttons_reset()
            az0002 = 0
            display.pixel(az0002, bullet_y, 1)
            display.show()
            while az0002 < 32:  # 32 columns across 4 8x8 segments
                display.pixel(az0002, bullet_y, 0)  # Clear previous position
                az0002 += 1
                display.pixel(az0002, bullet_y, 1)  # Light up new position
                display.show()
                time.sleep(0.05)  # Adjust speed as needed
            beep()  # Call the beep function when bullet reaches the end
            display.pixel(az0002, bullet_y, 0)
            display.show()
            Config.button_pressed = False
            az0002 = 0
            bullet_y = random.randint(0, 7)  # Assume bullet starts at row 3 (adjust as needed)
            display.pixel(az0002, bullet_y, 1)
            display.show()
        if Config.left: 					# Back
            time.sleep(0.2)
            Config.button_pressed=False
            Config.left=False
            print("END SHOOTING")
            break
        time.sleep(0.2)
def L214_RandomFill():
    print("L214 start")
    while True:
        display_reset()
        for x in range(32):  # 32 columns across 4 8x8 segments
            for y in range(8):  # 8 rows
                pixel_value = urandom.randint(0, 1)  # Either 0 or 1
                display.pixel(x, y, pixel_value)
                display.show()
                time.sleep(0.1)
                if Config.left:
                    print("Left1")
                    Config.left=True
                    break
            if Config.left:
                print("Left2")
                Config.left=True
                break
        if Config.left:
            print("Left3")
            time.sleep(0.2) # Back
            Config.left=False
            break
    print("L214 end")
def L215_SpiralFill():
    while True:
        display_reset()
        top_row, bottom_row = 0, 7
        left_col, right_col = 0, 31
        while top_row <= bottom_row and left_col <= right_col:
            for i in range(left_col, right_col + 1):
                display.pixel(i, top_row, 1)
                display.show()
                time.sleep(0.05)
                if Config.left: 					# Back
                    break
            for i in range(top_row + 1, bottom_row + 1):
                display.pixel(right_col, i, 1)
                display.show()
                time.sleep(0.05)
                if Config.left: 					# Back
                    break            
            for i in range(right_col - 1, left_col - 1, -1):
                display.pixel(i, bottom_row, 1)
                display.show()
                time.sleep(0.05)
                if Config.left: 					# Back
                    break            
            for i in range(bottom_row - 1, top_row, -1):
                display.pixel(left_col, i, 1)
                display.show()
                time.sleep(0.05)
                if Config.left: 					# Back
                    break            
            top_row += 1
            bottom_row -= 1
            left_col += 1
            right_col -= 1
            if Config.left: 					# Back
                break
        if Config.left: 					# Back
            time.sleep(0.2)
            Config.left=False
            break
values = ['A']
az0005 = 0
display_start = 0
blink_state = False
last_blink_time = time.ticks_ms()
BLINK_INTERVAL = 500  # Blink every 500 milliseconds
def update_display():
    global values, az0005, display_start, blink_state, last_blink_time, BLINK_INTERVAL
    display_values = values[display_start:display_start+4]
    if blink_state and display_start <= az0005 < display_start + 4:
        display_values[az0005 - display_start] = "_"
    while len(display_values) < 4:  # Pad the display values
        display_values.append(' ')
    text = ''.join(display_values)
    show(text)
def az0008(msg="A"):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789!' #@#$%^&*()-+='
    max_index = len(characters) - 1
    global values, az0005, display_start, blink_state, last_blink_time, BLINK_INTERVAL
    az0005 = 0
    display_start = 0
    values = list(msg) #['A']
    while True:
        current_time = time.ticks_ms()
        if current_time - last_blink_time >= BLINK_INTERVAL:
            blink_state = not blink_state
            last_blink_time = current_time
            update_display()
        if Config.up:
            Config.up=False
            index = characters.index(values[az0005])
            index = (index + 1) % max_index
            values[az0005] = characters[index]
            update_display()
            time.sleep(0.2)
            Config.up=False
        if Config.down:
            Config.down=False
            index = characters.index(values[az0005])
            index = (index - 1) % max_index
            values[az0005] = characters[index]
            update_display()
            time.sleep(0.2)
            Config.down=False
        if Config.left and az0005 > 0:
            Config.left=False
            az0005 -= 1
            if az0005 < display_start:
                display_start -= 1
            update_display()
            time.sleep(0.2)
            Config.left=False
        if Config.right:
            Config.right=False
            if az0005 < len(values) - 1:
                az0005 += 1
                if az0005 >= display_start + 4:
                    display_start += 1
                update_display()
            elif az0005 == len(values) - 1:
                values.append('A')
                az0005 += 1
                if az0005 >= display_start + 4:
                    display_start += 1
                update_display()
            time.sleep(0.2)
            Config.right=False
        if Config.button_pressed:
            time.sleep(0.2)
            Config.button_pressed=False
            break
        time.sleep(0.5)
    az0010 = ''.join(values)
    return az0010.rstrip()
def L111_EditYourMessage():
    msg = read_string_from_file("your_message.txt")
    if msg=="":
        msg="JOY!"
    msg = msg.upper()
    msg=az0008(msg)
    write_string_to_file("your_message.txt", msg)
    Config.left=True
def L112_ShowYourMessage():
    msg = read_string_from_file("your_message.txt")
    az0013=False
    if msg=="":
        msg="Change this message using Menu L111!"
        az0013=True
    msg = msg.upper()
    while True:
        scroll(msg, need_left=True)
        if az0013:
            pass
        if Config.left:
            time.sleep(0.2)
            Config.left=False
            break
        time.sleep(0.1)
    time.sleep(1)
    Config.left=True
def L301_Traffic():
    red_led = Pin(2, Pin.OUT)
    yellow_led = Pin(3, Pin.OUT)
    green_led = Pin(4, Pin.OUT)
    while True:
        red_led.value(0)
        yellow_led.value(0)
        green_led.value(0)
        show("    ")
        red_led.value(1)
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        red_led.value(0)
        yellow_led.value(0)
        green_led.value(0)
        show("    ")
        yellow_led.value(1)
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        red_led.value(0)
        yellow_led.value(0)
        green_led.value(0)
        show("    ")
        green_led.value(1)
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
        time.sleep(1)
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            show("    ")
            break
def L305_AdvancedTraffic():
    red_led = Pin(2, Pin.OUT)
    yellow_led = Pin(3, Pin.OUT)
    green_led = Pin(4, Pin.OUT)
    while True:
        red_led.value(0)
        yellow_led.value(0)
        green_led.value(0)
        red_led.value(1)
        if Config.left:
            break   
        show("0005")
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("0004")
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("0003")
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("0002")
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("0001")
        yellow_led.value(1)
        beep()
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("    ")
        display_reset()
        beep()
        red_led.value(0)
        time.sleep(1)  # keep it on for 2 seconds
        if Config.left:
            break   
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        red_led.value(0)
        yellow_led.value(0)
        green_led.value(1)
        show("0005")
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("0004")
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("0003")
        beep()
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("0002")
        beep()
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("0001")
        beep()
        time.sleep(1)  # keep it on for 5 seconds
        if Config.left:
            break   
        show("    ")
        display_reset()
        if Config.left:
            red_led.value(0)
            yellow_led.value(0)
            green_led.value(0)
            break  
def L302_IR_Intruder():
    IR = Pin(0, Pin.IN)
    while True:
        if IR.value() == 0:
            beep(0.5)
            scroll("INTRUDER DETECTED!")
            time.sleep(0.5)
            beep(0.5)
            time.sleep(0.5)
            beep(0.5)
            time.sleep(0.5)
        else:
            scroll("SECURITY IS ON")
        if Config.left:
            break
def L303_IR_Counter():
    IR = Pin(0, Pin.IN)
    count=0
    show("{:04}".format(count))
    while True:
        if IR.value() == 0:
            beep()
            count = count + 1
            show("{:04}".format(count))
            time.sleep(0.2)
        if Config.left:
            break
def L304_LightMeter():
    while True:
        light = ldr.read_u16()
        print("LDR: " + str(light))
        scaled_value = ((light - 0) / ((2**16 - 1) - 0)) * (9999 - 0) + 0
        scaled_value = int(round(9999-scaled_value))
        s=f"{scaled_value:04}"
        show(s)
        time.sleep(0.2)
        if Config.left:
            break    
def run_it():
    print("RUN IT")
    if Config.menu_index not in menu:
        print("Running: " + Config.menu_index + " Code: " + menu[Config.program_menu][Config.menu_index])
        original_string = menu[Config.program_menu][Config.menu_index]
        new_string = original_string.replace("PRESS TO START. ", "", -1)
        scroll("Running: " + new_string)
    else:
        print("Nothing to Run: "+ Config.menu_index)
        show("RunX")
        return Config.menu_index
    count=0
    while True:
        if Config.menu_index == "L101":
            L101_Snake()
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L102":
            L102_Car()
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L103":
            L103_16()
        if Config.menu_index == "L104":
            L104_AZ()
        if Config.menu_index == "L105":
            L105_Timer()
        if Config.menu_index == "L106":
            L106_StopWatch()
        if Config.menu_index == "L107":
            L107_MentalMath()
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L108":
            L108_PartyQuiz()
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L109":
            L109_IndiaQuiz()
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L110":
            L110_Greetings()
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L111":
            L111_EditYourMessage()
            time.sleep(0.2)
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L112":
            print("Calling L112")
            L112_ShowYourMessage()
            print("Ended L112 " + str(Config.left))
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L201":
            print("Starting GOOD")
            show("GOOD")
            while True:
                time.sleep(0.2)
                if Config.left:
                    print("Left")
                    time.sleep(0.2)
                    break
            Config.left=False
            print("Ending GOOD Returning")
            return Config.menu_index
        if Config.menu_index == "L202":
            print("Starting 1234")
            show("1234")
            while True:
                time.sleep(0.2)
                if Config.left:
                    print("Left")
                    time.sleep(0.2)
                    break
            Config.left=False
            print("Ending GOOD Returning")
            return Config.menu_index
        if Config.menu_index == "L203":
            while True:
                scroll("Hello, How Are you?", need_left=True)
                time.sleep(0.2)
                if Config.left:
                    print("Left")
                    time.sleep(0.2)
                    break                
            show(Config.menu_index)
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L204":
            show("Be  ")
            time.sleep(1)
            show("Kind")
            time.sleep(1)
            if any_button():
                while any_button():
                    buttons_reset()
                    time.sleep(0.2)
                    break
                Config.left = False
                return Config.menu_index
        if Config.menu_index == "L205":
            while True:
                if Config.button_pressed:
                    show("Kind")
                    time.sleep(0.5)
                    Config.button_pressed = False
                else:
                    show("Be  ")
                    time.sleep(1)
                if Config.left:
                    beep()
                    while any_button():
                        buttons_reset()
                        time.sleep(0.2)
                        break
                    Config.left = False
                    return Config.menu_index
        if Config.menu_index == "L206": #LOOP
            for i in range(1,11):
                show(str(i))
                time.sleep(1)
                if Config.left:
                    time.sleep(0.2)
                    beep()
                    break
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L207":
            while True:
                show(str(count))
                if Config.button_pressed:
                    count = count + 1
                    if count==11:
                        count=0
                    Config.button_pressed = False
                time.sleep(0.2)
                if Config.left:
                    time.sleep(0.2)
                    beep()
                    break
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L208":
            count=0
            while True:
                show(str(count))
                if Config.up:
                    while True:
                        Config.up = False
                        time.sleep(0.2)
                        if not Config.up:
                            break
                    count = count - 1
                    if count==-1:
                        beep()
                        count=0
                    time.sleep(0.2)
                    Config.up = False
                if Config.down:
                    while True:
                        Config.down = False
                        print("Down")
                        time.sleep(0.2)
                        if not Config.down:
                            print("Not Down")
                            break
                    count = count + 1
                    time.sleep(0.2)
                    Config.down = False
                time.sleep(0.4)
                if Config.left:
                    time.sleep(0.2)
                    beep()
                    break
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L209":
            while True:
                show("----")
                if Config.up:
                    show(" Up ")
                    Config.up = False
                if Config.down:
                    show("Down ")
                    Config.down = False
                if Config.right:
                    scroll("Right")
                    Config.right = False
                time.sleep(0.4)
                if Config.left:
                    time.sleep(0.2)
                    beep()
                    break
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L210": # RANDOM LETTER
            while True:
                letter = random.choice(string.ascii_uppercase)
                show(letter)
                beep()
                time.sleep(2)
                if Config.left:
                    time.sleep(0.2)
                    beep()
                    break
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L211": # RANDOM NUMBER
            while True:
                random.seed(Config.xValue)
                number = random.randint(0, 9999)
                show("{:04}".format(number))
                beep()
                time.sleep(2)
                if Config.left:
                    time.sleep(0.2)
                    beep()
                    break
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L212": # RANDOM WORD
            while True:
                kid_friendly_verbs = [
                    "jump",
                    "run",
                    "laugh",
                    "play",
                    "dance",
                    "sing",
                    "climb",
                    "draw",
                    "write",
                    "swing"
                ]
                chosen_verb = random.choice(kid_friendly_verbs)
                beep()
                scroll(chosen_verb+" ")
                time.sleep(2)
                if Config.left:
                    time.sleep(0.2)
                    beep()
                    break
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L213": # Shooting
            L213_Shooting()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L214": # Random Fill
            L214_RandomFill()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L215": # Spiral Fill
            L215_SpiralFill()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L216": # Bitmap
            for bitmap in bitmaps:
                display_reset()
                scroll(bitmap)
                display_bitmap(eval(bitmap),0)
                time.sleep(2)
                if Config.left:
                    break
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L217": # Spiral Fill
            L217_BoomBox()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L218": # Dot
            display_reset()
            L218_MoveADot()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L219": # Dot
            display_reset()
            L219_MoveADotAround()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L220": # Dot
            L220_CountryCapital()
            print("Exited Country Capital")
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L221": # Dot
            L221_WordOpposite()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L222": # Dot
            L222_MentalMath()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L223": # Dot
            L223_Tambola()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L301":
            L301_Traffic()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L302":
            L302_IR_Intruder()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L303":
            L303_IR_Counter()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L305":
            L305_AdvancedTraffic()
        if Config.menu_index == "L304":
            L304_LightMeter()
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.menu_index == "L305" or \
        Config.menu_index == "L306" or \
        Config.menu_index == "L307" or \
        Config.menu_index == "L308" or \
        Config.menu_index == "L309" or \
        Config.menu_index == "L310" or \
        Config.menu_index == "L311" or \
        Config.menu_index == "L312" or \
        Config.menu_index == "L313" or \
        Config.menu_index == "L314" or \
        Config.menu_index == "L315": # User projects
            fn="project_"+Config.menu_index+".py"
            user_code=read_string_from_file(fn)
            if user_code=="":
                template=PROJECT_TEMPLATE
                formatted_string = template.format(MENU=Config.menu_index)
                write_string_to_file(fn,formatted_string)
                user_code=formatted_string
            exec(user_code)
            scroll("Done..")
            show(Config.menu_index)
            while any_button():
                buttons_reset()
                time.sleep(0.2)
                break
            Config.left = False
            return Config.menu_index
        if Config.left: 					# Back
            time.sleep(0.2)
            while Config.left:
                time.sleep(0.2)
            Config.left=False
            print("Exiting run")
            return Config.menu_index
        print("RUN IT LAST " + str(Config.left))
        time.sleep(1)
        Config.left = False
