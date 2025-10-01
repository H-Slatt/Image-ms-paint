## How to run

1. Install the Python dependencies: `pip install pillow numpy pyautogui pydirectinput keyboard`.
2. Place the source image as `image.jpg` in the project directory (or adjust `file_path` in `main.py`).
3. Open Microsoft Paint, maximise the window and ensure the colour palette positions match the coordinates defined in `main.py`.
4. Select the pencil or brush tool and set its size equal to the `scale` constant (default 2 px).
5. Run the script: `python main.py`.
6. Press <kbd>F8</kbd> at any time to stop the drawing early.

The script pre-processes the image with vectorised colour matching and draws horizontal runs instead of individual pixels, dramatically reducing colour swaps and improving throughput.
