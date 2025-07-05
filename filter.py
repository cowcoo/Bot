import json
import os

# Global banned words (you can expand this)
GLOBAL_BANNED_WORDS = [
    "slur1", "slur2", "offensivephrase", "hateword"
]

# File to store server-specific banned words
FILTER_FILE = "server_filters.json"

# Load server-specific filters
def load_filters():
    if os.path.exists(FILTER_FILE):
        with open(FILTER_FILE, "r") as f:
            return json.load(f)
    return {}

# Save server-specific filters
def save_filters(filters):
    with open(FILTER_FILE, "w") as f:
        json.dump(filters, f, indent=2)

# Check if a message is clean
def is_message_clean(message, guild_id):
    filters = load_filters()
    server_words = filters.get(str(guild_id), [])
    lowered = message.lower()

    for word in GLOBAL_BANNED_WORDS + server_words:
        if word in lowered:
            return False
    return True

# Add a word to a server's filter
def add_banned_word(guild_id, word):
    filters = load_filters()
    guild_id = str(guild_id)
    if guild_id not in filters:
        filters[guild_id] = []
    if word.lower() not in filters[guild_id]:
        filters[guild_id].append(word.lower())
        save_filters(filters)
        return True
    return False

# Remove a word from a server's filter
def remove_banned_word(guild_id, word):
    filters = load_filters()
    guild_id = str(guild_id)
    if guild_id in filters and word.lower() in filters[guild_id]:
        filters[guild_id].remove(word.lower())
        save_filters(filters)
        return True
    return False

# List banned words for a server
def list_banned_words(guild_id):
    filters = load_filters()
    return filters.get(str(guild_id), [])