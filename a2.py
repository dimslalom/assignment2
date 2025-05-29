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
        # Add a name attribute for easier debugging, can be set by subclasses
        self.name_for_debug = self.__class__.__name__ 

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
        print(f"DEBUG_ENTITY: {self.name_for_debug} ({self.health}H,{self.shield}S) applying {shield}S. Old Shield: {self.shield}", end="")
        self.shield += shield
        print(f" -> New Shield: {self.shield}")
    def apply_health(self, health: int) -> None:
        """
        Applies the given health to this entity.
        """
        print(f"DEBUG_ENTITY: {self.name_for_debug} ({self.health}H,{self.shield}S) applying {health}H. Old Health: {self.health}", end="")
        self.health += health
        print(f" -> New Health: {self.health}")
    def apply_damage(self, damage: int) -> None:
        """
        Applies the given damage to this entity.
        """
        print(f"DEBUG_ENTITY: {self.name_for_debug} ({self.health}H,{self.shield}S) taking {damage}D. ", end="")
        original_damage = damage
        if self.shield > 0:
            if damage >= self.shield:
                damage_to_shield = self.shield
                damage -= self.shield
                self.shield = 0
                print(f"Shield broke ({damage_to_shield} absorbed). ", end="")
            else:
                self.shield -= damage
                print(f"Shield absorbed {damage}. Remaining Shield: {self.shield}. ", end="")
                damage = 0
        if damage > 0:
            self.health -= damage
            if self.health < 0:
                self.health = 0
            print(f"Health took {damage}. ", end="")
        print(f"-> Final State: {self.health}H,{self.shield}S")
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
        # For debugging, give heroes distinct names
        if not hasattr(self, 'name_for_debug_set'): # Avoid re-setting if called multiple times by mistake
            global _hero_debug_counter
            if '_hero_debug_counter' not in globals():
                _hero_debug_counter = 1
            self.name_for_debug = f"Hero{_hero_debug_counter}"
            _hero_debug_counter +=1
            self.name_for_debug_set = True
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
        print(f"DEBUG_HERO: {self.name_for_debug} new_turn starts. HP:{self.health}, Deck:{self.deck.remaining_count()}, Hand:{len(self.hand)} cards, Energy:{self.energy}/{self.max_energy}")
        for card in self.hand:
            if card.name == FIREBALL_NAME: # Make sure FIREBALL_NAME is defined
                print(f"DEBUG_HERO: {self.name_for_debug} incrementing Fireball {card} (turns: {card.turns_in_hand})")
                card.increment_turn()
        
        cards_to_draw_count = MAX_HAND - len(self.hand)
        if cards_to_draw_count > 0:
            print(f"DEBUG_HERO: {self.name_for_debug} attempting to draw {cards_to_draw_count} cards.")
            drawn_cards = self.deck.draw_cards(cards_to_draw_count)
            if drawn_cards:
                self.hand.extend(drawn_cards)
                print(f"DEBUG_HERO: {self.name_for_debug} drew {[c.get_symbol() for c in drawn_cards]}. Hand size now: {len(self.hand)}")
            else:
                print(f"DEBUG_HERO: {self.name_for_debug} drew no cards (deck empty or error).")
        else:
            print(f"DEBUG_HERO: {self.name_for_debug} hand full, not drawing.")

        self.max_energy += 1
        self.energy = self.max_energy
        print(f"DEBUG_HERO: {self.name_for_debug} new_turn ends. HP:{self.health}, Energy: {self.energy}/{self.max_energy}, Hand: {[c.get_symbol() for c in self.hand]}")

# Task 8
class Minion(Card, Entity):
    def __init__(self, health: int, shield: int):
        # Card.__init__(self) # Call Card's initializer
        # Entity.__init__(self, health, shield) # Explicitly call Entity's initializer
        # The super() call in your a2.py for Minion is: super().__init__(health = health, shield = shield)
        # This calls Card.__init__ which doesn't expect health/shield.
        # For robust initialization:
        Card.__init__(self) 
        Entity.__init__(self, health, shield)

        self.health = health # Explicitly set for Minion instance
        self.shield = shield # Explicitly set for Minion instance
        self.cost = 2
        self.name = MINION_NAME # Make sure MINION_NAME is defined
        self.description = MINION_DESC # Make sure MINION_DESC is defined
        
        # For debugging, give minions unique IDs or more descriptive names if needed
        global _minion_debug_counter
        if '_minion_debug_counter' not in globals():
            _minion_debug_counter = 1
        self.debug_id = _minion_debug_counter
        _minion_debug_counter += 1
        self.name_for_debug = f"{self.name}{self.debug_id}"


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
        print(f"DEBUG_MINION: Generic Minion {self.name_for_debug} ({self.health}H,{self.shield}S) choose_target (default: self).")
        return self

