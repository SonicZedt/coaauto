from vgamepad import XUSB_BUTTON
from core.gamepad import Gamepad
from core.screen import *
from core.report import FarmingReport
from commons import config, templates
import mss
import time
import random

# gamepad = None
gamepad = Gamepad()
sct = mss.mss()
monitor = sct.monitors[config.MONITOR]
report = FarmingReport()

def wait_screen(screen: ScreenBase, second: int = 15) -> dict:
    print(f"{screen.screen} >> waiting")
    for _ in range(second):
        match = screen.match(screenshot=sct.grab(monitor))
        if match:
            return match
        time.sleep(1)

    return None


def navigate(screen: ScreenBase, dst_template: str, src_template: str, confirmation_template: str = "", 
    dur_move: int = None, dur_limit: int = 30, dur_cycle: float = 1, 
    success_callback: callable = None, fail_callback: callable = None, get_obj_coordinate: callable = None, dst_tolerance: int = 0,
    force_center_src: bool = True):

    def check_confirmation(dur_current, dst_center: tuple[int, int]):
        # a confirmation template is detected
        if confirmation_template:
            return screen.match(confirmation_template, sct.grab(monitor))
        
        # destination reached
        elif dst_center is not None and get_obj_coordinate is not None:
            current_coordinate = get_obj_coordinate()
            if not current_coordinate:
                return None
             
            # print(current_coordinate.center, dst_center)
            in_x = abs(current_coordinate.center[0] - dst_center[0]) <= dst_tolerance
            in_y = abs(current_coordinate.center[1] - dst_center[1]) <= dst_tolerance
            
            return in_x and in_y

        # completed dur_move-th iteration
        elif dur_move is not None:
            return dur_current >= dur_move

        return None

    print(f"{screen.screen} >> navigating...")

    templates = [
        {
            'title': 'dst',
            'path': dst_template
        }, {
            'title': 'src',
            'path': src_template
        }
    ]

    prev_analog_x = 0
    prev_analog_y = 0

    # navigation_multiplier = 2.4 if config.MOBILE else 4
    confirmed = False

    for i in range(dur_limit):
        if not confirmed:
            confirmed = check_confirmation(i, None)
            
        matches = screen.matches(templates, sct.grab(monitor), 0.4)

        analog_x = 0
        analog_y = 0

        if confirmed:
            print(f"{screen.screen} >> navigation confirmed")

            gamepad.left_analog_reset()

            if success_callback:
                success_callback()
            
            return True

        elif len(matches) == len(templates):
            dst = matches[0]
            src = matches[1]

            confirmed = check_confirmation(i, dst_center=dst.center)
            if confirmed:
                if i == dur_limit:
                    i -= 1

                continue

            if force_center_src:
                src.width, src.height = config.RESOLUTION
                src.center = (src.coordinate[0] + src.width / 2,src.coordinate[1] + src.height / 2)

            analog_x, analog_y = gamepad.get_analog_direction(src, dst, 4)

        if (prev_analog_x != analog_x) or (prev_analog_y != analog_y):
            print(f"{screen.screen} >> navigating from {src.center} to {dst.center}, with direction ({analog_x}, {analog_y})")
            prev_analog_x = analog_x
            prev_analog_y = analog_y

        gamepad.left_analog(x=analog_x, y=analog_y, delay=0)
        time.sleep(dur_cycle)
    else:
        print(f"{screen.screen} >> navigation failed")
        gamepad.left_analog_reset()
        
        if fail_callback:
            fail_callback()

    return False


def login() -> bool:
    # Starting
    screen = ScreenMainMenu(sct.grab(monitor))
    if screen.match():
        screen.log_on_focus()
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        screen.log_undetected()
        return False

    # Character selection
    screen = ScreenCharacterList(sct.grab(monitor))
    match = wait_screen(screen)
    if match:
        screen.log_on_focus()
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        screen.log_undetected()
        return False
    
    return True


def cast_skill(combo: int = 1):
    if config.MODE == 'PC':
        match combo:
            case 1:
                for _ in range(random.randint(2, 4)):
                    gamepad.left_trigger(delay=0.1)
                gamepad.right_trigger()
                gamepad.right_trigger()
                for _ in range(random.randint(4, 10)):
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
            case 2:
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                for _ in range(random.randint(2, 4)):
                    gamepad.right_trigger()
            case 3:
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
            case _:
                for _ in range(random.randint(4, 8)):
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
    else:
        match combo:
            case 1:
                for _ in range(random.randint(2, 4)):
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B, 0.1)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)

                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
                for _ in range(random.randint(2, 6)):
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            case 2:
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
            case 3:
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
            case _:
                for _ in range(random.randint(2, 6)):
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)


