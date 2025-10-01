from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, List, Sequence

import keyboard
import numpy as np
import pydirectinput
import pyautogui
from PIL import Image


pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0
pyautogui.PAUSE = 0


# Drawing configuration ---------------------------------------------------
scale = 2  # Matches the configured brush size inside Paint.
starting_X = 500
starting_Y = 300


@dataclass(frozen=True)
class PaletteEntry:
    name: str
    rgb: Sequence[int]
    screen_xy: Sequence[int]


PALETTE: List[PaletteEntry] = [
    PaletteEntry("black", (0, 0, 0), (792, 83)),
    PaletteEntry("grey", (127, 127, 127), (813, 84)),
    PaletteEntry("dark_red", (128, 0, 0), (837, 86)),
    PaletteEntry("red", (255, 0, 0), (868, 87)),
    PaletteEntry("orange", (255, 127, 0), (887, 86)),
    PaletteEntry("yellow", (255, 255, 0), (912, 86)),
    PaletteEntry("green", (0, 255, 0), (930, 86)),
    PaletteEntry("turquoise", (0, 191, 255), (957, 85)),
    PaletteEntry("indigo", (0, 0, 255), (980, 85)),
    PaletteEntry("purple", (128, 0, 128), (1004, 84)),
    PaletteEntry("white", (255, 255, 255), (788, 103)),
    PaletteEntry("light_grey", (192, 192, 192), (816, 106)),
    PaletteEntry("brown", (139, 69, 19), (842, 105)),
    PaletteEntry("rose", (255, 105, 180), (863, 105)),
    PaletteEntry("gold", (255, 215, 0), (886, 106)),
    PaletteEntry("light_yellow", (245, 245, 220), (906, 107)),
]


PALETTE_RGB = np.array([entry.rgb for entry in PALETTE], dtype=np.uint8)


stop_flag = False


def main() -> None:
    """Entry point used when the module is executed as a script."""

    global stop_flag
    file_path = "image.jpg"

    image = Image.open(file_path).convert("RGB")
    image.save("output.jpg", dpi=(72, 72))
    width, height = image.size
    colour_grid = quantise_image(image)

    print("Drawing started. Press F8 to stop.")
    draw_image(colour_grid, width, height)
    if stop_flag:
        print("Stopped drawing.")
    else:
        print("Drawing complete.")


def quantise_image(image: Image.Image) -> np.ndarray:
    """Map every pixel in *image* to the nearest palette entry."""

    pixels = np.asarray(image, dtype=np.uint8)
    flat_pixels = pixels.reshape(-1, 3).astype(np.int16, copy=False)
    palette_rgb = PALETTE_RGB.astype(np.int16, copy=False)
    diff = flat_pixels[:, None, :] - palette_rgb[None, :, :]
    squared = diff.astype(np.int32)
    distances = np.sum(squared * squared, axis=2, dtype=np.int32)
    nearest_indices = np.argmin(distances, axis=1)
    return nearest_indices.reshape(pixels.shape[:2])


def draw_image(colour_grid: np.ndarray, width: int, height: int) -> None:
    """Replay the quantised image in MS Paint using horizontal runs."""

    global stop_flag

    active_colour_index: int | None = None

    for y in range(height):
        if stop_flag:
            break
        screen_y = starting_Y + y * scale
        row = colour_grid[y]

        for colour_index, start_x, end_x in iter_runs(row):
            if stop_flag:
                break

            if active_colour_index != colour_index:
                select_palette_colour(colour_index)
                active_colour_index = colour_index

            draw_run(screen_y, start_x, end_x)


def iter_runs(row: np.ndarray) -> Iterator[tuple[int, int, int]]:
    """Yield (colour_index, start, end) for consecutive runs in *row*."""

    if len(row) == 0:
        return

    colour_index = row[0]
    run_start = 0

    for x in range(1, len(row)):
        if row[x] != colour_index:
            yield colour_index, run_start, x - 1
            colour_index = row[x]
            run_start = x

    yield colour_index, run_start, len(row) - 1


def select_palette_colour(colour_index: int) -> None:
    entry = PALETTE[colour_index]
    move_cursor(*entry.screen_xy)
    pydirectinput.click(button="left")


def draw_run(screen_y: int, start_x: int, end_x: int) -> None:
    start_screen_x = starting_X + start_x * scale
    end_screen_x = starting_X + end_x * scale + (scale - 1)

    move_cursor(start_screen_x, screen_y)
    pydirectinput.mouseDown()
    move_cursor(end_screen_x, screen_y)
    pydirectinput.mouseUp()


def move_cursor(x: int, y: int) -> None:
    pydirectinput.moveTo(x, y)


def stop() -> None:
    global stop_flag
    stop_flag = True


if __name__ == "__main__":
    keyboard.add_hotkey("f8", stop)
    main()
