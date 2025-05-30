# DO NOT modify or add any import statements
from support import *
from display import HearthView

# Name: Dimas Gistha Adnyana
# Student Number: 49549236
# Favorite Building: Guggenheim Museum Builting
# -----------------------------------------------------------------------------

# Task 1
class Card():
    def __init__(self, **kwargs):
        """
        Initializes a card with the given attributes.
        """
        self.name = kwargs.get("_name", CARD_NAME)
        self.description = kwargs.get("_description", CARD_DESC)
        self.cost = kwargs.get("_cost", 1)
        self.effect = kwargs.get("_effect", {})
    def __str__(self) -> str:
        """
        Returns the name and description of this card
        """
        CARD_NAME = self.name
        CARD_DESC = self.description
        return f"{CARD_NAME}: {CARD_DESC}"
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted 
        into a REPL to construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}()"
    def get_symbol(self) -> str:
        """
        Returns the symbol of this card.
        """
        return CARD_SYMBOL
    def get_name(self) -> str:
        """
        Returns the name of this card.
        """
        return self.name
    def get_cost(self) -> int:
        """
        Returns the cost of this card.
        """
        return self.cost
    def get_effect(self) -> str:
        """
        Returns the effect of this card.
        """
        return self.effect
    def is_permanent(self) -> bool:
        """
        Returns True if this card is a permanent card.
        """
        return self.get_symbol() in [MINION_SYMBOL, RAPTOR_SYMBOL, WYRM_SYMBOL]
    
# Task 2
class Shield(Card):
    def __init__(self, **kwargs):
        """
        Initializes a shield card with the given attributes.
        """
        super().__init__(**kwargs)
        self.name = SHIELD_NAME
        self.description = SHIELD_DESC
        self.cost = 1
        self.effect = {SHIELD: 5}
    def get_symbol(self) -> str:
        """
        Returns the symbol of this card.
        """
        return SHIELD_SYMBOL

# Task 3
class Heal(Card):
    def __init__(self, **kwargs):
        """
        Initializes a heal card with the given attributes.
        """
        super().__init__(**kwargs)
        self.name = HEAL_NAME
        self.description = HEAL_DESC
        self.cost = 2
        self.effect = {HEALTH: 2}
    def get_symbol(self) -> str:
        """
        Returns the symbol of this card.
        """
        return HEAL_SYMBOL

# Task 4
class Fireball(Card):
    def __init__(self, turns_in_hand: int, **kwargs):
        """
        Initializes a fireball card with the given attributes.
        """
        super().__init__(**kwargs)
        self.turns_in_hand = turns_in_hand
        self.name = FIREBALL_NAME
        self.description = FIREBALL_DESC
        self.cost = 3
        self.effect = {DAMAGE: (3 + turns_in_hand)}
    def increment_turn(self) -> None:
        """
        Increments the number of turns this card has been in hand.
        """
        self.turns_in_hand += 1
        self.effect = {DAMAGE: (3 + self.turns_in_hand)}
    def get_symbol(self):
        return str(self.turns_in_hand)
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted 
        into a REPL to construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({self.turns_in_hand})"
    def __str__(self) -> str:
        """
        Returns the name and description of this card
        """
        CARD_NAME = self.name
        CARD_DESC = self.description
        return f"{CARD_NAME}: {CARD_DESC} Currently dealing {self.effect[DAMAGE]} damage."