def world_to_teamup(dungeon_name: str):
    # From world screen, navigate to dugenon teamup platform
    # World
    screen = ScreenWorld(sct.grab(monitor))
    match = wait_screen(screen)
    if match:
        screen.log_on_focus()

        # open up wheel menu
        if config.MODE == 'PC':
            gamepad.hold_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
            gamepad.right_analog(x=1, y=-1)
            gamepad.right_analog_reset()
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        else:
            gamepad.hold_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
            gamepad.right_analog(x=1, y=-1)
            gamepad.right_analog_reset()
            gamepad.release_button(XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

        time.sleep(1)
    else:
        screen.log_undetected()
        return False

    # Gameplay
    screen = ScreenGameplayAdventure(sct.grab(monitor))
    match = wait_screen(screen)
    if match:
        screen.log_on_focus()

        if config.MODE == 'PC':
            navigate(
                screen=screen,
                dst_template=screen.template_path,
                src_template=templates.GAMEPLAY,
                dur_move=1,
                dur_cycle=0.5,
                fail_callback=restart_from_world,
                # get_obj_coordinate=lambda: screen.find_cursor_gamepad(sct.grab(monitor)),
                # dst_tolerance=10
            )
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        screen.log_undetected()
        return False

    # Adventure
    screen = ScreenAdventureAbyss(sct.grab(monitor))
    match = wait_screen(screen)
    if match:
        screen.log_on_focus()

        if dungeon_name == 'abyss':
            return True
            
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP, press_delay=0.1)

        if config.MODE == 'PC':
            gamepad.left_analog(x=1, y=0, delay=3)
            gamepad.left_analog(x=-.75, y=-.4, delay=0.4)
            gamepad.left_analog_reset()
        else:
            for _ in range(5):
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT, press_delay=0.1)

        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        screen.log_undetected()
        return False

    # Adventure - 55
    screen = ScreenAdventure55(sct.grab(monitor))
    match = wait_screen(screen)
    if match:
        screen.log_on_focus()
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
    else:
        screen.log_undetected()
        return False

    return True


def match_making(screen: ScreenBase) -> str:
    frame = sct.grab(monitor)

    if screen.is_loading(frame):
        return 'confirmed'

    if screen.match_making(frame) or screen.match_confirmation(frame):
        match_status = 'matchmaking'
        print(f"{screen.screen} >> matchmaking...")

        for i in range(240):
            if screen.match_confirmation(sct.grab(monitor)):
                print(f"{screen.screen} >> match found!")
                time.sleep(1)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
                
                for j in range(20):
                    time.sleep(1)
                    if screen.is_loading(sct.grab(monitor)):
                        match_status = 'confirmed'
                        print(f"{screen.screen} >> match confirmed")
                        break

                    if screen.match_making(sct.grab(monitor)):
                        break

                return match_status
            time.sleep(1)


def teamup():
    # Teamup platform
    screen = ScreenTeamup(sct.grab(monitor))
    match = wait_screen(screen)
    if match:
        screen.log_on_focus()
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)

        print(f"{screen.screen} >> waiting matchmaking")
        for i in range(10):
            if screen.match_making(sct.grab(monitor)):
                print(f"{screen.screen} >> matchmaking started")
                break

            time.sleep(1)

        match_status = 'unconfirmed'
        for i in range(15):
            match_status = match_making(screen)
            if match_status == 'confirmed':
                break

            grab = sct.grab(monitor)
            if screen.match(screenshot=grab) and not screen.match_making(grab) and not screen.match_confirmation(grab):
                print(f"{screen.screen} >> matchmaking failed, finding quick match again")
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_X)
            else:
                print(f"{screen.screen} >> matchmaking failed, retrying")
                
            time.sleep(1)

        if match_status != 'confirmed':
            print(f"{screen.screen} >> unable to matchmaking")
            return False
    else:
        screen.log_undetected()
        return False

    return True


