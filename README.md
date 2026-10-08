# Snake for the TI-84 Evo-T

A colour Snake game for the **TI-84 Evo-T** graphing calculator, written in Python.

> **Made with AI:** this game and this README were created with the help of AI (Claude by Anthropic).
> Everything was tested on a real TI-84 Evo-T.

## Features

- Eat the red food to grow
- A blue wall shows exactly where the map ends
- The snake gets faster as it grows
- **High score** that stays saved after you quit
- Start screen, pause and "play again"
- Quick turns are remembered, so fast key presses still work
- No flicker

## What you need

- A **TI-84 Evo-T** calculator
- A USB cable to connect it to your computer
- **Google Chrome** or **Microsoft Edge** (Safari and Firefox do not work with the TI tool)
- The file [`snake.py`](snake.py) from this repo

## Setup

1. Download [`snake.py`](snake.py) to your computer.
2. Connect the calculator to your computer with the USB cable.
   Leave the calculator on the **home screen**.
3. Open **https://connectevo.ti.com** in **Chrome** or **Edge**.
4. Connect to your calculator in the page and allow access when the browser asks.
5. Drag `snake.py` onto the page to send it to the calculator.
6. **Choose RAM** to play right away.
   The Python app on the Evo-T only shows files that are in RAM.
   (Want to keep the game safe? See [Don't lose the game](#dont-lose-the-game).)

> **Already sent it to Archive?** On the calculator press **2nd → mem → Mem Management**,
> find **SNAKE** and press **enter**. The `*` in front of the name disappears, which means
> it is now in RAM.

## Start the game

1. Open the **Python** app on the calculator.
2. Choose **SNAKE** and run it.
3. Press **enter** on the start screen.

## Don't lose the game

The Evo-T **deletes RAM** when it stays turned off for a while.
A normal turn-off is fine, but after some time the game is gone.

**Best way:**

1. Keep the game in **Archive**. Archive is never deleted.
2. Before playing, press **2nd → mem → Mem Management**, find **SNAKE** and press **enter**.
   The `*` disappears, which means the game is now in RAM.
3. Open the **Python** app and play.

Programs can't move files between Archive and RAM by themselves, so this step can't be automatic.
The high score list **SNAKE** is in RAM too, so it can be deleted the same way.

## Keys

| Key | What it does |
|---|---|
| ◀ ▶ ▲ ▼ | Turn |
| 2nd or mode | Pause (2nd or enter to go on) |
| clear | Quit |

## Rules

- Each food gives **10 points**.
- You lose if you hit a **wall** or **yourself**.
- You cannot turn straight back into yourself.

## High score

The best score is saved in a calculator list called **SNAKE**, so it stays after you quit.

- To reset the high score, delete the list **SNAKE** in **2nd → mem → Mem Management**.
- A calculator reset (RAM clear) also resets it.

## Good to know

- Keep `snake.py` on your computer too, so you can always send it again.
- Made for the TI-84 Evo-T. Other TI-84 models are not tested.
