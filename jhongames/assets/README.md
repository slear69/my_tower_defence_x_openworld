# Jhon Games

A small Pygame browser-game prototype. The current build displays a tile map, lets you choose a plant from the icons below the map, and place it on an available spot using your starting money.

## Play

The game runs in a browser when built with Pygbag. It can also be run locally with Python.

### Run locally

Use Python 3.12, then install the dependencies and start the game:

```powershell
python -m pip install pygame pytmx pygbag
python main.py
```

Run these commands from the project folder, where `main.py` is located.

### Build for the browser

Install Pygbag if you have not already, then build from the project folder:

```powershell
python -m pip install pygbag
pygbag --build .
```

The browser-ready files are written to `build/web`.

## Controls

- Click a plant icon below the map to select it.
- Click an unoccupied marked spot on the map to place the selected plant.
- Your remaining money is shown in the upper-right corner.

## Publish on itch.io

1. Build the browser version as described above.
2. Create a ZIP containing the **contents** of `build/web`. `index.html` must be at the top level of the ZIP, not inside a nested `web` folder.
3. On itch.io, create a project and set its project type to **HTML**.
4. Upload the ZIP, enable **This file will be played in the browser**, and choose **Embed in page**.
5. Save and test the project page.

On Windows, you can create the ZIP from the project folder with:

```powershell
Compress-Archive -Path .\build\web\* -DestinationPath .\jhongames-itch.zip
```

## Project files

- `main.py` — game loop, display, input, and placement.
- `draw_map.py` — loads the Tiled map and map sprites.
- `test.tmx` — map and placement spots.
- `*.png` and `*.tsx` — image and tileset assets used by the map and game.

This is an in-progress prototype; enemy movement and the main gameplay/update logic are not implemented yet.
