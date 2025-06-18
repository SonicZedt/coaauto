from enums import STAMINA_TYPE
from vgamepad import XUSB_BUTTON
from gamepad import Gamepad
from screen import *
from report import FarmingReport
import mss
import time
import random

# gamepad = None
gamepad = Gamepad()
sct = mss.mss()
monitor = sct.monitors[2]
report = FarmingReport()

def wait_screen(screen: ScreenBase, second: int = 15):
    print(f"{screen.screen} >> waiting")
    for _ in range(second):
        match = screen.match(screenshot=sct.grab(monitor))
        if match:
            return match
        time.sleep(1)

    return None


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
        
        for i in range(5):
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
    
        print(f"{screen.screen} >> waiting for result")
        for i in range(60):
            if screen.is_finished(sct.grab(monitor)):
                print(f"{screen.screen} >> dungeon is finished, initiatin rematch")
                update_farming_result(screen)

                if screen.is_finished(sct.grab(monitor)):
                    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
                
                rematch_dungeon(dungeon_55)
                main()

                break

            if i > 0  and i % 5 == 0:
                print(f"{screen.screen} >> moving forward")
                gamepad.left_analog(0, 1, 1)
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
    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_START)
    gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)

    screen = ScreenDungeon55(sct.grab(monitor))
    for _ in range(5):
        if screen.is_exit(sct.grab(monitor)):
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)
            break
        time.sleep(1)


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


def rematch_dungeon(return_callback):
    res = (800, 600)
    # screen = ScreenDungeon(sct.grab(monitor))
    screen = ScreenDungeon55(sct.grab(monitor))
    templates = [
        {
            'title': 'waypoint',
            'path': 'templates/dungeon_waypoint_exit.png'
            # 'path': 'templates/world_waypoint_fight.png'
        }, {
            'title': 'profile',
            'path': 'templates/world_profile.png'
        }
    ]

    print(f"{screen.screen} >> attempting to rematch dungeon")

    prev_analog_x = 0
    prev_analog_y = 0
    for _ in range(30):
        matches = screen.matches(templates, sct.grab(monitor), 0.4)
        confirmation = screen.match('templates/dungeon_rematch.png', sct.grab(monitor))

        analog_x = 0
        analog_y = 0

        if confirmation:
            print(f"{screen.screen} >> waypoint triggered")
            gamepad.left_analog_reset()
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_Y)
            gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_A)

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

        elif len(matches) == len(templates):
            waypoint = matches[0]
            waypoint_x, waypoint_y = waypoint['coordinate']
            waypoint_w, waypoint_h = waypoint['width'], waypoint['height']
            waypoint_x = waypoint_x + waypoint_w / 2
            waypoint_y = waypoint_y + waypoint_h / 2

            window = matches[1]
            window_x, window_y = window['coordinate']
            window_w, window_h = res
            window_x = window_x + window_w / 2
            window_y = window_y + window_h / 2

            dx = waypoint_x - window_x
            dy = -1 * (waypoint_y - window_y)

            limit_x = window_w
            limit_y = window_h

            analog_x = dx / limit_x * 4
            analog_y = dy / limit_y * 4

        if (prev_analog_x != analog_x) or (prev_analog_y != analog_y):
            print(f"{screen.screen} >> navigating to exit waypoint ({analog_x}, {analog_y})")
            prev_analog_x = analog_x
            prev_analog_y = analog_y

        gamepad.left_analog(x=analog_x, y=analog_y)
        time.sleep(1)
    else:
        print(f"{screen.screen} >> unable to find exit waypoint, exiting")
        gamepad.left_analog_reset()
        exit_dungeon()
        main()

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

    window = window[0]

    return {
        'left': monitor['left'] + window['coordinate'][0],
        'top': monitor['top'] + window['coordinate'][1],
        'width': window['width'],
        'height': window['height']
    }


def restart_from_world():
    for _ in range(5):
        gamepad.press_button(XUSB_BUTTON.XUSB_GAMEPAD_B, 0.1)
    main()


def main():
    dungeon_name = ''

    time.sleep(2)
    screen = ScreenGeneric(sct.grab(monitor))
    matches = screen.matches(templates=[
        {
            'title': 'mainmenu',
            'path': 'templates/mainmenu.png' 
        }, {
            'title': 'world',
            'path': 'templates/world_profile.png' 
        }
    ], match_threshold=0.6)

    teamup_screen_confirmed = False

    if not matches:
        print(f"{screen.screen} >> starting screen unknown")
        gamepad.right_analog(x=1, y=0)
        gamepad.right_analog_reset()
        restart_from_world()
        return

    elif matches[0]['title'] == 'mainmenu':
        login()
        teamup_screen_confirmed = world_to_teamup(dungeon_name)
    elif any(m['title'] == 'world' for m in matches): # this failed
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

    main()
    sct.close()