# Task 5
class CardDeck():
    def __init__(self, cards: list[Card]):
        """
        Initializes a card deck with the given cards.
        """
        self.cards = cards
    def __str__(self) -> str:
        """
        Returns a comma separated list of the symbols 
        representing each card in the deck.
        """
        return ",".join([card.get_symbol() for card in self.cards]) 
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into 
        a REPL to construct a new instance identical to self.
        """
        return f"CardDeck({self.cards})"
    def is_empty(self) -> bool:
        """
        Returns True if this deck is empty.
        """
        return len(self.cards) == 0
    def remaining_count(self) -> int:
        """
        Returns the number of cards remaining in this deck.
        """
        return len(self.cards)
    def draw_cards(self, num: int) -> list[Card]:
        """
        Draws the specified number of cards from the top of the deck.
        """
        drawn_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return drawn_cards
    def add_card(self, card: Card) -> None:
        """
        Adds a card to the bottom of the deck.
        """
        self.cards.append(card)

# Task 6
class Entity(): 
    def __init__(self, health: int, shield: int):
        """
        Initializes an entity with the given health and shield.
        """
        self.health = health
        self.shield = shield
    def __repr__(self):
        """
        Returns a string which could be copied and pasted into 
        a REPL to construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({self.health}, {self.shield})"
    def __str__(self):
        """
        Returns this hero’s health and shield, comma separated.
        """
        return f"{self.health},{self.shield}"
    def get_health(self) -> int:
        """
        Returns the health of this entity.
        """
        return self.health
    def get_shield(self) -> int:
        """
        Returns the shield of this entity.
        """
        return self.shield
    def apply_shield(self, shield: int) -> None:
        """
        Applies the given shield to this entity.
        """
        self.shield += shield
    def apply_health(self, health: int) -> None:
        """
        Applies the given health to this entity.
        """
        self.health += health
    def apply_damage(self, damage: int) -> None:
        """
        Applies the given damage to this entity.
        """
        if self.shield > 0:
            if damage >= self.shield:
                damage -= self.shield
                self.shield = 0
            else:
                self.shield -= damage
                damage = 0
        if damage > 0:
            self.health -= damage
            if self.health < 0:
                self.health = 0
    def is_alive(self) -> bool:
        """
        Returns True if this entity is alive.
        """
        return self.health > 0

# Task 7
class Hero(Entity):
    """
    A Hero is an entity with energy, a deck, and a hand of cards. 
    It starts with max energy and can hold up to 5 cards in hand. 
    A hero is alive if its health and deck size are both above 0.
    """
    def __init__(self, health: int, shield: int, max_energy: int, deck: CardDeck, hand: list[Card]):
        """
        Initialize Hero with health, shield, energy, deck, and hand.
        """
        super().__init__(health, shield)
        self.max_energy = max_energy
        self.energy = max_energy
        self.deck = deck
        self.hand = hand
    def __str__(self) -> str:
        """
        Returns hero's health, shield, energy capacity, deck, and hand as a formatted string.
        """
        deck_str = str(self.deck)
        hand_str = ",".join([card.get_symbol() for card in self.hand])
        return f"{self.health},{self.shield},{self.max_energy};{deck_str};{hand_str}"
    def __repr__(self):
        """
        Returns a string which could be copied and pasted into 
        a REPL to construct a new instance identical to self.

        Expected Output: Hero(4, 5, 3, CardDeck([Card(), Card(), Shield(), Heal(), Fireball(6)]), [Heal(), Heal(), Fireball(2)])
        """
        return f"{self.__class__.__name__}({self.health}, {self.shield}, {self.max_energy}, {repr(self.deck)}, {self.hand})"
    def is_alive(self) -> bool:
        """
        Returns True if this entity is alive.
        """
        return self.health > 0 and self.deck.remaining_count() > 0
    def get_energy(self) -> int:
        """
        Returns this hero’s current energy level.
        """
        return self.energy
    def spend_energy(self, energy: int) -> None:
        """
        Tries to spend the specified energy. Returns True if successful, False otherwise.
        """
        if energy <= self.energy:
            self.energy -= energy
            return True
        return False
    def get_max_energy(self) -> int:
        """
        Returns this hero’s energy capacity.
        """
        return self.max_energy
    def get_deck(self) -> CardDeck:
        """
        Returns this hero’s deck.
        """
        return self.deck
    def get_hand(self) -> list[Card]:
        """
        Returns this hero’s hand.
        """
        return self.hand
    def new_turn(self) -> None:
        """
        Updates fireball cards, draws card, increases energy capacity by 1, and refills energy.
        """
        for card in self.hand:
            if card.name == FIREBALL_NAME:
                card.increment_turn()
        # Draw cards until hand is full or deck is empty
        while len(self.hand) < MAX_HAND:
            if self.deck.is_empty(): # Check if deck is empty before drawing
                break
            drawn_card_list = self.deck.draw_cards(1) # Returns a list
            self.hand.append(drawn_card_list[0]) # Append the card object itself

        self.max_energy += 1
        self.energy = self.max_energy

