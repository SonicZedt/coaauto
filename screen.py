from PIL import Image
from typing import Any
from mss.models import Monitor
from mss.screenshot import ScreenShot
from rapidocr import RapidOCR
from model import MatchTemplate
import cv2
import numpy as np
import config

ocr = None

class ScreenShotBase(ScreenShot):
    def __init__(self, data: bytearray, monitor: Monitor, **_: Any) -> None:
        super().__init__(data, monitor, **_)

    def grab_screen(self):
        return


class ScreenBase:
    @property
    def screen(self):
        return f"Screen: {self.__class__.__name__}"

    last_image = None

    def __init__(self, template: str, screenshot: ScreenShot, match_treshold: float = 0.8):
        self.screenshot = screenshot
        self.template_path = template
        self.template = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
        self.match_threshold = match_treshold

    def match(self, template: str = "", screenshot: ScreenShot = None, match_threshold: float = None) -> MatchTemplate:
        threshold = match_threshold if match_threshold else self.match_threshold
        image_gray = self.last_image

        if config.MOBILE:
            threshold = threshold * 0.7

        if screenshot:
            image = Image.frombytes("RGBA", screenshot.size, screenshot.bgra, "raw", "BGRA")
            image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
            self.last_image = image_gray
        elif not self.last_image:
            image = Image.frombytes("RGBA", self.screenshot.size, self.screenshot.bgra, "raw", "BGRA")
            image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)            
            self.last_image = image_gray

        
        template_image = self.template
        if template:
            template_image = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
        
        template_w, template_h = template_image.shape[::-1]

        res = cv2.matchTemplate(image_gray, template_image, cv2.TM_CCOEFF_NORMED)
        match = None

        min_val, pt, min_loc, max_loc = cv2.minMaxLoc(res)

        if pt >= threshold:
            match = MatchTemplate(
                title="",
                coordinate=max_loc,
                center=(max_loc[0] + template_w // 2, max_loc[1] + template_h // 2),
                width=template_w,
                height=template_h
            )

            # for debugging
            cv2.rectangle(
                image_gray, 
                max_loc, 
                (max_loc[0] + template_w, max_loc[1] + template_h),
                (0, 255, 255), 2
            )
 
        if config.DEBUG_CAPTURE:
            cv2.imwrite(f'captures/{self.__class__.__name__}.png', image_gray)
            cv2.imwrite(f'captures/debug.png', image_gray)
        
        if config.DEBUG_SHOW:
            cv2.imshow('debug', image_gray)
            cv2.waitKey(1)

        return match
    
    def matches(self, templates: list, screenshot: ScreenShot = None, match_threshold: float = None) -> list[MatchTemplate]:
        threshold = match_threshold if match_threshold else self.match_threshold

        if config.MOBILE:
            threshold = threshold * 0.7

        image_gray = self.last_image
        if screenshot:
            image = Image.frombytes("RGBA", screenshot.size, screenshot.bgra, "raw", "BGRA")
            image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
            self.last_image = image_gray
        elif not self.last_image:
            image = Image.frombytes("RGBA", self.screenshot.size, self.screenshot.bgra, "raw", "BGRA")
            image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)            
            self.last_image = image_gray

        all_matches = []

        for template in templates:
            template_path = template['path']

            template_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template_image is None:
                continue

            template_w, template_h = template_image.shape[::-1]
            res = cv2.matchTemplate(image_gray, template_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val >= threshold:
                all_matches.append(MatchTemplate(
                    title=template['title'],
                    coordinate=max_loc,
                    center=(max_loc[0] + template_w // 2, max_loc[1] + template_h // 2),
                    width=template_w,
                    height=template_h
                ))

                # for debugging
                cv2.rectangle(
                    image_gray,
                    max_loc,
                    (max_loc[0] + template_w, max_loc[1] + template_h),
                    (0, 255, 255), 2
                )

        if config.DEBUG_CAPTURE:
            cv2.imwrite(f'captures/{self.__class__.__name__}_multi.png', image_gray)
            cv2.imwrite(f'captures/debug.png', image_gray)

        if config.DEBUG_SHOW:
            cv2.imshow('debug', image_gray)
            cv2.waitKey(1)

        return all_matches

    def matches_test(self, templates: list, screenshot: ScreenShot = None, match_threshold: float = None) -> list[MatchTemplate]:
        threshold = match_threshold if match_threshold else self.match_threshold

        if config.MOBILE:
            threshold = threshold * 0.7

        image_gray = self.last_image
        if screenshot:
            image = Image.frombytes("RGBA", screenshot.size, screenshot.bgra, "raw", "BGRA")
            image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
            self.last_image = image_gray
        elif not self.last_image:
            image = Image.frombytes("RGBA", self.screenshot.size, self.screenshot.bgra, "raw", "BGRA")
            image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)            
            self.last_image = image_gray

        image_blur = cv2.GaussianBlur(image_gray, (3, 3), 0)
        image_canny = cv2.Canny(image=image_blur, threshold1=50, threshold2=100)

        all_matches = []

        for template in templates:
            template_path = template['path']

            template_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template_image is None:
                continue

            # template_image = cv2.GaussianBlur(template_image, (3, 3), 0)
            # template_image = cv2.Canny(image=template_image, threshold1=50, threshold2=100)
            cv2.imshow(template_path, template_image)
            cv2.waitKey(0)

            template_w, template_h = template_image.shape[::-1]
            res = cv2.matchTemplate(image_gray, template_image, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            print(template_path, max_val)
            if max_val >= threshold:
                all_matches.append(MatchTemplate(
                    title=template['title'],
                    coordinate=max_loc,
                    center=(max_loc[0] + template_w // 2, max_loc[1] + template_h // 2),
                    width=template_w,
                    height=template_h
                ))

                # for debugging
                cv2.rectangle(
                    image_gray,
                    max_loc,
                    (max_loc[0] + template_w, max_loc[1] + template_h),
                    (0, 255, 255), 2
                )

        if config.DEBUG_CAPTURE:
            cv2.imwrite(f'captures/{self.__class__.__name__}_multi.png', image_gray)
            cv2.imwrite(f'captures/debug.png', image_gray)

        if config.DEBUG_SHOW:
            cv2.imshow('debug', image_gray)
            cv2.waitKey(1)

        return all_matches

    def match_making(self, screenshot: ScreenShot):
        return self.match('templates/teamup_matchmaking.png', screenshot, 0.6)

    def match_confirmation(self, screenshot: ScreenShot):
        return self.match('templates/teamup_confirmation.png', screenshot)

    def is_loading(self, screenshot: ScreenShot):
        return self.match('templates/loading.png', screenshot, 0.4)
    
    def window(self):
        if config.MOBILE:
            match = self.match('templates/window_mobile.png')
            # if match:
            #     match.coordinate = (-1080, -300)
            #     match.center = (-1080 + match.width // 2, -300 + match.height // 2)
            return match
        return self.match('templates/window.png')

    def log_on_focus(self):
        print(self.screen)
    
    def log_undetected(self):
        print(f"{self.screen} not detected")


class UIStamina(ScreenBase):
    def __init__(self, screenshot: ScreenShot, stamina_type: str):
        super().__init__(f'templates/stamina_{stamina_type}.png', screenshot)
        self.stamina_type = stamina_type

    def count(self):
        matches = self.match()
        
        if not matches:
            print(f"Stamina {self.stamina_type} not detected")
            return
        
        match = matches[0]
        match.width += 60

        x, y = match.coordinate
        w, h = match.width, match.height

        image = Image.frombytes("RGBA", self.screenshot.size, self.screenshot.bgra, "raw", "BGRA")
        image_roi = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)[y:y+h, x:x+w]


class ScreenGeneric(ScreenBase):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/mainmenu.png', screenshot, 0.7)
    

class ScreenMainMenu(ScreenBase):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/mainmenu.png', screenshot)


class ScreenCharacterList(ScreenBase):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/characterlist_play.png', screenshot)


class ScreenWorld(ScreenBase):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/world_profile.png', screenshot, 0.7)


class ScreenGameplayAdventure(ScreenBase):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/gameplay_adventure.png', screenshot, 0.7)


class ScreenAdventureAbyss(ScreenBase):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/adventure_abyss.png', screenshot)


class ScreenAdventure55(ScreenBase):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/adventure_55.png', screenshot, 0.9)


class ScreenTeamup(ScreenBase):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/teamup_buttons.png', screenshot, 0.8)


class ScreenDungeon(ScreenBase):
    def __init__(self, template: str, screenshot: ScreenShot):
        super().__init__(template, screenshot, 0.8)
    
    def is_finished(self, screenshot: ScreenShot):
        return self.match('templates/dungeon_result_character.png', screenshot, 0.9)
    
    def is_exit(self, screenshot: ScreenShot):
        return self.match('templates/dungeon_exit_confirmation.png', screenshot)
    
    def get_reward(self, screenshot: ScreenShot):
        match = self.match('templates/dungeon_result_gold.png', screenshot)
        
        if not match:
            return None
        
        match.width = 83
        match.height = 76

        x, y = match.coordinate
        w, h = match.width, match.height

        roi = self.last_image[y:y+h, x:x+w]
        result = ocr(roi)

        # assume the order is:
        # gold bonus (%)
        # gold
        # exp text
        # exp bonus (%)
        # exp
        if not result.txts or len(result.txts) != 5:
            return None
        
        gold = result.txts[1].replace(',', '')
        exp = result.txts[4].replace(',', '')

        try:
            gold = int(gold)
        except:
            print(f"{self.screen} >> unable to parse value ({gold})")
            return None

        try:
            exp = int(exp)
        except:
            print(f"{self.screen} >> unable to parse value ({exp})")
            return None

        return {
            'gold': gold,
            'exp': exp
        }
    
    def get_time(self, screenshot: ScreenShot):
        return self.match('templates/dungeon_result_time.png', screenshot)


class ScreenDungeon55(ScreenDungeon):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/dungeon_map.png', screenshot)

    def is_bossfight(self, screenshot: ScreenShot):
        return len(self.matches([
            {
                'title': 'cutscene',
                'path': 'templates/dungeon_cutscene_boss.png'
            }, {
                'title': 'bossfight',
                'path': 'templates/dungeon_boss.png'
            }
        ], screenshot)) > 0

class ScreenDungeonAbyss(ScreenDungeon):
    def __init__(self, screenshot: ScreenShot):
        super().__init__('templates/dugeon_abyss.png', screenshot)

    def is_bossfight(self, screenshot: ScreenShot):
        return self.match('templates/dungeon_abyss_boss.png', screenshot, 0.7)


if __name__ == 'screen':
    ocr = RapidOCR()