# Task 9
class Wyrm(Minion):
    """
    A Wyrm is a minion that has 2 cost, is represented by the symbol W, and whose effect is to apply 1 heal and 1 shield.
    When selecting a target entity, a Wyrm will choose the allied entity with the lowest health.
    If multiple entities have the lowest health, if one of the tied entities is the allied hero, the allied hero should be selected. Otherwise, the leftmost tied minion should be selected.
    """
    def __init__(self, health: int, shield: int):
        super().__init__(health, shield)
        self.name = WYRM_NAME # Make sure WYRM_NAME is defined
        self.description = WYRM_DESC # Make sure WYRM_DESC is defined
        self.cost = 2
        self.effect = {HEALTH: 1, SHIELD: 1}
        self.name_for_debug = f"Wyrm{self.debug_id}"


    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        """
        Chooses the target entity for the Wyrm's effect.
        """
        print(f"DEBUG_WYRM: {self.name_for_debug} ({self.health}H,{self.shield}S) choosing target for on-play/effect.")
        print(f"  Ally Hero: {ally_hero.name_for_debug} ({ally_hero.get_health()}H,{ally_hero.get_shield()}S)")
        print(f"  Ally Minions on board (passed to choose_target): {[f'{m.name_for_debug}({m.get_health()}H,{m.get_shield()}S)' for m in ally_minions]}")
        
        # Ensure 'self' (this Wyrm instance) is considered if it's in ally_minions
        # The list `ally_minions` passed when a card is played should already contain the new Wyrm.
        all_ally_entities = [ally_hero] + ally_minions 

        all_ally_entities_health = [e.get_health() for e in all_ally_entities]
        if not all_ally_entities_health: # Should not happen if hero is always there
            print(f"DEBUG_WYRM: No allied entities to target!")
            return None
        lowest_health = min(all_ally_entities_health)
        
        lowest_health_entities = [e for e in all_ally_entities if e.get_health() == lowest_health]
        print(f"DEBUG_WYRM: Lowest health found: {lowest_health}. Entities with lowest health: {[f'{e.name_for_debug}({e.get_health()}H)' for e in lowest_health_entities]}")

        chosen_target = None
        if ally_hero in lowest_health_entities:
            chosen_target = ally_hero
            print(f"DEBUG_WYRM: Allied hero is among lowest health, targeting Hero {chosen_target.name_for_debug}.")
        elif lowest_health_entities: # If hero not chosen, and there are low health entities
            chosen_target = lowest_health_entities[0] # Leftmost (hero was first, then minions in order)
            print(f"DEBUG_WYRM: Hero not chosen or not lowest. Targeting leftmost lowest: {chosen_target.name_for_debug} ({chosen_target.get_health()}H).")
        else:
            print(f"DEBUG_WYRM: No target found (this should be rare).")
            return None # Should ideally not happen if hero is always an option

        return chosen_target

