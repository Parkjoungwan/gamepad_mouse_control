# Gamepad Mapper with Mouse, Scroll, Vibration & GUI

**Overview:**  
This project is designed for Windows and utilizes **pygame** to process gamepad inputs. The application allows smooth mouse cursor movement via the left joystick, scroll control via the right joystick, and button-triggered actions with vibration feedback. Additionally, a simple GUI (built with **tkinter**) displays the running status and key assignments, making it easy to exit the program.

---

## Features

- **Left Joystick (Mouse Movement):**  
  - Smooth, natural cursor movement using interpolation and deadzone filtering (deadzone set to 0.2).

- **Right Joystick (Scroll Control):**  
  - Cumulative scroll control to adjust scroll sensitivity while preventing excessive scrolling.

- **Button Mapping & Vibration Patterns:**  
  - **A Button (Button 0):** Executes a single mouse click and triggers one short vibration.  
  - **B Button (Button 1):** Executes a double click and triggers two short vibrations.  
  - **Y Button (Button 3):** Executes the Windows Task View (Win+Tab) command and triggers three short vibrations.

- **Vibration Feedback:**  
  - Uses pygame's `Joystick.rumble()` (available in pygame 2.0+) to provide tactile feedback.

- **Multithreaded Processing:**  
  - Separate threads handle left joystick movement, right joystick scrolling, and button input to ensure responsiveness without input interference.

- **GUI Control Panel:**  
  - A tkinter window displays a status message along with key assignments:  
    **Key Assignments:** A = Click, B = Double Click, Y = Win+Tab  
  - An "Exit" button is provided to easily terminate the application.

---

## Requirements

- Python 3.7 or later
- Windows operating system
- [pygame](https://www.pygame.org/docs/)
- [pyautogui](https://pyautogui.readthedocs.io/en/latest/)

---

## Installation and Running

1. **Install Python and Configure Environment Variables:**  
   - Download and install Python from the [official website](https://www.python.org/downloads/windows/).  
   - Ensure the **"Add Python to PATH"** option is selected during installation.

2. **Install Required Libraries:**  
   - Open a Command Prompt and run:
     ```
     pip install pygame pyautogui
     ```

3. **Download the Project Code:**  
   - Save the project code as `gamepad_mapper.py`.

4. **Run the Program:**  
   - In Command Prompt, navigate to the directory containing `gamepad_mapper.py` and run:
     ```
     python gamepad_mapper.py
     ```
   - A tkinter GUI control panel will appear showing the status and key assignments. Use the left joystick for mouse movement, the right joystick for scrolling, and the mapped buttons (A, B, Y) for the corresponding actions with vibration feedback.

---

## Building an EXE File (Deployment)

You can convert this script into a standalone executable using PyInstaller.

1. **Install PyInstaller:**
  ```
  pip install pyinstaller
  ```

2. **Build the EXE:**  
- Navigate to the directory containing `gamepad_mapper.py` and run:
  ```
  pyinstaller --onefile --noconsole gamepad_mapper.py
  ```
- The `--onefile` option bundles the application into a single executable, and `--noconsole` hides the console window during execution.

3. **Run the EXE:**  
- After building, the executable `gamepad_mapper.exe` will be located in the `dist` folder.  
- Running the EXE will launch the GUI control panel with key assignment information and allow you to exit the program via the "Exit" button.

---

## Configuration Options

You can adjust the following settings at the top of the script to tailor the behavior:

- **MOUSE_SENSITIVITY:**  
Controls the speed of mouse movement based on left joystick input.

- **SCROLL_SENSITIVITY:**  
Adjusts the responsiveness of scrolling from right joystick input.

- **DEADZONE_THRESHOLD:**  
Sets the deadzone value (currently 0.2) below which joystick inputs are ignored to prevent unintended movement.

- **SMOOTHING_FACTOR:**  
Determines the interpolation factor used for smoothing mouse movement transitions.

---

## References

- [pygame Official Documentation](https://www.pygame.org/docs/)
- [PyAutoGUI Official Documentation](https://pyautogui.readthedocs.io/en/latest/)

---

## License

This project is distributed under the MIT License.
