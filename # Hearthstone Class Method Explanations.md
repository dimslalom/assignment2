# Hearthstone Class Method Explanations

This document outlines the functionality of each method within the `Hearthstone` class, which acts as the controller for the game.

---

### `__init__(self, file_path: str)`
*   **Purpose:** Initializes a new `Hearthstone` game controller.
*   **Functionality:**
    *   Stores the provided `file_path` for current game state and for the `__repr__` method.
    *   Calls the private helper method `_load_model_from_file(file_path)` to parse the game state from the specified file and create a `HearthModel` instance. This model represents the current state of the game (heroes, minions, decks, hands).
    *   Instantiates `HearthView()`, which is responsible for displaying the game to the user.
    *   **Note on File Loading:** As per the requirements, this method assumes the `file_path` exists and contains valid game data. It does not perform error checking for file existence or format. Minions loaded from the file that are not in a minion slot (i.e., in a deck or hand) are initialized with 1 health and 0 shield by the helper parsing methods.

---

### `_create_card_for_deck_hand(self, symbol: str) -> Card`
*   **Purpose:** A private helper method to create `Card` objects based on their string symbol, specifically for cards that are part of a hero's deck or hand.
*   **Functionality:**
    *   Takes a `symbol` (e.g., "S" for Shield, "R" for Raptor, "0" for Fireball with 0 turns in hand) as input.
    *   Returns the corresponding `Card` subclass instance:
        *   `Shield()` for `SHIELD_SYMBOL`.
        *   `Heal()` for `HEAL_SYMBOL`.
        *   `Raptor(1, 0)` for `RAPTOR_SYMBOL` (1 health, 0 shield as it's not on board).
        *   `Wyrm(1, 0)` for `WYRM_SYMBOL` (1 health, 0 shield as it's not on board).
        *   `Minion(1, 0)` for `MINION_SYMBOL` (1 health, 0 shield as it's not on board).
        *   `Fireball(int(symbol))` if the symbol is a digit.
        *   Defaults to a generic `Card()` if the symbol is not specifically handled (though this path is less likely with valid input files).

---

### `_parse_deck_or_hand_from_str(self, cards_str: str) -> list[Card]`
*   **Purpose:** A private helper method to convert a comma-separated string of card symbols into a list of `Card` objects.
*   **Functionality:**
    *   Takes `cards_str` (e.g., "S,R,0,H") as input.
    *   If `cards_str` is empty, returns an empty list.
    *   Splits the string by commas to get individual symbols.
    *   For each symbol, it calls `_create_card_for_deck_hand(symbol)` to instantiate the card.
    *   Returns a list of these `Card` objects.

---

### `_create_minion_for_board(self, symbol: str, health: int, shield: int) -> Minion`
*   **Purpose:** A private helper method to create `Minion` objects that are already on the game board, using their symbol and current health/shield values.
*   **Functionality:**
    *   Takes a `symbol` (e.g., "R" for Raptor), `health`, and `shield` as input.
    *   Returns the corresponding `Minion` subclass instance (`Raptor`, `Wyrm`, or generic `Minion`) initialized with the given `health` and `shield`.
    *   It explicitly sets the `health` and `shield` attributes of the created minion to the provided values, ensuring they reflect the on-board state.

---

### `_parse_minions_on_board_from_str(self, minions_str: str) -> list[Minion]`
*   **Purpose:** A private helper method to convert a semicolon-separated string of minion data into a list of `Minion` objects currently on the board.
*   **Functionality:**
    *   Takes `minions_str` (e.g., "R,2,1;W,1,0") as input.
    *   If `minions_str` is empty, returns an empty list.
    *   Splits the string by semicolons to get individual minion data strings.
    *   Each minion data string (e.g., "R,2,1") is then split by commas to get its symbol, health, and shield.
    *   For each set of data, it calls `_create_minion_for_board(symbol, health, shield)` to instantiate the minion.
    *   Returns a list of these `Minion` objects.

---

### `_parse_hero_from_str(self, hero_data_str: str) -> Hero`
*   **Purpose:** A private helper method to parse a hero's complete data string into a `Hero` object.
*   **Functionality:**
    *   Takes `hero_data_str` (e.g., "10,5,3;S,R,0;H,W") as input.
    *   The string is split by semicolons into three parts:
        1.  Hero stats (health, shield, max_energy).
        2.  Deck card symbols.
        3.  Hand card symbols.
    *   Hero stats are parsed into integers.
    *   `_parse_deck_or_hand_from_str` is called for the deck and hand symbol strings to create lists of `Card` objects. The deck list is used to instantiate a `CardDeck`.
    *   Returns a new `Hero` object initialized with all the parsed data.

---

### `_load_model_from_file(self, file_path: str) -> HearthModel`
*   **Purpose:** A private helper method responsible for reading the game state from a file and constructing the `HearthModel`.
*   **Functionality:**
    *   Opens and reads the *first line* of the file specified by `file_path`.
    *   The line is expected to be a string representation of the entire game model, with parts separated by `|` (player hero, player minions, enemy hero, enemy minions).
    *   It splits this main string and then uses `_parse_hero_from_str` and `_parse_minions_on_board_from_str` to create the respective `Hero` and `Minion` list components.
    *   Finally, it instantiates and returns a `HearthModel` object with these parsed components.

---

### `__str__(self) -> str`
*   **Purpose:** Returns a human-readable string representation of the `Hearthstone` controller.
*   **Functionality:**
    *   Returns a string indicating that this is a game of Hearthstone and includes the file path that was used to initialize or load the current game state (e.g., "A game of HearthStone using: levels/deck1.txt"). It uses the `CONTROLLER_DESC` constant from `support.py`.

---

### `__repr__(self) -> str`
*   **Purpose:** Returns a string that, if executed, would reconstruct an identical `Hearthstone` controller instance.
*   **Functionality:**
    *   Returns a string in the format `Hearthstone(filepath)`, where `filepath` is the path to the game state file.
    *   **Note:** Specifically implemented to satisfy a Gradescope requirement where the filepath argument should *not* be enclosed in quotes (e.g., `Hearthstone(levels/deck1.txt)` instead of `Hearthstone("levels/deck1.txt")`).

---

### `update_display(self, messages: list[str])`
*   **Purpose:** Updates the game's visual display presented to the user.
*   **Functionality:**
    *   Calls the `display_game` method of its `self.view` (an instance of `HearthView`) object.
    *   Passes the current `self.model` (the game state) and a list of `messages` (strings to be shown to the player, like status updates or errors) to the view. The view then handles the rendering of the game board, heroes, minions, hands, and messages.

---

### `get_command(self) -> str`
*   **Purpose:** Prompts the user for a command and validates it, returning a valid command string in lowercase.
*   **Functionality:**
    *   Enters a loop, repeatedly displaying the `COMMAND_PROMPT` (from `support.py`) and reading user input.
    *   Converts the input to lowercase and splits it to separate the command action (e.g., "play", "load") from its argument (e.g., "1", "new_game.txt").
    *   Validates the command:
        *   `play` and `discard` require a numeric argument between 1 and `MAX_HAND`.
        *   `load` requires a non-empty argument (the filename).
        *   `help` and `end turn` should have no arguments.
    *   If the input is invalid, it calls `update_display` with the `INVALID_COMMAND` message and prompts again.
    *   Once a valid command is entered, the full command string (e.g., "play 1", "load myfile.txt", "help") is returned in lowercase.

---

### `get_target_entity(self) -> str`
*   **Purpose:** Prompts the user to select a target entity (hero or minion) and validates the selection.
*   **Functionality:**
    *   Enters a loop, repeatedly displaying the `ENTITY_PROMPT` (from `support.py`) and reading user input.
    *   Converts input to uppercase.
    *   Validates the input:
        *   `PLAYER_SELECT` ('M') or `ENEMY_SELECT` ('O') are valid for targeting heroes.
        *   Digits 1-`MAX_MINIONS` (e.g., 1-5) target enemy minions. The method checks if a minion exists at that 0-indexed slot and is alive. If valid, returns `ENEMY_SELECT` + 0-indexed position (e.g., "O0" for input "1").
        *   Digits `MAX_MINIONS`+1 to `MAX_MINIONS`*2 (e.g., 6-10) target player minions. The method checks if a minion exists at that 0-indexed slot (after subtracting `MAX_MINIONS`) and is alive. If valid, returns `PLAYER_SELECT` + 0-indexed position (e.g., "M0" for input "6").
    *   If the input is invalid (e.g., no minion at the specified slot, or non-recognized input), it calls `update_display` with the `INVALID_ENTITY` message and prompts again.
    *   Returns the validated target identifier string in uppercase (e.g., "M", "O", "O2", "M0").

---

### `_get_entity_from_identifier(self, identifier: str) -> Optional[Entity]`
*   **Purpose:** A private helper method to convert a valid target identifier string (obtained from `get_target_entity`) into the actual `Entity` object it refers to.
*   **Functionality:**
    *   Takes a target `identifier` string (e.g., "M", "O2").
    *   If "M", returns the player's hero object from the model.
    *   If "O", returns the enemy's hero object from the model.
    *   If it starts with "M" or "O" followed by a number (e.g., "M0", "O2"), it parses the index and attempts to retrieve the corresponding minion from the player's or enemy's active minion list in the model.
    *   Returns the `Entity` object or `None` if the identifier is malformed or the entity doesn't exist (though `get_target_entity` should prevent invalid identifiers from reaching here).

---

### `save_game(self)`
*   **Purpose:** Saves the current game state to a file.
*   **Functionality:**
    *   Opens the file specified by `SAVE_LOC` (from `support.py`, typically "autosave.txt") in write mode (overwriting existing content).
    *   Writes the string representation of the current `self.model` (obtained by `str(self.model)`) to this file.
    *   The specification implies no direct message output from this method itself; messages like "Game Saved." are handled in the `run_game_loop`.

---

### `load_game(self, file_path: str)`
*   **Purpose:** Loads a new game state from a specified file, replacing the current game model.
*   **Functionality:**
    *   Calls `_load_model_from_file(file_path)` to parse the new game state and create a new `HearthModel` instance.
    *   Assigns this new model to `self.model`.
    *   Updates `self.filepath` and `self.filepath_for_repr` to the new `file_path`.
    *   **Note on File Loading:** Similar to `__init__`, this method assumes the `file_path` exists and contains valid game data, without performing error checks.

---

### `run_game_loop(self)`
*   **Purpose:** Manages the primary interaction flow of the game.
*   **Functionality:**
    *   Initializes `current_messages` with `WELCOME_MESSAGE`.
    *   Enters a main `while True` loop that continues until the game ends.
    *   **Inside the loop:**
        1.  Calls `self.update_display(current_messages)` to show the current game state and any messages.
        2.  Clears `current_messages`.
        3.  Checks for win/loss conditions using `self.model.has_won()` and `self.model.has_lost()`. If the game is over, appends the appropriate win/loss message, updates the display one last time, and breaks the loop.
        4.  Calls `self.get_command()` to get a valid command from the player.
        5.  Processes the command:
            *   **help:** Appends `HELP_MESSAGES` to `current_messages`.
            *   **end turn:** Calls `self.model.end_turn()`, appends messages for any cards the enemy played, calls `self.save_game()`, and appends `GAME_SAVE_MESSAGE`.
            *   **play `X`:**
                *   Parses the card index `X`.
                *   Retrieves the card from the player's hand.
                *   If it's a spell (not permanent), calls `self.get_target_entity()` and then `_get_entity_from_identifier()` to determine the target.
                *   Calls `self.model.play_card()`.
                *   If successful, appends `PLAY_MESSAGE`, calls `self.save_game()`, and appends `GAME_SAVE_MESSAGE`.
                *   If unsuccessful (e.g., insufficient energy), appends `ENERGY_MESSAGE`.
                *   If card index is invalid, appends `INVALID_COMMAND`.
            *   **discard `X`:**
                *   Parses the card index `X`.
                *   Retrieves the card from the player's hand.
                *   Calls `self.model.discard_card()`.
                *   Appends `DISCARD_MESSAGE`, calls `self.save_game()`, and appends `GAME_SAVE_MESSAGE`.
                *   If card index is invalid, appends `INVALID_COMMAND`.
            *   **load `filepath`:**
                *   Calls `self.load_game(filepath)`.
                *   Appends `GAME_LOAD_MESSAGE`.

---