# Task 10
class Raptor(Minion):
    """
    A minion that has 2 cost, represented by R, and whose 
    effect is to apply damage equal to it's health
    """
    def __init__ (self, health: int, shield: int):
        super().__init__(health, shield)
        self.name = RAPTOR_NAME # Make sure RAPTOR_NAME is defined
        self.description = RAPTOR_DESC # Make sure RAPTOR_DESC is defined
        self.cost = 2
        # self.effect = {DAMAGE: self.health} # Effect is dynamic via get_effect()
        self.name_for_debug = f"Raptor{self.debug_id}"


    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        """
        The Raptor will choose the enemy minion with the highest health. 
        """
        print(f"DEBUG_RAPTOR: {self.name_for_debug} ({self.health}H,{self.shield}S) choosing attack target.")
        living_enemy_minions = [m for m in enemy_minions if m.is_alive()]
        print(f"  Enemy Hero: {enemy_hero.name_for_debug} ({enemy_hero.get_health()}H,{enemy_hero.get_shield()}S)")
        print(f"  Living Enemy Minions: {[f'{m.name_for_debug}({m.get_health()}H,{m.get_shield()}S)' for m in living_enemy_minions]}")

        if not living_enemy_minions:
            print(f"DEBUG_RAPTOR: No enemy minions, targeting enemy hero {enemy_hero.name_for_debug}.")
            return enemy_hero
        
        highest_health_minion = living_enemy_minions[0]
        for m in living_enemy_minions[1:]:
            if m.get_health() > highest_health_minion.get_health():
                highest_health_minion = m
        
        print(f"DEBUG_RAPTOR: Targeting highest health enemy minion: {highest_health_minion.name_for_debug} ({highest_health_minion.get_health()}H).")
        return highest_health_minion
    
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
        print(f"DEBUG_MODEL: remove_defeated_entities called.")
        orig_player_minions_count = len(self.active_player_minions)
        orig_enemy_minions_count = len(self.active_enemy_minions)

        self.active_player_minions = [
            minion for minion in self.active_player_minions if minion.is_alive()
        ]
        self.active_enemy_minions = [
            minion for minion in self.active_enemy_minions if minion.is_alive()
        ]
        if len(self.active_player_minions) != orig_player_minions_count:
            print(f"  Player minions removed. New count: {len(self.active_player_minions)}")
        if len(self.active_enemy_minions) != orig_enemy_minions_count:
            print(f"  Enemy minions removed. New count: {len(self.active_enemy_minions)}")


    def play_card(self, card: Card, target: Entity) -> bool:
        """
        Attempts to play the specified card by the player.
        """
        acting_hero = self.player
        hero_name = acting_hero.name_for_debug
        print(f"DEBUG_MODEL ({hero_name}): Attempting to play card {card.get_name()}({card.get_symbol()}) (Cost: {card.get_cost()}). Energy: {acting_hero.get_energy()}")
        
        if card.get_cost() > acting_hero.get_energy():
            print(f"DEBUG_MODEL ({hero_name}): Not enough energy for {card.get_name()}.")
            return False

        acting_hero_minions = self.active_player_minions
        opponent_hero = self.enemy
        opponent_minions = self.active_enemy_minions

        # This part is from your a2.py, ensure it's correct for your logic
        if card.is_permanent(): # Minion
            print(f"DEBUG_MODEL ({hero_name}): Playing minion {card.get_name()}. Board size: {len(acting_hero_minions)}/{MAX_MINIONS}")
            if len(acting_hero_minions) >= MAX_MINIONS:
                removed_minion = acting_hero_minions.pop(0) # Remove leftmost minion
                print(f"DEBUG_MODEL ({hero_name}): Board full. Removed leftmost minion: {removed_minion.name_for_debug}")
            
            acting_hero.spend_energy(card.get_cost())
            if card in acting_hero.get_hand(): 
                acting_hero.get_hand().remove(card)
                print(f"DEBUG_MODEL ({hero_name}): Removed {card.get_name()} from hand.")
            else:
                print(f"DEBUG_MODEL ({hero_name}): WARNING - Card {card.get_name()} not found in hand to remove.")

            # IMPORTANT: The 'card' from hand is a Card instance. If it's a MinionCard, you need to create a Minion instance.
            # Your current code appends 'card' (which is a Card type) to acting_hero_minions.
            # This will cause issues if acting_hero_minions expects Minion instances with Entity properties.
            # Assuming 'card' is already a Minion instance if is_permanent() is true, as per your structure.
            # If 'card' is a 'MinionCard' from hand, it should be converted to a 'Minion' for the board.
            # For now, I'll follow your existing structure:
            actual_minion_to_play = card 
            acting_hero_minions.append(actual_minion_to_play) 
            print(f"DEBUG_MODEL ({hero_name}): Added {actual_minion_to_play.name_for_debug} to board. Board: {[m.name_for_debug for m in acting_hero_minions]}")
            
            # On-play effect
            # The get_effect() on a Minion in your code is its attack effect.
            # Wyrm redefines get_effect() to be its on-play. This is inconsistent.
            # Let's assume card.get_effect() is the on-play effect for now.
            on_play_effect_data = actual_minion_to_play.get_effect() 
            if on_play_effect_data:
                print(f"DEBUG_MODEL ({hero_name}): Minion {actual_minion_to_play.name_for_debug} has on-play effect: {on_play_effect_data}")
                # The choose_target for a Wyrm is its on-play target logic.
                # For a generic Minion, choose_target returns self.
                chosen_target_for_effect = actual_minion_to_play.choose_target(acting_hero, opponent_hero, acting_hero_minions, opponent_minions)
                
                if chosen_target_for_effect:
                    print(f"DEBUG_MODEL ({hero_name}): On-play target for {actual_minion_to_play.name_for_debug} is {chosen_target_for_effect.name_for_debug}")
                    for effect_type, amount in on_play_effect_data.items():
                        print(f"  Applying on-play {effect_type}: {amount} to {chosen_target_for_effect.name_for_debug}")
                        if effect_type == DAMAGE: chosen_target_for_effect.apply_damage(amount)
                        elif effect_type == SHIELD: chosen_target_for_effect.apply_shield(amount)
                        elif effect_type == HEALTH: chosen_target_for_effect.apply_health(amount)
                else:
                    print(f"DEBUG_MODEL ({hero_name}): Minion {actual_minion_to_play.name_for_debug} on-play chose NO target.")
            
            self.remove_defeated_entities()
            print(f"DEBUG_MODEL ({hero_name}): Finished playing minion {card.get_name()}. Energy left: {acting_hero.get_energy()}")
            return True
        else: # Non-permanent card (spell)
            print(f"DEBUG_MODEL ({hero_name}): Playing spell {card.get_name()}. Target: {target.name_for_debug if target else 'None'}")
            if not target: 
                print(f"DEBUG_MODEL ({hero_name}): Spell {card.get_name()} requires a target but none provided.")
                return False 
            
            acting_hero.spend_energy(card.get_cost())
            if card in acting_hero.get_hand():
                acting_hero.get_hand().remove(card)
                print(f"DEBUG_MODEL ({hero_name}): Removed {card.get_name()} from hand.")
            else:
                 print(f"DEBUG_MODEL ({hero_name}): WARNING - Card {card.get_name()} not found in hand to remove.")

            spell_effect_data = card.get_effect()
            print(f"DEBUG_MODEL ({hero_name}): Applying spell effect {spell_effect_data} to {target.name_for_debug}")
            for effect_type, amount in spell_effect_data.items():
                if effect_type == DAMAGE: target.apply_damage(amount)
                elif effect_type == SHIELD: target.apply_shield(amount)
                elif effect_type == HEALTH: target.apply_health(amount)
            
            self.remove_defeated_entities()
            print(f"DEBUG_MODEL ({hero_name}): Finished playing spell {card.get_name()}. Energy left: {acting_hero.get_energy()}")
            return True
    
    def enemy_play_card(self, card: Card, target: Entity) -> bool:
        """
        Helper method for the enemy to play a card.
        """
        acting_hero = self.enemy
        hero_name = acting_hero.name_for_debug # Should be "EnemyHero" or similar
        print(f"DEBUG_MODEL ({hero_name}): Attempting to play card {card.get_name()}({card.get_symbol()}) (Cost: {card.get_cost()}). Energy: {acting_hero.get_energy()}")

        if card.get_cost() > acting_hero.get_energy():
            print(f"DEBUG_MODEL ({hero_name}): Not enough energy for {card.get_name()}.")
            return False

        acting_hero_minions = self.active_enemy_minions
        opponent_hero = self.player
        opponent_minions = self.active_player_minions
        
        # Logic mirrors play_card, ensure consistency
        if card.is_permanent(): # Minion
            print(f"DEBUG_MODEL ({hero_name}): Playing minion {card.get_name()}. Board size: {len(acting_hero_minions)}/{MAX_MINIONS}")
            if len(acting_hero_minions) >= MAX_MINIONS:
                removed_minion = acting_hero_minions.pop(0)
                print(f"DEBUG_MODEL ({hero_name}): Board full. Removed leftmost minion: {removed_minion.name_for_debug}")
            
            acting_hero.spend_energy(card.get_cost())
            # Card removal from hand is handled by the caller loop in end_turn for enemy
            # if card in acting_hero.get_hand(): acting_hero.get_hand().remove(card) 
            
            actual_minion_to_play = card # Assuming card is already a Minion instance
            acting_hero_minions.append(actual_minion_to_play)
            print(f"DEBUG_MODEL ({hero_name}): Added {actual_minion_to_play.name_for_debug} to board. Board: {[m.name_for_debug for m in acting_hero_minions]}")
            
            on_play_effect_data = actual_minion_to_play.get_effect()
            if on_play_effect_data:
                print(f"DEBUG_MODEL ({hero_name}): Minion {actual_minion_to_play.name_for_debug} has on-play effect: {on_play_effect_data}")
                # CRITICAL DEBUG FOR WYRM ON-PLAY
                if isinstance(actual_minion_to_play, Wyrm):
                    print(f"CRITICAL_DEBUG ({hero_name}): Wyrm {actual_minion_to_play.name_for_debug} is being played.")
                    print(f"  Current {hero_name} HP: {acting_hero.get_health()}")
                    print(f"  Current {hero_name} Minions on board (before this Wyrm's choose_target): {[f'{m.name_for_debug}({m.get_health()}H,{m.get_shield()}S)' for m in acting_hero_minions]}")

                chosen_target_for_effect = actual_minion_to_play.choose_target(acting_hero, opponent_hero, acting_hero_minions, opponent_minions)
                
                if chosen_target_for_effect:
                    print(f"DEBUG_MODEL ({hero_name}): On-play target for {actual_minion_to_play.name_for_debug} is {chosen_target_for_effect.name_for_debug} ({chosen_target_for_effect.get_health()}H)")
                    for effect_type, amount in on_play_effect_data.items():
                        print(f"  Applying on-play {effect_type}: {amount} to {chosen_target_for_effect.name_for_debug}")
                        if effect_type == DAMAGE: chosen_target_for_effect.apply_damage(amount)
                        elif effect_type == SHIELD: chosen_target_for_effect.apply_shield(amount)
                        elif effect_type == HEALTH: chosen_target_for_effect.apply_health(amount)
                else:
                    print(f"DEBUG_MODEL ({hero_name}): Minion {actual_minion_to_play.name_for_debug} on-play chose NO target.")
            
            self.remove_defeated_entities()
            print(f"DEBUG_MODEL ({hero_name}): Finished playing minion {card.get_name()}. Energy left: {acting_hero.get_energy()}")
            return True
        else: # Non-permanent card (spell)
            print(f"DEBUG_MODEL ({hero_name}): Playing spell {card.get_name()}. Target: {target.name_for_debug if target else 'None'}")
            if not target:
                print(f"DEBUG_MODEL ({hero_name}): Spell {card.get_name()} requires a target but none provided.")
                return False
            
            acting_hero.spend_energy(card.get_cost())
            # Card removal from hand is handled by the caller loop in end_turn for enemy
            # if card in acting_hero.get_hand(): acting_hero.get_hand().remove(card)

            spell_effect_data = card.get_effect()
            print(f"DEBUG_MODEL ({hero_name}): Applying spell effect {spell_effect_data} to {target.name_for_debug}")
            for effect_type, amount in spell_effect_data.items():
                if effect_type == DAMAGE: target.apply_damage(amount)
                elif effect_type == SHIELD: target.apply_shield(amount)
                elif effect_type == HEALTH: target.apply_health(amount)
            
            self.remove_defeated_entities()
            print(f"DEBUG_MODEL ({hero_name}): Finished playing spell {card.get_name()}. Energy left: {acting_hero.get_energy()}")
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
        print("\nDEBUG_MODEL: ===== End Turn Initiated =====")
        print(f"DEBUG_MODEL (Start of End Turn): Player: {self.player.name_for_debug} HP: {self.player.get_health()}, Enemy: {self.enemy.name_for_debug} HP: {self.enemy.get_health()}")
        print(f"  Player Minions: {[f'{m.name_for_debug}({m.get_health()}H,{m.get_shield()}S)' for m in self.active_player_minions]}")
        print(f"  Enemy Minions: {[f'{m.name_for_debug}({m.get_health()}H,{m.get_shield()}S)' for m in self.active_enemy_minions]}")

        enemy_played_card_names = []

        # Local helper for effect application
        def apply_effects_and_handle_deaths_local(effect_dict: dict, target_entity: Entity, source_description: str, model_self: 'HearthModel'):
            if target_entity and effect_dict:
                print(f"DEBUG_MODEL: Applying effect {effect_dict} from {source_description} to {target_entity.name_for_debug} ({target_entity.get_health()}H,{target_entity.get_shield()}S)")
                # Direct application using Entity methods which now have prints
                if HEALTH in effect_dict: target_entity.apply_health(effect_dict[HEALTH])
                if SHIELD in effect_dict: target_entity.apply_shield(effect_dict[SHIELD])
                if DAMAGE in effect_dict: target_entity.apply_damage(effect_dict[DAMAGE])
                print(f"  Target {target_entity.name_for_debug} after effect: {target_entity.get_health()}H,{target_entity.get_shield()}S")
            else:
                print(f"DEBUG_MODEL: No target or no effect for {source_description}.")
            model_self.remove_defeated_entities()

        # 1. Player's minions attack
        print("\nDEBUG_MODEL: --- 1. Player's minions attack ---")
        for minion in list(self.get_player_minions()): 
            if not minion.is_alive():
                print(f"DEBUG_MODEL: Player's {minion.name_for_debug} is not alive, skipping attack.")
                continue
            print(f"DEBUG_MODEL: Player's {minion.name_for_debug} ({minion.get_health()}H,{minion.get_shield()}S) attacking.")
            # Minion.choose_target returns self. Wyrm.choose_target is on-play. Raptor.choose_target is attack.
            # This part needs to be very clear about what 'choose_target' and 'get_effect' mean for each minion type in attack context.
            # Your current Wyrm.choose_target is for on-play. If called here, it targets an ALLY.
            # Your current Wyrm.get_effect is {HEALTH:1, SHIELD:1}.
            # This means player's Wyrm will HEAL/SHIELD an ALLY when it "attacks".
            target = minion.choose_target(self.player, self.enemy, self.active_player_minions, self.active_enemy_minions)
            
            if target:
                minion_attack_effect = minion.get_effect() # This is {HEALTH:1,SHIELD:1} for Wyrm, {DAMAGE:health} for Raptor
                print(f"  Player's {minion.name_for_debug} chose target: {target.name_for_debug} ({target.get_health()}H) with effect {minion_attack_effect}")
                apply_effects_and_handle_deaths_local(minion_attack_effect, target, f"Player's {minion.name_for_debug} attack", self)
            else:
                print(f"  Player's {minion.name_for_debug} chose no target.")
            if self.has_won() or self.has_lost():
                print("DEBUG_MODEL: Game ended after player's minion attacks.")
                return enemy_played_card_names
        self.remove_defeated_entities() 

        # 2. Enemy hero: new turn sequence
        print(f"\nDEBUG_MODEL: --- 2. Enemy hero ({self.enemy.name_for_debug}): new turn sequence ---")
        print(f"  Enemy HP before new_turn: {self.enemy.get_health()}, Deck: {self.enemy.deck.remaining_count()}, IsAlive: {self.enemy.is_alive()}")
        self.enemy.new_turn() # This has its own debug prints
        print(f"  Enemy HP after new_turn: {self.enemy.get_health()}, Energy: {self.enemy.get_energy()}/{self.enemy.get_max_energy()}, IsAlive: {self.enemy.is_alive()}")
        
        if not self.enemy.is_alive():
            print("DEBUG_MODEL: Enemy hero is not alive after new_turn. Skipping enemy turn.")
            return enemy_played_card_names

        # 3. Enemy hero plays cards
        print(f"\nDEBUG_MODEL: --- 3. Enemy hero ({self.enemy.name_for_debug}) plays cards ---")
        print(f"  Enemy hand before playing: {[c.get_name() for c in self.enemy.get_hand()]}, Energy: {self.enemy.get_energy()}")
        still_can_play = True
        while still_can_play: 
            if not self.enemy.is_alive():
                print("DEBUG_MODEL: Enemy hero became not alive during card play loop. Stopping.")
                break 
            
            played_a_card_this_scan = False
            
            # Iterate over a copy of the hand indices because hand can change
            current_hand_indices = list(range(len(self.enemy.get_hand())))
            
            for hand_idx_pos, original_hand_idx in enumerate(current_hand_indices):
                if original_hand_idx >= len(self.enemy.get_hand()): # Card was removed, skip
                    continue
                card_to_play = self.enemy.get_hand()[original_hand_idx] # Get current card at that position

                print(f"DEBUG_MODEL: Enemy considering card: {card_to_play.get_name()}({card_to_play.get_symbol()}) (Cost: {card_to_play.get_cost()}). Energy: {self.enemy.get_energy()}")

                if card_to_play.get_cost() > self.enemy.get_energy():
                    print(f"  Enemy cannot afford {card_to_play.get_name()}.")
                    continue # Go to next card in hand

                chosen_target_for_enemy_spell = None
                if not card_to_play.is_permanent(): 
                    effect = card_to_play.get_effect()
                    # Simplified AI for spell targeting
                    if DAMAGE in effect and self.player.is_alive():
                        chosen_target_for_enemy_spell = self.player
                        print(f"  Enemy spell {card_to_play.get_name()} will target Player Hero {self.player.name_for_debug}")
                    elif HEALTH in effect and self.enemy.is_alive(): 
                        chosen_target_for_enemy_spell = self.enemy
                        print(f"  Enemy spell {card_to_play.get_name()} will target self ({self.enemy.name_for_debug})")
                    elif self.enemy.is_alive(): # Default for other spells
                         chosen_target_for_enemy_spell = self.enemy
                         print(f"  Enemy spell {card_to_play.get_name()} will target self (default) ({self.enemy.name_for_debug})")
                
                # Store card before playing, as it might be removed from hand
                card_name_for_log = card_to_play.get_name()
                if self.enemy_play_card(card_to_play, chosen_target_for_enemy_spell): # This has its own debug prints
                    enemy_played_card_names.append(card_name_for_log)
                    # Card is removed from hand inside enemy_play_card IF it was found.
                    # Your enemy_play_card doesn't remove from hand, the loop in end_turn does.
                    # Let's ensure it's removed here if successfully played.
                    if card_to_play in self.enemy.get_hand(): # Check if it's still there (it should be)
                        self.enemy.get_hand().remove(card_to_play)
                        print(f"DEBUG_MODEL: Removed {card_name_for_log} from enemy hand after successful play.")
                    else:
                        print(f"DEBUG_MODEL: WARNING - {card_name_for_log} was not in enemy hand after supposedly successful play for removal.")
                    
                    played_a_card_this_scan = True
                    print(f"DEBUG_MODEL: Enemy successfully played {card_name_for_log}. Restarting scan of hand.")
                    break # Breaks from inner loop (scan of current_hand_indices) to rescan hand
                else:
                    # If enemy_play_card returned False (e.g. not enough energy, though checked above)
                    print(f"DEBUG_MODEL: Enemy failed to play {card_name_for_log} via enemy_play_card (should be rare if cost check passed).")
                    # hand_index += 1 # This was from your original loop, not needed with current for loop
            
            if not played_a_card_this_scan: # If a full scan of the hand yielded no plays
                print("DEBUG_MODEL: Enemy made a full pass of hand, no card played. Ending card play phase.")
                still_can_play = False # Exit the outer while loop

            if self.has_won() or self.has_lost():
                print("DEBUG_MODEL: Game ended after enemy played a card.")
                return enemy_played_card_names
        self.remove_defeated_entities()
        
        # 4. Enemy's minions attack
        print(f"\nDEBUG_MODEL: --- 4. Enemy's ({self.enemy.name_for_debug}) minions attack ---")
        for minion in list(self.get_enemy_minions()): 
            if not minion.is_alive():
                print(f"DEBUG_MODEL: Enemy's {minion.name_for_debug} is not alive, skipping attack.")
                continue
            
            player_has_targetable_entities = self.player.is_alive() or any(m.is_alive() for m in self.active_player_minions)
            if not player_has_targetable_entities:
                print(f"DEBUG_MODEL: Enemy's {minion.name_for_debug} has no valid targets (player hero and minions defeated). Stopping attacks.")
                break 

            print(f"DEBUG_MODEL: Enemy's {minion.name_for_debug} ({minion.get_health()}H,{minion.get_shield()}S) attacking.")
            target = minion.choose_target(self.enemy, self.player, self.active_enemy_minions, self.active_player_minions) # This has debug prints
            
            if target:
                minion_attack_effect = minion.get_effect()
                print(f"  Enemy's {minion.name_for_debug} chose target: {target.name_for_debug} ({target.get_health()}H) with effect {minion_attack_effect}")
                apply_effects_and_handle_deaths_local(minion_attack_effect, target, f"Enemy's {minion.name_for_debug} attack", self)
            else:
                print(f"  Enemy's {minion.name_for_debug} chose no target.")
            if self.has_won() or self.has_lost():
                print("DEBUG_MODEL: Game ended after enemy's minion attacks.")
                return enemy_played_card_names
        self.remove_defeated_entities()

        # 5. Player: new turn sequence (if game not over and player is alive)
        print(f"\nDEBUG_MODEL: --- 5. Player ({self.player.name_for_debug}): new turn sequence ---")
        if self.player.is_alive() and not (self.has_won() or self.has_lost()):
            print(f"  Player HP before new_turn: {self.player.get_health()}, IsAlive: {self.player.is_alive()}")
            self.player.new_turn() # This has its own debug prints
            print(f"  Player HP after new_turn: {self.player.get_health()}, Energy: {self.player.get_energy()}/{self.player.get_max_energy()}, IsAlive: {self.player.is_alive()}")
        else:
            print("DEBUG_MODEL: Player is not alive or game ended, skipping player's new turn sequence.")
        
        print("\nDEBUG_MODEL: ===== End Turn Finished =====")
        print(f"DEBUG_MODEL (End of End Turn): Player: {self.player.name_for_debug} HP: {self.player.get_health()}, Enemy: {self.enemy.name_for_debug} HP: {self.enemy.get_health()}")
        print(f"  Player Minions: {[f'{m.name_for_debug}({m.get_health()}H,{m.get_shield()}S)' for m in self.active_player_minions]}")
        print(f"  Enemy Minions: {[f'{m.name_for_debug}({m.get_health()}H,{m.get_shield()}S)' for m in self.active_enemy_minions]}")
        return enemy_played_card_names
    
