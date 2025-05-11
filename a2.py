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
        return f"Entity({self.health}, {self.shield})"
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

def main() -> None:
    Card1 = Card(name="Fireball", description="Deal 6 damage to a taget", cost=4, effect={DAMAGE:6}, type="Spell")
    Card2 = Card(name="Fire Elemental", description="Deal 3 damage to a target.", cost=5, effect={DAMAGE:3}, type="Minion")

    # #TESTING
    # # --- Operations for Card1 ---
    # # Prints the string representation of Card1
    # print(str(Card1))
    # # Prints the symbol of Card1
    # print(Card1.get_symbol())
    # # Prints the name of Card1
    # print(Card1.get_name())
    # # Prints the cost of Card1
    # print(Card1.get_cost())
    # # Prints the effect of Card1
    # print(Card1.get_effect())
    # # Prints whether Card1 is permanent
    # print(Card1.is_permanent())

    # # --- Operations for Card2 ---
    # # Prints the string representation of Card2
    # print(str(Card2))
    # # Prints the symbol of Card2
    # print(Card2.get_symbol())
    # # Prints the name of Card2
    # print(Card2.get_name())
    # # Prints the cost of Card2
    # print(Card2.get_cost())
    # # Prints the effect of Card2
    # print(Card2.get_effect())
    # # Prints whether Card2 is permanent
    # print(Card2.is_permanent())

    # # --- Operations for Shield ---
    # Shield1 = Shield()
    # # Prints the string representation of Shield1
    # print(str(Shield1))
    # # Prints the symbol of Shield1
    # print(Shield1.get_symbol())
    # # Prints the name of Shield1
    # print(Shield1.get_name())
    # # Prints the cost of Shield1
    # print(Shield1.get_cost())
    # # Prints the effect of Shield1
    # print(Shield1.get_effect())
    # # Prints whether Shield1 is permanent
    # print(Shield1.is_permanent())

    # # --- Operations for Heal ---
    # Heal1 = Heal()
    # # Prints the string representation of Heal1
    # print(str(Heal1))
    # # Prints the symbol of Heal1
    # print(Heal1.get_symbol())
    # # Prints the name of Heal1
    # print(Heal1.get_name())
    # # Prints the cost of Heal1
    # print(Heal1.get_cost())
    # # Prints the effect of Heal1
    # print(Heal1.get_effect())
    # # Prints whether Heal1 is permanent

    # # --- Operations for Fireball ---
    # Fireball1 = Fireball(7)
    # # Prints the string representation of Fireball1
    # print(str(Fireball1))
    # # Prints the symbol of Fireball1
    # print(Fireball1.get_symbol())
    # # Prints the name of Fireball1
    # print(Fireball1.get_name())
    # # Prints the cost of Fireball1
    # print(Fireball1.get_cost())
    # # Prints the effect of Fireball1
    # print(Fireball1.get_effect())
    # # Prints whether Fireball1 is permanent
    # print(Fireball1.is_permanent())
    # # Prints the number of turns Fireball1 has been in hand
    # print(Fireball1.turns_in_hand)


    # # Increments the number of turns Fireball1 has been in hand
    # Fireball1.increment_turn()
    # # Prints the number of turns Fireball1 has been in hand
    # print(Fireball1.turns_in_hand)
    # # Prints the symbol of Fireball1
    # print(Fireball1.get_symbol())
    # # Prints the effect of Fireball1
    # print(Fireball1.get_effect())

    # # --- Test sequence for CardDeck ---
    # print("--- CardDeck Test Sequence ---")
    # cards_list = [Card(), Card(), Shield(), Heal(), Fireball(6)]
    # deck = CardDeck(cards_list)
    # print(f">>> deck = CardDeck([Card(), Card(), Shield(), Heal(), Fireball(6)])") # Simulating input line
    # print(f">>> deck\n{repr(deck)}") # Simulating output line
    # print("\n>>> str(deck)")
    # print(f"'{str(deck)}'") # Simulating output line, note the extra ' '

    # print(f"\n>>> deck.remaining_count()\n{deck.remaining_count()}")

    # print(f"\n>>> deck.is_empty()\n{deck.is_empty()}")

    # drawn_cards_1 = deck.draw_cards(3)
    # print(f"\n>>> deck.draw_cards(3)\n{drawn_cards_1}")

    # print(f"\n>>> deck.remaining_count()\n{deck.remaining_count()}")

    # print("\n>>> str(deck)")
    # print(f"'{str(deck)}'")

    # deck.add_card(Fireball(5))
    # print(f"\n>>> deck.add_card(Fireball(5))") # Action

    # print(f"\n>>> deck.remaining_count()\n{deck.remaining_count()}")

    # print("\n>>> str(deck)")
    # print(f"'{str(deck)}'")

    # drawn_cards_2 = deck.draw_cards(1001)
    # print(f"\n>>> deck.draw_cards(1001)\n{drawn_cards_2}")

    # print("\n>>> str(deck)")
    # # The example shows '' for an empty deck string, so CardDeck.__str__ handles this.
    # print(f"{str(deck)}") # str(deck) already returns "''" when empty

    # print(f"\n>>> deck.is_empty()\n{deck.is_empty()}")
    # print("--- End of CardDeck Test Sequence ---")

    # # --- Entity Test Sequence ---
    # print("--- Entity Test Sequence ---")

    # # >>> entity = Entity(5,3)
    # entity = Entity(5, 3)
    # print(f">>> entity = Entity(5,3)") # Simulating input line

    # # >>> entity
    # # Entity(5, 3)
    # print(f">>> entity\n{repr(entity)}")

    # # >>> str(entity)
    # # '5,3'
    # print(f"\n>>> str(entity)\n'{str(entity)}'") # Output '5,3' as a string

    # # >>> entity.get_health()
    # # 5
    # print(f"\n>>> entity.get_health()\n{entity.get_health()}")

    # # >>> entity.get_shield()
    # # 3
    # print(f"\n>>> entity.get_shield()\n{entity.get_shield()}")

    # # >>> entity.apply_shield(1)
    # print(f"\n>>> entity.apply_shield(1)")
    # entity.apply_shield(1)
    # # >>> entity
    # # Entity(5, 4)
    # print(f">>> entity\n{repr(entity)}")

    # # >>> entity.apply_health(10)
    # print(f"\n>>> entity.apply_health(10)")
    # entity.apply_health(10)
    # # >>> entity
    # # Entity(15, 4)
    # print(f">>> entity\n{repr(entity)}")

    # # >>> entity.apply_damage(10)
    # print(f"\n>>> entity.apply_damage(10)")
    # entity.apply_damage(10)
    # # >>> entity
    # # Entity(9, 0)
    # print(f">>> entity\n{repr(entity)}")

    # # >>> entity.is_alive()
    # # True
    # print(f"\n>>> entity.is_alive()\n{entity.is_alive()}")

    # # >>> entity.apply_damage(9999999999)
    # print(f"\n>>> entity.apply_damage(9999999999)")
    # entity.apply_damage(9999999999)

    # # >>> entity.get_health()
    # # 0
    # print(f">>> entity.get_health()\n{entity.get_health()}") # This comes after the damage

    # # >>> entity.is_alive()
    # # False
    # print(f"\n>>> entity.is_alive()\n{entity.is_alive()}")
    
    # print("--- End of Entity Test Sequence ---")


if __name__ == "__main__":
    main()