# Atlas Discord Bot

## Overview
The **Atlas Discord Bot** is a fun and interactive bot designed to play the classic game of Atlas on Discord. Created in 2022, this bot provides an engaging experience for both single-player and multiplayer modes. The bot leverages Python for its development and stores game data in JSON files.

## Features
- **Two Modes of Play:**
  - **Play With Bot (`^pwb`)**: Play against the bot in single-player mode.
  - **Play With Friends (`^play`)**: Challenge your friends in multiplayer mode.
- **Game Rules Enforcement:** Automatically checks if the entered place is valid and ensures players respond within the time limit.
- **Time-Limited Turns:** Players must respond within 10 seconds.
- **Error Tracking:** Keeps track of incorrect attempts with a three-cross (❌) system.
- **User-Friendly Commands:** Intuitive commands for seamless gameplay.
- **Emoji Enhancements:** Uses emojis to enhance user engagement and make interactions lively.

## Game Rules
- Enter a place from the last letter of the previously mentioned place within 10 seconds.
- If you fail to respond in time or enter an invalid place, you get a cross (❌).
- Accumulate three crosses (❌ ❌ ❌), and you lose the game.
- Enter `pass` if you don’t know a place or `quit` to exit the game.

## Bot Commands
### **Help Command**
```plaintext
Hello there! Here are all the commands you can use:

Rules
You have to enter a place from the last letter of the last entered place within 10 seconds. If you fail to do so, you get a cross (❌). If you get 3 crosses (❌ ❌ ❌), you lose. If you don’t know a place enter pass or if you want to quit, enter quit into the chat.

^pwb
To play atlas with me type this into the chat.

^play
To play atlas with your friends type this into the chat.
```

## Links
- **Invite the Bot:** [Click here to add the bot](https://tinyurl.com/bot-atlas)
- **Vote for the Bot:** [Vote on top.gg](https://top.gg/bot/929728088651227146/vote)

## Technical Details
- **Language:** Python
- **Database:** JSON (for storing game data)
- **Features:**
  - Input validation for place names
  - Time-based gameplay logic
  - Emoji-based interactions for a better user experience

## Future Improvements
- Transition from JSON to a database system (e.g., SQLite or MongoDB) for better data management.
- Add a leaderboard to track player scores globally.
- Implement more complex rules and variations of the Atlas game.
- Enhance multiplayer interactions with Discord buttons and more.


---
Enjoy playing Atlas on Discord and challenge yourself or your friends to win!