# Task 12


def play_game(initial_save_file: str) -> None:
    """
    Constructs the Hearthstone controller and starts the game loop.
    """
    # controller = Hearthstone(initial_save_file)
    # controller.run_game_loop()



def _build_specific_card(symbol: str, context: str = "player") -> Card:
    """
    Helper to build specific card instances for the test_end_turn scenario.
    """
    if symbol == 'S':
        return Shield()
    elif symbol == 'H':
        return Heal()
    elif symbol == 'R': # Raptor card (becomes Raptor minion on play)
        return Raptor(health=1, shield=0)
    elif symbol == 'W':
        if context == "player_hand_or_deck_fireball": # Player's 'W' card is a Fireball
            return Fireball(turns_in_hand=0)
        else: # Default 'W' is a Wyrm card/minion
            return Wyrm(health=1, shield=0)
    elif symbol.isdigit(): # Fireball with N turns
        return Fireball(turns_in_hand=int(symbol))
    else:
        # Fallback for unknown symbols, though test case should be specific
        print(f"WARNING: Unknown card symbol '{symbol}' in _build_specific_card. Creating generic Card.")
        return Card(_name=f"Unknown({symbol})", _cost=1)

def _build_specific_minion_on_board(symbol: str) -> Minion:
    """Helper to build specific minion instances for the board."""
    if symbol == 'W':
        return Wyrm(health=1, shield=0)
    elif symbol == 'R':
        return Raptor(health=1, shield=0)
    else:
        print(f"WARNING: Unknown minion symbol '{symbol}' for board. Creating generic Minion.")
        # Generic Minion in your a2.py takes health, shield
        return Minion(health=1, shield=0)


