Crystal of Atlan Auto Dungeon
========================

#### Note:
This is an unofficial automation tool for the game Crystal of Atlan. It is designed to automate the process of farming dungeons by simulating player actions. This tool is intended for educational and research purposes especially in computer vision and automation and should be used at your own risk. The developers are not responsible for any consequences that may arise from using this tool, including but not limited to account bans or other issues with the game.

#### How it works:
The program uses computer vision to detect and interact with the game interface. It takes screenshots of the game window and analyzes them to find specific elements, such as buttons and menus. Once the elements are detected, the program simulates controller inputs to navigate the game and perform actions automatically.

Note: No game files are modified or injected with code. The program only interacts with the game through the user interface, similar to how a human player would. Use at your own risk.

#### How to use:
1. Install the required dependencies
    ```bash
    pip install -r requirements.txt
    ```
2. Replace templates `world_profile.png` and `dungeon_result_character.png` with your own screenshots of the game interface. These images should be taken while the game is running in windowed mode at 800x600 resolution. The program uses these images to identify the game elements it needs to interact with.
    - `world_profile.png`: A screenshot of player profile on the top left corner.
    - `dungeon_result_character.png`: A screenshot of the character result screen after completing a dungeon.
3. Open the game and make sure it is running in windowed mode in 800x600 resolution.
4. Player need to stand by in any town or city, preferably in Chrome Military Factory.
5. Adjust `config.py` if necessary, 
6. Run `main.py`.
7. Quickly alt + tab to game window.

#### In Game Configuration:
- Set **Resolution** to 800x600, windowed mode.
- Set **Gameplay Screeen** to slot 4 of quick wheel settings.
- Ensure game window is focused, not minimized.

#### Farming flow:
1. From world sreen, the program will automatically navigate to the dungeon menu.
2. It will select 55 dungeons in the dungeon menu.
3. Matchmaking will be initiated.
5. Wait for the dungeon to start.
6. Wait for boss cutscene.
7. Moving forward then cast some skill combos every 5 seconds.
8. Once finished, it will navigate players to exit waypoint.
9. Rematch and repeat.

#### Known Issues:
- May not work propery if resolution is different.
- May not work properly in some area in some city.
- Gamepad cursor navigation may not work properly in some cases.
- Some edge cases may cause the program to crash.
- Some edge cases are not yet handled, such as when kicked out of dungeon or when the game is closed unexpectedly.