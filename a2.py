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
        """
        # Find the entity with the lowest health
        min_health_entity = self
        for entity in ally_minions + [ally_hero]:
            if entity.get_health() < min_health_entity.get_health():
                min_health_entity = entity
            elif entity.get_health() == min_health_entity.get_health():
                # If the health is the same, prefer the hero
                if isinstance(entity, Hero) and not isinstance(min_health_entity, Hero):
                    min_health_entity = entity
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
        self.effect = {DAMAGE: health}
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
        Return player, active player minions, enemy, and 
        active enemy minions as a formatted string.
        """
        player_str = str(self.player)
        active_player_minions_str = ";".join(str(minion) for minion in self.active_player_minions)
        enemy_str = str(self.enemy)
        active_enemy_minions_str = ";".join(str(minion) for minion in self.active_enemy_minions)
        return f"{player_str}|{active_player_minions_str}|{enemy_str}|{active_enemy_minions_str}"
    def __repr__(self) -> str:
        """
        Returns a string which could be copied and pasted into
        a REPL to construct a new instance identical to self.
        """
        return f"{self.__class__.__name__}({self.player}, {self.active_player_minions}, {self.enemy}, {self.active_enemy_minions})"
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
    def get_active_player_minions(self) -> list[Minion]:
        """
        Returns the active player minions. Minions should appear in order 
        from leftmost minion slot to rightmost minion slot.
        """
        return self.active_player_minions
    def get_active_enemy_minions(self) -> list[Minion]:
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
    def play_card(self, card: Card, target: Entity) -> bool:
        """
        Attempts to play the specified card on the player’s behalf. Table 2 Specifies the actions that must occur when an attempt is made to play a card. Returns whether the card was successfully played or not. The target argument will be ignored if the specified card is permanent. If a minion is defeated, it should be removed from the game, and any remaining minions within the respective minion slots should be moved one slot left if able.
        """
        if card.get_cost() > self.player.get_energy():
            return False
        if card.is_permanent():
            target = card.choose_target(self.player, self.enemy, self.active_player_minions, self.active_enemy_minions)
        self.player.spend_energy(card.get_cost())
        for effect in card.get_effect():
            if effect == DAMAGE:
                target.apply_damage(card.get_effect()[DAMAGE])
            elif effect == SHIELD:
                target.apply_shield(card.get_effect()[SHIELD])
            elif effect == HEALTH:
                target.apply_health(card.get_effect()[HEALTH])
        for minion in self.active_player_minions + self.active_enemy_minions:
            if not minion.is_alive():
                if minion in self.active_player_minions:
                    self.active_player_minions.remove(minion)
                else:
                    self.active_enemy_minions.remove(minion)
    

def main() -> None:
    Card1 = Card(name="Fireball", description="Deal 6 damage to a taget", cost=4, effect={DAMAGE:6}, type="Spell")
    Card2 = Card(name="Fire Elemental", description="Deal 3 damage to a target.", cost=5, effect={DAMAGE:3}, type="Minion")


if __name__ == "__main__":
    main()