def dungeon_55():
    # Dungeon
    screen = ScreenDungeon55(sct.grab(monitor))
    match = wait_screen(screen, 60)
    if match:
        screen.log_on_focus()
        report.update_attempt()

        print(f"{screen.screen} >> waiting for boss fight")
        for i in range(120):
            grab = sct.grab(monitor)
            if screen.is_bossfight(grab):
                print(f"{screen.screen} >> in boss fight")
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y, 0.1)

                print(f"{screen.screen} >> moving forward")
                gamepad.left_analog(0, 1, 2)
                gamepad.left_analog_reset()

                print(f"{screen.screen} >> casting skills")
                cast_skill()
                break
            elif screen.is_finished(grab):
                print(f"{screen.screen} >> bossfight finished without participating")
                break

            time.sleep(1)
        else:
            print(f"{screen.screen} >> boss fight not initiated, exiting")
            update_farming_result(screen)
            
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_START)
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
            return False
    
        for i in range(60):
            if screen.is_finished(sct.grab(monitor)):
                print(f"{screen.screen} >> dungeon is finished, initiatin rematch")
                update_farming_result(screen)

                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
                
                rematch_dungeon(dungeon_55)
                main()

                break

            if i > 0  and i % 5 == 0:
                print(f"{screen.screen} >> moving forward")
                gamepad.left_analog(0, 1, 1)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B, 0.1)
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B, 0.1)
                gamepad.left_analog_reset()
                print(f"{screen.screen} >> casting skills")
                cast_skill(2)

            time.sleep(1)
        else:
            print(f"{screen.screen} >> result unknown, attempting to exit")
            for i in range(5):
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
            report.add_avg_reward()
            exit_dungeon()
            main()
            
    else:
        screen.log_undetected()
        return False
    
    return True


def dungeon_abyss():
    screen = ScreenDungeonAbyss(sct.grab(monitor))
    match = wait_screen(screen, 60)
    if match:
        screen.log_on_focus()
        report.update_attempt()

        print(f"{screen.screen} >> moving forward")
        gamepad.left_analog(0, 1, 2)

        print(f"{screen.screen} >> casting skill")
        cast_skill(3)

        for _ in range(15):
            if screen.is_bossfight(sct.grab(monitor)):
                break
            print(f"{screen.screen} >> casting default batk")
            cast_skill(0)
            time.sleep(1)

        print(f"{screen.screen} >> casting skill")
        cast_skill(1)

        print(f"{screen.screen} >> waiting for result")
        for i in range(60):
            if screen.is_finished(sct.grab(monitor)):
                print(f"{screen.screen} >> dungeon is finished, initiatin rematch")
                update_farming_result(screen)

                if screen.is_finished(sct.grab(monitor)):
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
                
                rematch_dungeon(dungeon_abyss)
                main()

                break

            if i > 0  and i % 5 == 0:
                print(f"{screen.screen} >> moving forward")
                gamepad.left_analog(0, 1, 2)
                gamepad.left_analog_reset()
                print(f"{screen.screen} >> casting skills")
                cast_skill(2)

            time.sleep(1)
        else:
            print(f"{screen.screen} >> result unknown, attempting to exit")
            for i in range(5):
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
            report.add_avg_reward()
            exit_dungeon()
            main()
    else:
        screen.log_undetected()
        return False
    
    return True


def exit_dungeon():
    if config.MODE == 'PC':
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        gamepad.left_analog(x=0, y=1, delay=2)
        gamepad.left_analog(x=.5, y=-.25, delay=0.4)
        gamepad.left_analog_reset()
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_START)
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)

    screen = ScreenDungeon55(sct.grab(monitor))
    for _ in range(5):
        if screen.is_exit(sct.grab(monitor)):
            if config.MODE == 'PC':
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
            else:
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
            break
        time.sleep(1)


def rematch_dungeon(return_callback):
    # screen = ScreenDungeon(sct.grab(monitor))
    screen = ScreenDungeon55(sct.grab(monitor))

    print(f"{screen.screen} >> attempting to rematch dungeon")

    def trigger_rematch():
        print(f"{screen.screen} >> waypoint triggered")
        gamepad.left_analog_reset()
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)

        print(f"{screen.screen} >> waiting matchmaking")
        for i in range(15):
            if not screen.match_making(sct.grab(monitor)):
                time.sleep(1)
                continue
            else:
                print(f"{screen.screen} >> matchmaking started")
                break
        else:
            print(f"{screen.screen} >> unable to matchmaking, exiting")
            exit_dungeon()
            return False
        
        attempt = 0
        max_attempt = 15
        match_status = 'unconfirmed'
        while attempt < max_attempt:
            match_status = match_making(screen)
            if match_status == 'confirmed':
                break

            grab = sct.grab(monitor)
            if not screen.match_making(grab) and not screen.match_confirmation(grab):
                print(f"{screen.screen} >> matchmaking failed, finding rematch")
                gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
                attempt = 0
            else:
                print(f"{screen.screen} >> matchmaking failed, retrying")
                attempt += 1
            
            time.sleep(1)
        else:
            print(f"{screen.screen} >> maximum attempt reached, exiting")
            exit_dungeon()
            return False
        
        if match_status != 'confirmed':
            print(f"{screen.screen} >> rematch not confirmed, exiting")
            exit_dungeon()
            return False
        
        return_callback()

    navigate(
        screen=screen,
        dst_template=templates.DUNGEON_WAYPOINT_EXIT,
        src_template=templates.WORLD_PROFILE,
        confirmation_template=templates.DUNGEON_REMATCH,
        dur_limit=30,
        success_callback=trigger_rematch,
        fail_callback=lambda: (exit_dungeon(), main())
    )

    return False


