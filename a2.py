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
        Updates fireball cards, draws a card, increases energy capacity by 1, and refills energy.
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
        Returns the symbol of this card.
        """
        return WYRM_SYMBOL
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        """
        Chooses the target entity for the Wyrm's effect.
        A Wyrm will choose the allied entity (including itself if on board) with the lowest health.
        If multiple entities have the lowest health, if one of the tied entities is the allied hero,
        the allied hero should be selected. Otherwise, the leftmost tied minion should be selected.
        """
        potential_targets = []
        
        # Create a list of all allied entities to consider
        all_allies = []
        if self in ally_minions: # Ensure the Wyrm itself is considered if it's on the board
            all_allies.extend(ally_minions)
        else: # If the Wyrm is not in ally_minions
            all_allies.append(self) # Add itself
            all_allies.extend(ally_minions) # Then other minions
        
        all_allies.append(ally_hero)

        if not all_allies:
            return None # Should not happen if Wyrm or hero exists

        min_health_entity = all_allies[0] # Start with the first ally

        for i in range(1, len(all_allies)):
            current_entity = all_allies[i]
            if current_entity.get_health() < min_health_entity.get_health():
                min_health_entity = current_entity
            elif current_entity.get_health() == min_health_entity.get_health():
                # Tie-breaking:
                # 1. If current_entity is Hero and min_health_entity is not Hero, prefer current_entity (Hero).
                if isinstance(current_entity, Hero) and not isinstance(min_health_entity, Hero):
                    min_health_entity = current_entity
                # 2. If both are Minions, min_health_entity (being earlier in the list) is already the leftmost.
                # 3. If min_health_entity is Hero and current_entity is Minion, keep Hero (already preferred).
                # No change needed for cases 2 and 3 due to iteration order and hero preference.
        
        return min_health_entity

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
        self.effect = {DAMAGE: self.health} 

    def get_effect(self) -> dict[str, int]:
        """
        Returns the effect of this card, with damage equal to current health.
        """
        return {DAMAGE: self.health} # Dynamically uses current health

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
        max_health_entity = enemy_hero
        for entity in enemy_minions:
            if entity.get_health() > max_health_entity.get_health():
                max_health_entity = entity
            elif entity.get_health() == max_health_entity.get_health():
                # If the health is the same, prefer the leftmost minion
                if isinstance(entity, Minion) and not isinstance(max_health_entity, Minion):
                    max_health_entity = entity
        return max_health_entity

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
            
            if card.get_effect():
                chosen_target_for_effect = card.choose_target(acting_hero, opponent_hero, acting_hero_minions, opponent_minions)
                if chosen_target_for_effect:
                    for effect_type, amount in card.get_effect().items():
                        if effect_type == DAMAGE: chosen_target_for_effect.apply_damage(amount)
                        elif effect_type == SHIELD: chosen_target_for_effect.apply_shield(amount)
                        elif effect_type == HEALTH: chosen_target_for_effect.apply_health(amount)
            
            self.remove_defeated_entities()
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
            
            if card.get_effect():
                chosen_target_for_effect = card.choose_target(acting_hero, opponent_hero, acting_hero_minions, opponent_minions)
                if chosen_target_for_effect:
                    for effect_type, amount in card.get_effect().items():
                        if effect_type == DAMAGE: chosen_target_for_effect.apply_damage(amount)
                        elif effect_type == SHIELD: chosen_target_for_effect.apply_shield(amount)
                        elif effect_type == HEALTH: chosen_target_for_effect.apply_health(amount)
            
            self.remove_defeated_entities()
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
            model_self.remove_defeated_entities()
            if target_entity and effect_dict:
                if HEALTH in effect_dict: target_entity.apply_health(effect_dict[HEALTH])
                if SHIELD in effect_dict: target_entity.apply_shield(effect_dict[SHIELD])
                if DAMAGE in effect_dict: target_entity.apply_damage(effect_dict[DAMAGE])
            model_self.remove_defeated_entities()

        # 1. Player's minions attack
        for minion in list(self.get_player_minions()): # Iterate copy as list might change
            if not minion.is_alive(): continue
            target = minion.choose_target(self.player, self.enemy, self.active_player_minions, self.active_enemy_minions)
            if target:
                apply_effects_and_handle_deaths(minion.get_effect(), target, self)
            if self.has_won() or self.has_lost(): return enemy_played_card_names

        # 2. Enemy hero: new turn sequence
        self.enemy.new_turn()
        if not self.enemy.is_alive(): return enemy_played_card_names # Check after draw

        # 3. Enemy hero plays cards
        still_can_play = True
        while still_can_play: # Loop to allow restarting hand scan
            if not self.enemy.is_alive(): break
            played_a_card_this_scan = False
            
            hand_index = 0
            while hand_index < len(self.enemy.get_hand()): # Iterate through current hand
                card_to_play = self.enemy.get_hand()[hand_index]

                if card_to_play.get_cost() > self.enemy.get_energy():
                    hand_index += 1
                    continue

                chosen_target_for_enemy_spell = None
                if not card_to_play.is_permanent(): # Spell card targeting
                    effect = card_to_play.get_effect()
                    if DAMAGE in effect and self.player.is_alive():
                        chosen_target_for_enemy_spell = self.player
                    elif self.enemy.is_alive(): # Otherwise, target self if alive
                        chosen_target_for_enemy_spell = self.enemy
                # For permanent cards, target for enemy_play_card is effectively the board slot;
                # on-play effects use minion's own choose_target.

                if self.enemy_play_card(card_to_play, chosen_target_for_enemy_spell):
                    enemy_played_card_names.append(card_to_play.get_name())
                    played_a_card_this_scan = True
                    # Successfully played a card, restart scan from the beginning of the (modified) hand
                    break  # Breaks from inner while (hand_index loop)
                else:
                    hand_index += 1 # Could not play this card, try next

            if not played_a_card_this_scan: # Full scan of hand, no card played
                still_can_play = False # Exit outer while loop

            if self.has_won() or self.has_lost(): return enemy_played_card_names
        
        # 4. Enemy's minions attack
        for minion in list(self.get_enemy_minions()): # Iterate copy
            if not minion.is_alive(): continue
            if not self.player.is_alive() and not any(m.is_alive() for m in self.active_player_minions): break # No valid targets
            target = minion.choose_target(self.enemy, self.player, self.active_enemy_minions, self.active_player_minions)
            if target:
                apply_effects_and_handle_deaths(minion.get_effect(), target, self)
            if self.has_won() or self.has_lost(): return enemy_played_card_names

        # 5. Player: new turn sequence (if game not over)
        if self.player.is_alive() and not (self.has_won() or self.has_lost()):
            self.player.new_turn()

        return enemy_played_card_names
    
# Task 12


def play_game(initial_save_file: str) -> None:
    """
    Constructs the Hearthstone controller and starts the game loop.
    """
    # controller = Hearthstone(initial_save_file)
    # controller.run_game_loop()



def main() -> None:
    """
    Main function to run the Hearthstone game simulation.
    """
    # Default initial file, can be changed or made configurable (e.g. sys.argv)
    initial_file = "levels/deck1.txt" 
    play_game(initial_file)


if __name__ == "__main__":
    main()