# Task 8
class Minion(Card, Entity):
    def __init__(self, health: int, shield: int):
        super().__init__(health = health, shield = shield)
        self.health = health
        self.shield = shield
        self.cost = 2
        self.name = MINION_NAME
        self.description = MINION_DESC
    def __str__(self) -> str:
        """
        Returns the name and description of this card
        """
        return f"{self.name}: {self.description}"
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into 
        a REPL to construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({self.health}, {self.shield})"
    def get_symbol(self) -> str:
        """
        Returns the symbol of this Minion.
        """
        return MINION_SYMBOL
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        """
        Chooses a target for the minion's attack. For a minion, this is always itself.
        """
        return self
    def get_symbol(self) -> str:
        """
        Returns the symbol of this card.
        """
        return MINION_SYMBOL

# Task 9
class Wyrm(Minion):
    """
    A Wyrm is a minion that has 2 cost, is represented by the symbol W, and whose effect is to apply 1 heal and 1 shield.
    When selecting a target entity, a Wyrm will choose the allied entity with the lowest health.
    If multiple entities have the lowest health, if one of the tied entities is the allied hero, the allied hero should be selected. Otherwise, the leftmost tied minion should be selected.
    """
    def __init__(self, health: int, shield: int):
        super().__init__(health, shield)
        self.name = WYRM_NAME
        self.description = WYRM_DESC
        self.cost = 2
        self.effect = {HEALTH: 1, SHIELD: 1}
    def get_symbol(self) -> str:
        """
        Returns the symbol of this Wyrm.
        """
        return WYRM_SYMBOL
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        """
        Chooses the target entity for the Wyrm's effect.
        A Wyrm will choose the allied entity (including itself if on board) with the lowest health.
        If multiple entities have the lowest health, if one of the tied entities is the allied hero,
        the allied hero should be selected. Otherwise, the leftmost tied minion should be selected.
        """
        all_ally_entities = [ally_hero] + ally_minions

        # Find the entity with the lowest health
        all_ally_entities_health = [e.get_health() for e in all_ally_entities]
        lowest_health = min(all_ally_entities_health)
        lowest_health_entities = [e for e in all_ally_entities if e.get_health() == lowest_health]
        if ally_hero in lowest_health_entities:
            # If the allied hero is among the lowest health entities, return it
            return ally_hero
        return lowest_health_entities[0]  # Return the leftmost minion with lowest health    

# Task 10
class Raptor(Minion):
    """
    A minion that has 2 cost, represented by R, and whose 
    effect is to apply damage equal to it's health
    """
    def __init__ (self, health: int, shield: int):
        super().__init__(health, shield)
        self.name = RAPTOR_NAME
        self.description = RAPTOR_DESC
        self.cost = 2

    def get_effect(self) -> dict[str, int]:
        """
        Returns the effect of this card, with damage equal to current health.
        """
        return {DAMAGE: self.get_health()} # Dynamically uses current health

    def get_symbol(self) -> str:
        """
        Returns the symbol of this card.
        """
        return RAPTOR_SYMBOL
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        """
        The Raptor will choose the enemy minion with the highest health. 
        If there is no such minion, select the enemy hero. Leftmost minion is selected in case of a tie.
        """
        if not enemy_minions:  # No enemy minions, target enemy hero
            return enemy_hero
        # Find the enemy minion with the highest health
        enemy_minions_health = [e.get_health() for e in enemy_minions]
        highest_health = max(enemy_minions_health)
        highest_health_entities = [e for e in enemy_minions if e.get_health() == highest_health]
        return highest_health_entities[0]  # Return the leftmost minion with highest health
    

