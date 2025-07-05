# Discord Anonymous Confession Bot

A Discord bot that enables anonymous confessions across multiple categories with admin configuration and moderation logging.

## Features

- 🎭 **Anonymous Confessions**: Users can send anonymous messages in different categories
- 📋 **Multiple Categories**: General, crush, truth or dare, and AMA confessions
- 🛠️ **Admin Configuration**: Administrators can set channels for each category
- 📝 **Moderation Logging**: Optional logging system for moderation purposes
- 💾 **Persistent Storage**: Channel configurations are saved to JSON file
- 🔒 **Privacy Protection**: Original messages are deleted immediately for anonymity

## Categories

1. **General Confessions** (`!confess`) - General anonymous confessions
2. **Crush Confessions** (`!confesscrush`) - Anonymous crush confessions  
3. **Truth or Dare** (`!truthordare`) - Anonymous truth or dare submissions
4. **Ask Me Anything** (`!askmeanything`) - Anonymous AMA questions

## Setup

### Prerequisites

- Python 3.8 or higher
- Discord bot token

### Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install discord.py
   ```

### Configuration

1. Create a Discord application and bot at https://discord.com/developers/applications
2. Copy the bot token
3. Set the bot token as an environment variable:
   ```bash
   export TOKEN=your_bot_token_here
   ```
   Or alternatively:
   ```bash
   export DISCORD_TOKEN=your_bot_token_here
   ```

### Bot Permissions

Make sure your bot has the following permissions:
- Read Messages
- Send Messages
- Manage Messages (to delete original confession messages)
- Add Reactions
- Use Slash Commands
- Send Messages in Threads (optional)

### Running the Bot

```bash
python main.py