def update_farming_result(screen: ScreenDungeon):
    report.update_completed_attempt()

    print(f"{screen.screen} >> waiting for reward info")
    reward = screen.get_reward(sct.grab(monitor))
    for i in range(10):
        if reward:
            report.update_dungeon_reward(reward['gold'], reward['exp'])
            return
        reward = screen.get_reward(sct.grab(monitor))
        time.sleep(1)
    else:
        print(f"{screen.screen} >> unable to get reward info")
        report.add_avg_reward()


def get_window():
    screen = ScreenGeneric(sct.grab(monitor))
    window = screen.window()

    if not window:
        return None
    
    window.width, window.height = config.RESOLUTION

    x = monitor['left'] + window.coordinate[0]
    y = monitor['top'] + window.coordinate[1]
    
    return {
        'left': x,
        'top': y,
        'center': (x + window.width // 2, y + window.height // 2),
        'width': window.width,
        'height': window.height
    }


def restart_from_world():
    for _ in range(5):
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B, 0.1)
    main()


def calibrate_gamepad(screen: ScreenBase):
    print(f"{screen.screen} >> calibrating gamepad")

    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, press_delay=0.1)

    match = screen.find_cursor_gamepad(sct.grab(monitor))
    if not match:
        print(f"{screen.screen} >> gamepad calibration failed, unable to find cursor")
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, press_delay=0.1)
        return
    
    time = 0.5

    initial_coordinate = match.center

    gamepad.left_analog(x=0.5, y=0.5, delay=time)
    gamepad.left_analog_reset()

    match = screen.find_cursor_gamepad(sct.grab(monitor))
    if not match:
        print(f"{screen.screen} >> gamepad calibration failed, unable to find cursor")
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, press_delay=0.1)
        return
    
    current_coordinate = match.center
    
    dx = abs(current_coordinate[0] - initial_coordinate[0])
    dy = abs(current_coordinate[1] - initial_coordinate[1])

    # cursor velocity, pixels per 0.1
    vx = (dx / time) * 0.1
    vy = (dy / time) * 0.1

    print(initial_coordinate, current_coordinate)
    print('dx:', dx, vx)
    print('dy:', dy, vy)

    gamepad.set_velocity(vx, vy)
    print(f"{screen.screen} >> gamepad calibrated. vx: {vx}, vy: {vy}")
    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN, press_delay=0.1)


def main():
    dungeon_name = ''

    time.sleep(2)
    screen = ScreenGeneric(sct.grab(monitor))

    calibrate_gamepad(screen)

    matches = screen.matches(templates=[
        {
            'title': 'mainmenu',
            'path': templates.MAINMENU
        }, {
            'title': 'world',
            'path': templates.WORLD_PROFILE
        }
    ], match_threshold=0.6)

    teamup_screen_confirmed = False

    if not matches:
        print(f"{screen.screen} >> starting screen unknown")
        gamepad.right_analog(x=1, y=0)
        gamepad.right_analog_reset()
        restart_from_world()
        return

    elif matches[0].title == 'mainmenu':
        login()
        teamup_screen_confirmed = world_to_teamup(dungeon_name)
    elif any(m.title == 'world' for m in matches):
        teamup_screen_confirmed = world_to_teamup(dungeon_name)

    if not teamup_screen_confirmed:
        print(f"{screen.screen} >> next screen not confirmed, restarting")
        restart_from_world()

    teamup_match_confirmed = teamup()
    if not teamup_match_confirmed:
        print(f"{screen.screen} >> restarting")
        restart_from_world()
        return
    
    dungeon_55()


if __name__ == "__main__":
    window = get_window()
    if window:
        monitor = window

    # rematch_dungeon(lambda: print("test"))
    main()
    sct.close()