# Task 11
class HearthModel():
    def __init__(self, player: Hero, active_player_minions: list[Minion], enemy: Hero, active_enemy_minions: list[Minion]):
        """
        Initializes HearthModel with player, enemy,
        and their active minions.
        """
        self.player = player
        self.active_player_minions = active_player_minions
        self.enemy = enemy
        self.active_enemy_minions = active_enemy_minions

    def __str__(self) -> str:
        """
        Returns a string representation of the game state.
        Format: player_hero|player_minions|enemy_hero|enemy_minions
        Minions: symbol,health,shield (semicolon separated list)
        """
        player_str = str(self.player)
        player_minions_str = ";".join([f"{minion.get_symbol()},{minion.get_health()},{minion.get_shield()}" for minion in self.active_player_minions])
        enemy_str = str(self.enemy)
        enemy_minions_str = ";".join([f"{minion.get_symbol()},{minion.get_health()},{minion.get_shield()}" for minion in self.active_enemy_minions])
        
        return f"{player_str}|{player_minions_str}|{enemy_str}|{enemy_minions_str}"

    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into
        a REPL to construct a new instance identical to self.
        """
        return (f"{self.__class__.__name__}({repr(self.player)}, {repr(self.active_player_minions)}, "
                f"{repr(self.enemy)}, {repr(self.active_enemy_minions)})")

    def get_player(self) -> Hero:
        """
        Returns the player.
        """
        return self.player

    def get_enemy(self) -> Hero:
        """
        Returns the enemy.
        """
        return self.enemy

    def get_player_minions(self) -> list[Minion]:
        """
        Returns the active player minions. Minions should appear in order
        from leftmost minion slot to rightmost minion slot.
        """
        return self.active_player_minions

    def get_enemy_minions(self) -> list[Minion]:
        """
        Returns the active enemy minions. Minions should appear in order
        from leftmost minion slot to rightmost minion slot.
        """
        return self.active_enemy_minions

    def has_won(self) -> bool:
        """
        Return true if and only if the player has won the game.
        """
        return not self.enemy.is_alive() and self.player.is_alive()

    def has_lost(self) -> bool:
        """
        Return true if and only if the player has lost the game.
        """
        return not self.player.is_alive()
    
    def remove_defeated_entities(self):
        """
        Removes defeated minions from both player's and enemy's active minion lists.
        """
        self.active_player_minions = [
            minion for minion in self.active_player_minions if minion.is_alive()
        ]
        self.active_enemy_minions = [
            minion for minion in self.active_enemy_minions if minion.is_alive()
        ]

    def play_card(self, card: Card, target: Entity) -> bool:
        """
        Attempts to play the specified card by the player.
        Returns True if successful, False otherwise.
        Implements minion slot replacement if board is full.
        """
        acting_hero = self.player
        
        if card.get_cost() > acting_hero.get_energy():
            return False

        acting_hero_minions = self.active_player_minions
        opponent_hero = self.enemy
        opponent_minions = self.active_enemy_minions

        if card.is_permanent():
            if len(acting_hero_minions) >= MAX_MINIONS:
                acting_hero_minions.pop(0) # Remove leftmost minion
            
            acting_hero.spend_energy(card.get_cost())
            if card in acting_hero.get_hand(): # Ensure card is in hand
                acting_hero.get_hand().remove(card)
            
            acting_hero_minions.append(card) # Add new minion to the right
            
            return True
        else: # Non-permanent card (spell)
            if not target: 
                return False # Spells generally need a target
            
            acting_hero.spend_energy(card.get_cost())
            if card in acting_hero.get_hand(): # Ensure card is in hand
                acting_hero.get_hand().remove(card)

            for effect_type, amount in card.get_effect().items():
                if effect_type == DAMAGE: target.apply_damage(amount)
                elif effect_type == SHIELD: target.apply_shield(amount)
                elif effect_type == HEALTH: target.apply_health(amount)
            
            self.remove_defeated_entities()
            return True
    
    def enemy_play_card(self, card: Card, target: Entity) -> bool:
        """
        Helper method for the enemy to play a card.
        Returns True if successful, False otherwise.
        Implements minion slot replacement if board is full.
        """
        acting_hero = self.enemy

        if card.get_cost() > acting_hero.get_energy():
            return False

        acting_hero_minions = self.active_enemy_minions
        opponent_hero = self.player
        opponent_minions = self.active_player_minions

        if card.is_permanent():
            if len(acting_hero_minions) >= MAX_MINIONS:
                acting_hero_minions.pop(0) # Remove leftmost minion
            
            acting_hero.spend_energy(card.get_cost())
            if card in acting_hero.get_hand(): # Ensure card is in hand
                acting_hero.get_hand().remove(card)

            acting_hero_minions.append(card) # Add new minion to the right
            
            return True
        else: # Non-permanent card (spell)
            if not target:
                return False # Spells generally need a target
            
            acting_hero.spend_energy(card.get_cost())
            if card in acting_hero.get_hand(): # Ensure card is in hand
                acting_hero.get_hand().remove(card)

            for effect_type, amount in card.get_effect().items():
                if effect_type == DAMAGE: target.apply_damage(amount)
                elif effect_type == SHIELD: target.apply_shield(amount)
                elif effect_type == HEALTH: target.apply_health(amount)
            
            self.remove_defeated_entities()
            return True

    

    def discard_card(self, card: Card) -> None:
        """
        Discards the specified card from the player's hand then
        add it to the bottom of the player’s deck
        """
        if card in self.player.get_hand():
            self.player.get_hand().remove(card)
            self.player.get_deck().add_card(card)


    def end_turn(self) -> list[str]:
        """
        Handles the sequence of actions at the end of a turn, including minion attacks
        and the enemy's turn.
        """
        enemy_played_card_names = []

        def apply_effects_and_handle_deaths(effect_dict: dict, target_entity: Entity, model_self: 'HearthModel'):
            if target_entity and effect_dict:
                if HEALTH in effect_dict: target_entity.apply_health(effect_dict[HEALTH])
                if SHIELD in effect_dict: target_entity.apply_shield(effect_dict[SHIELD])
                if DAMAGE in effect_dict: target_entity.apply_damage(effect_dict[DAMAGE])
            model_self.remove_defeated_entities()

        # 1. Player's minions attack
        for m in list(self.get_player_minions()): # Iterate copy as list might change
            if not m.is_alive(): continue
            target = m.choose_target(self.player, self.enemy, self.active_player_minions, self.active_enemy_minions)
            if target:
                apply_effects_and_handle_deaths(m.get_effect(), target, self)
            if self.has_won() or self.has_lost(): return enemy_played_card_names

        # Enemy hero: new turn sequence
        self.enemy.new_turn()
        
        # If the enemy hero is not alive after drawing cards, they do not take a turn.
        if not self.enemy.is_alive():
            return enemy_played_card_names
    

        # 3. Enemy hero plays cards
        still_can_play = True
        while still_can_play: 
            if not self.enemy.is_alive(): break # Stop if enemy becomes not alive during card play
            played_a_card_this_scan = False
            
            hand_index = 0
            while hand_index < len(self.enemy.get_hand()): 
                card_to_play = self.enemy.get_hand()[hand_index]

                if card_to_play.get_cost() > self.enemy.get_energy():
                    hand_index += 1
                    continue

                chosen_target_for_enemy_spell = None
                if not card_to_play.is_permanent(): 
                    effect = card_to_play.get_effect()
                    if DAMAGE in effect and self.player.is_alive():
                        chosen_target_for_enemy_spell = self.player
                    elif self.enemy.is_alive(): 
                        chosen_target_for_enemy_spell = self.enemy
                
                if self.enemy_play_card(card_to_play, chosen_target_for_enemy_spell):
                    enemy_played_card_names.append(card_to_play.get_name())
                    played_a_card_this_scan = True
                    break 
                else:
                    hand_index += 1 

            if not played_a_card_this_scan: 
                still_can_play = False 

            if self.has_won() or self.has_lost(): return enemy_played_card_names
        
        # 4. Enemy's minions attack
        for m in list(self.get_enemy_minions()): # Iterate copy
            if not m.is_alive(): continue
            # Ensure there's a valid target (player hero or player minions)
            if not self.player.is_alive() and not any(m.is_alive() for m in self.active_player_minions): break 
            target = m.choose_target(self.enemy, self.player, self.active_enemy_minions, self.active_player_minions)
            if target:
                apply_effects_and_handle_deaths(m.get_effect(), target, self)
            if self.has_won() or self.has_lost(): return enemy_played_card_names

        # 5. Player: new turn sequence (if game not over and player is alive)
        if self.player.is_alive() and not (self.has_won() or self.has_lost()):
            self.player.new_turn()

        return enemy_played_card_names
    
# Task 12

class Hearthstone():
    def __init__(self, file_path: str):
        """
        Instantiates the controller. Creates view and model instances.
        The model is instantiated with the game state from the given file.
        Minions not in a slot (deck/hand) are set to 1 health, 0 shield.
        Assumes the file exists and is valid.
        """
        self.filepath = file_path
        self.filepath_for_repr = file_path  # For repr

        self.model = self.load_model_from_file(file_path)
        self.view = HearthView()

    def _create_card_for_deck_hand(self, symbol: str) -> Card:
        """
        Creates a Card object from its symbol, for cards in deck or hand.
        Minions are initialized with 1 health and 0 shield.
        """
        if symbol == SHIELD_SYMBOL:
            return Shield()
        elif symbol == HEAL_SYMBOL:
            return Heal()
        elif symbol == RAPTOR_SYMBOL:
            return Raptor(1, 0)  # Not in a slot: 1 health, 0 shield
        elif symbol == WYRM_SYMBOL:
            return Wyrm(1, 0)    # Not in a slot: 1 health, 0 shield
        elif symbol == MINION_SYMBOL: # Generic Minion symbol
            return Minion(1, 0)  # Not in a slot: 1 health, 0 shield
        elif symbol.isdigit(): # Fireball
            return Fireball(int(symbol))


    def parse_deck_or_hand_from_str(self, cards_str: str) -> list[Card]:
        """
        Parses a string of card symbols (comma-separated) into a list of Card objects.
        """
        if not cards_str:
            return []
        
        symbols = cards_str.split(',')
        card_list = []
        for symbol in symbols:
            if symbol: # Ensure symbol is not empty string
                card_list.append(self._create_card_for_deck_hand(symbol))
        return card_list

    def create_minion_for_board(self, symbol: str, health: int, shield: int) -> Minion:
        """
        Creates a Minion object from its symbol, health, and shield for minions on board.
        """
        if symbol == RAPTOR_SYMBOL:
            minion = Raptor(health, shield)
        elif symbol == WYRM_SYMBOL:
            minion = Wyrm(health, shield)
        elif symbol == MINION_SYMBOL: # Generic Minion on board
            minion = Minion(health, shield)
        # Ensure health and shield are set correctly
        minion.health = health
        minion.shield = shield
        return minion

    def parse_minions_on_board_from_str(self, minions_str: str) -> list[Minion]:
        """
        Parses a string of active minions (semicolon-separated) into a list of Minion objects.
        Each minion format: "symbol,health,shield"
        """
        if not minions_str:
            return []

        minion_data_list = minions_str.split(';')
        active_minions = []
        for minion_data in minion_data_list:
            if minion_data: 
                parts = minion_data.split(',')
                symbol = parts[0]
                health = int(parts[1])
                shield = int(parts[2])
                active_minions.append(self.create_minion_for_board(symbol, health, shield))
        return active_minions

    def parse_hero_from_str(self, hero_data_str: str) -> Hero:
        """
        Parses a hero data string into a Hero object.
        Format: "health,shield,max_energy;deck_symbols_str;hand_symbols_str"
        """
        parts = hero_data_str.split(';')
        
        stats_str = parts[0]
        # Handle cases where deck or hand strings might be missing if hero_data_str is minimal
        deck_symbols_str = parts[1] if len(parts) > 1 and parts[1] else ""
        hand_symbols_str = parts[2] if len(parts) > 2 and parts[2] else ""

        stat_values = stats_str.split(',')
        health = int(stat_values[0])
        shield = int(stat_values[1])
        max_energy = int(stat_values[2])

        deck_cards = self.parse_deck_or_hand_from_str(deck_symbols_str)
        deck = CardDeck(deck_cards)
        
        hand_cards = self.parse_deck_or_hand_from_str(hand_symbols_str)

        return Hero(health, shield, max_energy, deck, hand_cards)

    def load_model_from_file(self, file_path: str) -> HearthModel:
        """
        Loads a HearthModel from the first line of the specified file.
        """
        with open(file_path, 'r') as f:
            content = f.readline().strip() # Read only the first line
        
        parts = content.split('|')
        player_hero_data_str = parts[0]
        player_minions_data_str = parts[1] if len(parts) > 1 and parts[1] else ""
        enemy_hero_data_str = parts[2] if len(parts) > 2 and parts[2] else ""
        enemy_minions_data_str = parts[3] if len(parts) > 3 and parts[3] else ""

        player_hero = self.parse_hero_from_str(player_hero_data_str)
        active_player_minions = self.parse_minions_on_board_from_str(player_minions_data_str)
        
        enemy_hero = self.parse_hero_from_str(enemy_hero_data_str)
        active_enemy_minions = self.parse_minions_on_board_from_str(enemy_minions_data_str)

        return HearthModel(player_hero, active_player_minions, enemy_hero, active_enemy_minions)

    def __str__(self) -> str:
        """Returns a human readable string stating that this is a game of Hearthstone using the current file path."""
        return CONTROLLER_DESC + self.filepath

    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into a REPL to construct a new instance identical to self.
        Satisfies Gradescope requirement for no quotes around the file path argument.
        """
        return f"Hearthstone({self.filepath_for_repr})"

    def update_display(self, messages: list[str]):
        """
        Update the display by printing out the current game state using HearthView.
        """
        player_hero = self.model.get_player()
        enemy_hero = self.model.get_enemy()
        player_minions = self.model.get_player_minions()
        enemy_minions = self.model.get_enemy_minions()

        self.view.update(
            player_hero,
            enemy_hero,
            player_minions,
            enemy_minions,
            messages
        )

    def get_command(self) -> str:
        """
        Repeatedly prompts the user until they enter a valid command.
        Returns the first valid command (lowercase) entered by the user.
        """
        while True:
            raw_input_str = input(COMMAND_PROMPT).strip()
            lower_input_str = raw_input_str.lower()

            # Check for exact match commands that take no variable arguments
            if lower_input_str == HELP_COMMAND or lower_input_str == END_TURN_COMMAND:
                return lower_input_str

            # If not an exact match, then check for commands that take arguments
            command_parts = lower_input_str.split(maxsplit=1)
            command_action = command_parts[0]
            argument = command_parts[1] if len(command_parts) > 1 else None

            if not argument: # Commands below here require an argument
                self.update_display([INVALID_COMMAND])
                continue

            if command_action == PLAY_COMMAND or command_action == DISCARD_COMMAND:
                if argument.isdigit():
                    card_pos = int(argument)
                    # Check against actual hand size
                    hand_size = len(self.model.get_player().get_hand())
                    if 1 <= card_pos <= hand_size:
                        return lower_input_str

            elif command_action == LOAD_COMMAND:
                return lower_input_str

            # If no valid command format was matched, it's invalid
            self.update_display([INVALID_COMMAND])


    def get_target_entity(self) -> str:
        """
        Repeatedly prompts the user until they enter a valid entity identifier.
        Returns the uppercase entity identifier string.
        """
        while True:
            identifier_input = input(ENTITY_PROMPT).strip().upper()

            if identifier_input == PLAYER_SELECT or identifier_input == ENEMY_SELECT:
                # Check if heroes are targetable (e.g., alive)
                # For simplicity and based on prompt, assume M/O are valid if entered.
                return identifier_input

            if identifier_input.isdigit():
                num = int(identifier_input)
                if 1 <= num <= MAX_MINIONS: # Enemy minion slots 1-5
                    idx = num - 1 # 0-indexed
                    if idx < len(self.model.get_enemy_minions()) and self.model.get_enemy_minions()[idx].is_alive():
                        return ENEMY_SELECT + str(idx)
                elif MAX_MINIONS < num <= MAX_MINIONS * 2: # Player minion slots 6-10
                    idx = num - MAX_MINIONS - 1 # 0-indexed for player minions list
                    if idx < len(self.model.get_player_minions()) and self.model.get_player_minions()[idx].is_alive():
                        return PLAYER_SELECT + str(idx)
            
            self.update_display([INVALID_ENTITY])
    # Add this entire method inside your Hearthstone class

    def get_entity_from_identifier(self, identifier: str) -> Entity | None:
        """
        Translates a string identifier into the corresponding Entity object.

        Args:
            identifier (str): The string identifier (e.g., 'M', 'O', 'M0', 'O2').

        Returns:
            Entity | None: The corresponding Hero or Minion object, or None if
                        the identifier is invalid.
        """
        if identifier == PLAYER_SELECT:
            return self.model.get_player()

        if identifier == ENEMY_SELECT:
            return self.model.get_enemy()

        # Check for minion identifiers (e.g., 'M0' or 'O2')
        if identifier.startswith(PLAYER_SELECT):
            try:
                # Extract the index from the identifier string (e.g., '0' from 'M0')
                index = int(identifier[len(PLAYER_SELECT):])
                player_minions = self.model.get_player_minions()
                if 0 <= index < len(player_minions):
                    return player_minions[index]
            except (ValueError, IndexError):
                return None # Invalid format or index

        if identifier.startswith(ENEMY_SELECT):
            try:
                # Extract the index from the identifier string (e.g., '2' from 'O2')
                index = int(identifier[len(ENEMY_SELECT):])
                enemy_minions = self.model.get_enemy_minions()
                if 0 <= index < len(enemy_minions):
                    return enemy_minions[index]
            except (ValueError, IndexError):
                return None # Invalid format or index

        return None # Identifier did not match any known format

    def save_game(self):
        """Writes the string representation of the current HearthModel to autosave.txt."""
        with open(SAVE_LOC, 'w') as f:
            f.write(str(self.model))
        

    def load_game(self, file_path: str):
        """
        Replaces the current model instance with a new one loaded from the file.
        Assumes file exists and is valid.
        """
        self.model = self.load_model_from_file(file_path)
        self.filepath = file_path
        self.filepath_for_repr = file_path # Update for repr

    def play(self):
        """Manages the main game loop and player interaction."""
        current_messages = [WELCOME_MESSAGE]

        while True:
            self.update_display(current_messages)
            current_messages = [] # Clear messages for the next action/turn

            if self.model.has_won():
                current_messages.append(WIN_MESSAGE)
                self.update_display(current_messages)
                break
            if self.model.has_lost():
                current_messages.append(LOSS_MESSAGE)
                self.update_display(current_messages)
                break

            full_command_str = self.get_command()
            command_parts = full_command_str.split(maxsplit=1)
            command_action = command_parts[0]
            argument = command_parts[1] if len(command_parts) > 1 else None

            if command_action == HELP_COMMAND:
                current_messages.extend(HELP_MESSAGES)
            elif command_action == END_TURN_COMMAND:
                played_card_names = self.model.end_turn()
                for name in played_card_names:
                    current_messages.append(ENEMY_PLAY_MESSAGE + name)
                self.save_game() # Save after turn ends
                current_messages.append(GAME_SAVE_MESSAGE)
            elif command_action == PLAY_COMMAND:
                card_idx_one_based = int(argument)
                card_idx_zero_based = card_idx_one_based - 1
                
                player_hand = self.model.get_player().get_hand()
                if 0 <= card_idx_zero_based < len(player_hand):
                    card_to_play = player_hand[card_idx_zero_based]
                    target_entity_object = None
                    
                    if not card_to_play.is_permanent(): # Spell card, needs a target
                        target_identifier = self.get_target_entity()
                        target_entity_object = self.get_entity_from_identifier(target_identifier)
                        if target_entity_object is None: # Should not occur if get_target_entity is robust
                             current_messages.append(INVALID_ENTITY)
                             continue # Restart command input

                    if self.model.play_card(card_to_play, target_entity_object):
                        current_messages.append(PLAY_MESSAGE + card_to_play.get_name())
                        self.save_game()
                        current_messages.append(GAME_SAVE_MESSAGE)
                    else:
                        current_messages.append(ENERGY_MESSAGE)
                else:
                    current_messages.append(INVALID_COMMAND) # Invalid card index
            
            elif command_action == DISCARD_COMMAND:
                card_idx_one_based = int(argument)
                card_idx_zero_based = card_idx_one_based - 1
                player_hand = self.model.get_player().get_hand()

                if 0 <= card_idx_zero_based < len(player_hand):
                    card_to_discard = player_hand[card_idx_zero_based]
                    # Ensure card is actually removed by model.discard_card before getting name
                    # Or get name first. Let's get name first.
                    card_name = card_to_discard.get_name()
                    self.model.discard_card(card_to_discard)
                    current_messages.append(DISCARD_MESSAGE + card_name)
                    self.save_game()
                    current_messages.append(GAME_SAVE_MESSAGE)
                else:
                    current_messages.append(INVALID_COMMAND) # Invalid card index

            elif command_action == LOAD_COMMAND:
                file_to_load = argument
                try:
                    self.load_game(file_to_load)
                    # Only add the success message if loading works
                    current_messages.append(GAME_LOAD_MESSAGE + file_to_load)
                except (FileNotFoundError, IndexError, ValueError):
                    # Catch errors from file not existing or being invalid.
                    # As per the spec, "nothing happens", so we just add a
                    # failure message for the user.
                    current_messages.append(LOAD_FAILURE_MESSAGE)


def play_game(initial_save_file: str) -> None:
    """
    Constructs the Hearthstone controller and starts the game loop.
    """
    controller = Hearthstone(initial_save_file)
    controller.play()



def main() -> None:
    """
    Main function to run the Hearthstone game simulation.
    """
    # Default initial file, can be changed or made configurable (e.g. sys.argv)
    initial_file = "levels/deck1.txt" 
    play_game(initial_file)


if __name__ == "__main__":
    main()