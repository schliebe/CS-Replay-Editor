# CS Replay Editor
**Editor for Circuit Superstars replay files.**\
*Version 1.0.0*

## What is this?
This is a simple editor for replays of the game [**Circuit Superstars**](https://www.originalfiregames.com/circuit-superstars "Circuit Superstars") ([Steam](https://store.steampowered.com/app/1097130/Circuit_Superstars/ "Circuit Superstars on Steam")).\
This editor might be most useful for content creators or anyone else that wants to change how the replays look like.

You can edit existing replays, which are saved as a pair of .replay and .header files.
It is only possible to make cosmetic changes.

The editor is working for the current Early Access version `v.0.3.0`.

### What you can change
- Names of drivers\
  (Not visible when watching the replay)
- Suit and design of each driver
- Helmet and design of each driver
- Car, design and number of each driver\
  (Changing the car might result in weird looking behavior)

Suits, helmets, cars and designs can only be selected out of the options available in the game.

### What you can't change
- Idle and celebration animations, as you can't see them in the replay
- No custom suits, helmets, cars or designs not in the game
- No changes in what the cars actually do
- No changes in tracks or settings like number of laps, damage, etc.
- No changes in starting positions
- Anything else not in the lists above

### Planned features
- Possibility to load and save drivers and cars as presets
- Complete list of designs and their names
- Improved interface
- Design preview (maybe even with the selected colors)

### How to use
Make sure you have [Python 3 installed](https://www.python.org/downloads/ 'Install Python 3'). For development, version `3.7` was used but any other Python 3 version should work.\
To use the editor, just type the following into the command-line in the same directory as the script:
```shell
python CS_Replay_Editor.py
```
The main window should now open. You can also try to double click the script but there is no guarantee this works.

### Changelog
#### [1.0.0] - 2021-08-04
- First release
