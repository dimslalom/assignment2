# Test snippet for Wyrm.choose_target

# --- Minimal Class Definitions (based on a2.py structure) ---
HEALTH = "health"
SHIELD = "shield"
DAMAGE = "damage" # Though not directly used by Wyrm's effect logic
WYRM_SYMBOL = "W"
RAPTOR_SYMBOL = "R"
CARD_SYMBOL = "C" # Generic card
MINION_SYMBOL = "M" # Generic minion

class Entity:
    def __init__(self, health: int, shield: int):
        self.health = health
        self.shield = shield
        # Assign a default name based on the class, can be overridden by subclasses
        self.name = self.__class__.__name__ 

    def get_health(self) -> int:
        return self.health

    def get_shield(self) -> int:
        return self.shield

    def get_symbol(self) -> str: # For basic identification
        return "E"

    def __str__(self) -> str:
        # Provides a readable representation of the entity, useful for printing the target
        return f"{self.name}(H:{self.health}, S:{self.shield})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.health}, {self.shield})"

class Card:
    def __init__(self, **kwargs):
        # Simplified: name, description, cost, effect not all strictly needed for this specific test
        self.name = kwargs.get("name", "Card")
        self.cost = kwargs.get("cost", 1)
        self.effect = kwargs.get("effect", {})

    def get_symbol(self) -> str:
        return CARD_SYMBOL
    
    def get_name(self) -> str:
        return self.name

    def get_cost(self) -> int:
        return self.cost

    def get_effect(self) -> dict: # Changed from str to dict to match Wyrm
        return self.effect

class Minion(Card, Entity): # Order of inheritance from a2.py
    def __init__(self, health: int, shield: int):
        # Explicitly initialize both base classes for clarity in this snippet
        Card.__init__(self) 
        Entity.__init__(self, health, shield)
        self.cost = 2 # Default for Minion subclasses like Wyrm/Raptor
        # Name will be set by Entity.__init__ and can be overridden by Wyrm/Raptor

    def get_symbol(self) -> str:
        return MINION_SYMBOL # Default, overridden by subclasses

    # Generic minion's choose_target (e.g., for attacking), not for Wyrm's on-play effect.
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        return self # Default minion targets itself for its own actions

class Wyrm(Minion):
    def __init__(self, health: int, shield: int):
        super().__init__(health, shield)
        self.name = "Wyrm" # Specific name
        # self.description = WYRM_DESC # Not needed for this test
        self.cost = 2
        self.effect = {HEALTH: 1, SHIELD: 1}

    def get_symbol(self) -> str:
        return WYRM_SYMBOL

    # This is the method under test, copied from your a2.py (from attachment)
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        ally_minions_copy = [m for m in ally_minions] # Creates a copy as in your code
        all_ally_entities = [ally_hero] + ally_minions_copy
        
        if not all_ally_entities: # Should not happen if ally_hero is always present
            return None

        # Find the entity with the lowest health
        # Using direct min finding to avoid issues with empty list for min() if all_ally_entities could be empty
        current_min_health = all_ally_entities[0].get_health()
        for entity in all_ally_entities[1:]:
            if entity.get_health() < current_min_health:
                current_min_health = entity.get_health()
        
        lowest_health_entities = [e for e in all_ally_entities if e.get_health() == current_min_health]
        
        if ally_hero in lowest_health_entities:
            # If the allied hero is among the lowest health entities, return it
            return ally_hero
        
        # Otherwise, return the leftmost minion with the lowest health
        # (If lowest_health_entities is not empty and hero wasn't chosen)
        if lowest_health_entities:
            return lowest_health_entities[0] 
        return None # Fallback, though unlikely given the logic

class Raptor(Minion):
    def __init__(self, health: int, shield: int):
        super().__init__(health, shield)
        self.name = "Raptor" # Specific name
        # self.description = RAPTOR_DESC # Not needed for this test
        self.cost = 2
        # self.effect = {DAMAGE: self.health} # Effect details not critical for this test

    def get_symbol(self) -> str:
        return RAPTOR_SYMBOL

class CardDeck:
    def __init__(self, cards: list[Card]):
        self.cards = list(cards) # Make a copy

    def remaining_count(self) -> int: # Needed for Hero if its is_alive() is complex
        return len(self.cards)
    
    def is_empty(self) -> bool:
        return not self.cards

class Hero(Entity):
    def __init__(self, health: int, shield: int, max_energy: int, deck: CardDeck, hand: list[Card]):
        super().__init__(health, shield)
        self.max_energy = max_energy
        self.energy = max_energy # For completeness
        self.deck = deck
        self.hand = list(hand) # Make a copy
        self.name = "Hero" # Specific name

    # For this test, Hero.is_alive() isn't directly called by Wyrm.choose_target,
    # only get_health() is. So, Entity's is_alive() or a simple one is fine.

# --- Test Scenario Setup ---

print("--- Wyrm.choose_target Test Snippet ---")

# Create entities for the test
# The Wyrm whose choose_target method we are testing
wyrm_under_test = Wyrm(health=1, shield=0) 
# An allied minion (Raptor) to the left of the Wyrm
raptor_ally = Raptor(health=2, shield=0)

# The list of allied minions on the board. 
# The Wyrm is included as it has just been played. Raptor is to its left.
# This list is passed to wyrm_under_test.choose_target()
# (Assuming enemy player's perspective, these are "enemy" units to the main player)
current_allied_minions = [raptor_ally, wyrm_under_test]

# --- Case A: Allied Hero has 1 health ---
hero_A = Hero(health=1, shield=0, max_energy=10, deck=CardDeck([]), hand=[])

# Parameters for choose_target:
# ally_hero is hero_A
# enemy_hero and enemy_minions are not used by Wyrm's logic, so can be None or empty.
target_A = wyrm_under_test.choose_target(
    ally_hero=hero_A, 
    enemy_hero=None,  # Placeholder
    ally_minions=current_allied_minions, 
    enemy_minions=[]  # Placeholder
)
print(f"\nCase A: Hero HP={hero_A.get_health()}, Raptor HP={raptor_ally.get_health()}, Wyrm HP={wyrm_under_test.get_health()}")
print(f"Entities considered: {[str(e) for e in [hero_A] + current_allied_minions]}")
print(f"Chosen target by Wyrm: {target_A}")
# Expected for Case A: Hero (Wyrm and Hero both 1HP, Hero is preferred)


# --- Case B: Allied Hero has 2 health ---
hero_B = Hero(health=2, shield=0, max_energy=10, deck=CardDeck([]), hand=[])
# The Wyrm and Raptor instances are the same, their healths haven't changed.
# wyrm_under_test still has 1 health.

target_B = wyrm_under_test.choose_target(
    ally_hero=hero_B,
    enemy_hero=None, 
    ally_minions=current_allied_minions,
    enemy_minions=[]
)
print(f"\nCase B: Hero HP={hero_B.get_health()}, Raptor HP={raptor_ally.get_health()}, Wyrm HP={wyrm_under_test.get_health()}")
print(f"Entities considered: {[str(e) for e in [hero_B] + current_allied_minions]}")
print(f"Chosen target by Wyrm: {target_B}")
# Expected for Case B: Wyrm (Wyrm 1HP, Hero 2HP, Raptor 2HP; Wyrm is sole lowest)

print("\n--- Test End ---")