def main_debug_test_end_turn():
    """
    Sets up and runs the specific scenario from test_end_turn for debugging.
    """
    print("--- DEBUG: main_debug_test_end_turn ---")

    # Initialize debug counters if they are part of your instrumentation
    # These should ideally be global or handled within the class __init__ itself
    # to ensure they reset or increment correctly per run if needed.
    # For a single run like this, initializing here is okay.
    global _hero_debug_counter
    global _minion_debug_counter
    _hero_debug_counter = 1
    _minion_debug_counter = 1

    # --- Player Setup ---
    player_deck_symbols = ['S', 'H', '1', 'R', 'W', 'S', 'H', '0', '0', 'R', 'S', 'H', '0', '0', 'R', 'S', 'H', '0', '0', 'R']
    player_deck_cards = [_build_specific_card(s, "player_hand_or_deck_fireball" if s == 'W' else "player") for s in player_deck_symbols]
    player_deck = CardDeck(player_deck_cards)

    player_hand_symbols = ['R', 'W', '3', 'S', 'H'] # R, Fireball(W), Fireball(3), Shield, Heal
    player_hand_cards = []
    for s in player_hand_symbols:
        if s == 'W': # Player's 'W' in hand is Fireball(0)
            player_hand_cards.append(_build_specific_card(s, "player_hand_or_deck_fireball"))
        else:
            player_hand_cards.append(_build_specific_card(s, "player"))
            
    player_hero = Hero(health=10, shield=10, max_energy=5, deck=player_deck, hand=player_hand_cards)
    # Manually set debug name if your Hero init doesn't do it or if you want to override
    if hasattr(player_hero, 'name_for_debug'): player_hero.name_for_debug = "PlayerHero_Test"


    player_minion_symbols_on_board = ['W', 'R'] # Wyrm(1,0), Raptor(1,0) on board
    player_initial_minions = [_build_specific_minion_on_board(s) for s in player_minion_symbols_on_board]

    # --- Enemy Setup ---
    enemy_deck_symbols = ['R', 'W', 'S', 'H', 'R', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9']
    enemy_deck_cards = [_build_specific_card(s, "enemy") for s in enemy_deck_symbols] # Enemy 'W' is Wyrm
    enemy_deck = CardDeck(enemy_deck_cards)

    enemy_hand_symbols = ['W', 'W', 'H', '0', 'S'] # WyrmCard, WyrmCard, Heal, Fireball(0), Shield
    enemy_hand_cards = [_build_specific_card(s, "enemy") for s in enemy_hand_symbols]
    enemy_hero = Hero(health=20, shield=5, max_energy=5, deck=enemy_deck, hand=enemy_hand_cards)
    if hasattr(enemy_hero, 'name_for_debug'): enemy_hero.name_for_debug = "EnemyHero_Test"


    enemy_minion_symbols_on_board = ['R', 'R', 'R', 'R', 'R'] # Five Raptor(1,0) on board
    enemy_initial_minions = [_build_specific_minion_on_board(s) for s in enemy_minion_symbols_on_board]

    # --- Initialize Model ---
    model = HearthModel(
        player_hero,
        player_initial_minions,
        enemy_hero,
        enemy_initial_minions
    )
    print("\nDEBUG_MAIN: ===== Initial Model State =====")
    print(str(model))
    print(f"  Player Hand: {[c.get_name() for c in model.get_player().get_hand()]}")
    print(f"  Enemy Hand: {[c.get_name() for c in model.get_enemy().get_hand()]}")


    # --- Simulate pre-end_turn actions from test_end_turn ---
    print("\nDEBUG_MAIN: ===== Simulating pre-end_turn card plays by Player =====")

    # 1. Player plays first card from hand (RaptorCard)
    if model.get_player().get_hand():
        # The test implies playing the 'R' card. Let's find it.
        card_to_play1 = None
        for card_in_hand in model.get_player().get_hand():
            if isinstance(card_in_hand, Raptor): # Or check by name/symbol if more robust
                card_to_play1 = card_in_hand
                break
        
        if card_to_play1:
            print(f"DEBUG_MAIN: Player pre-play 1: Attempting to play {card_to_play1.get_name()} ({card_to_play1.get_symbol()})")
            # Minions in your setup don't need an explicit target for the play_card method itself,
            # their on-play choose_target is called internally.
            model.play_card(card_to_play1, target=None) # Target is None for minion summon
        else:
            print("DEBUG_MAIN: Player 'Raptor' card not found in hand for first pre-play.")
    else:
        print("DEBUG_MAIN: Player hand empty for first pre-play.")
    print(f"DEBUG_MAIN: Model state after player pre-play 1: {str(model)}")
    print(f"  Player Hand: {[c.get_name() for c in model.get_player().get_hand()]}")


    # 2. Player plays second card from hand (Fireball 'W') targeting enemy hero
    if model.get_player().get_hand():
        # The test implies playing the 'W' (Fireball) card.
        card_to_play2 = None
        for card_in_hand in model.get_player().get_hand():
            # Player's 'W' card in hand is a Fireball(0)
            if isinstance(card_in_hand, Fireball) and card_in_hand.get_symbol() == '0': # Check symbol if multiple fireballs
                card_to_play2 = card_in_hand
                break
        
        if card_to_play2:
            print(f"DEBUG_MAIN: Player pre-play 2: Attempting to play {card_to_play2.get_name()} ({card_to_play2.get_symbol()}) targeting enemy hero.")
            model.play_card(card_to_play2, target=model.get_enemy())
        else:
            print("DEBUG_MAIN: Player 'Fireball(W)' card not found in hand for second pre-play.")
    else:
        print("DEBUG_MAIN: Player hand empty for second pre-play.")

    print(f"DEBUG_MAIN: Model state after player pre-play 2: {str(model)}")
    print(f"  Player Hand: {[c.get_name() for c in model.get_player().get_hand()]}")
    print(f"DEBUG_MAIN: Enemy Hero HP before first end_turn: {model.get_enemy().get_health()}")


    # --- Call the end_turn method ---
    print("\nDEBUG_MAIN: ===== CALLING model.end_turn() (First Call) =====")
    played_by_enemy_in_turn = model.end_turn()
    print(f"\nDEBUG_MAIN: Cards played by enemy during their turn: {[name for name in played_by_enemy_in_turn]}")

    print("\nDEBUG_MAIN: ===== Final Model State after first end_turn =====")
    final_state_str = str(model)
    print(f"FINAL MODEL STRING: {final_state_str}")

    expected_output_substring_enemy_minions = "R,2,1;R,2,1;R,1,0;W,1,0;W,1,0" # From test_end_turn expected
    print(f"\nDEBUG_MAIN: For reference, expected enemy minions part: {expected_output_substring_enemy_minions}")
    if expected_output_substring_enemy_minions in final_state_str:
        print("DEBUG_MAIN: Enemy minions part MATCHES expected.")
    else:
        print("DEBUG_MAIN: Enemy minions part DOES NOT MATCH expected.")
        # Extract actual enemy minions from final_state_str for comparison
        parts = final_state_str.split('|')
        if len(parts) == 4:
            actual_enemy_minions_str = parts[3]
            print(f"  Actual enemy minions string: {actual_enemy_minions_str}")


    print("\n--- DEBUG: End of main_debug_test_end_turn ---")


def main() -> None:
    """
    Main function to run the Hearthstone game simulation.
    """
    


if __name__ == "__main__":
    # Make sure constants from support.py are loaded if you run this directly
    # e.g. MAX_HAND, CARD_NAME, MINION_SYMBOL etc.
    # If they are not available, you might get NameError exceptions.
    # You might need to add dummy versions of these constants at the top of a2.py
    # for standalone testing if support.py isn't structured for direct import access here.
    # Example dummy constants (replace with actual values or ensure support.py provides them):
    # CARD_NAME, CARD_DESC, CARD_SYMBOL = "Card", "A card.", "C"
    # SHIELD_NAME, SHIELD_DESC, SHIELD_SYMBOL = "Shield", "Grants shield.", "S"
    # HEAL_NAME, HEAL_DESC, HEAL_SYMBOL = "Heal", "Restores health.", "H"
    # FIREBALL_NAME, FIREBALL_DESC = "Fireball", "Deals damage."
    # MINION_NAME, MINION_DESC, MINION_SYMBOL = "Minion", "A minion.", "M"
    # WYRM_NAME, WYRM_DESC, WYRM_SYMBOL = "Wyrm", "A wyrm.", "W"
    # RAPTOR_NAME, RAPTOR_DESC, RAPTOR_SYMBOL = "Raptor", "A raptor.", "R"
    # HEALTH, SHIELD, DAMAGE = "health", "shield", "damage"
    # MAX_HAND = 5
    # MAX_MINIONS = 7

    main_debug_test_end_turn()