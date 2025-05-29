import copy

# --- Constants (from a2.py context) ---
HEALTH = "health"
SHIELD = "shield"
DAMAGE = "damage"

PLAYER_HERO_MAX_HEALTH = 30 # Default, test might override
ENEMY_HERO_MAX_HEALTH = 30  # Default

MAX_HAND_SIZE = 5
MAX_MINIONS = 7 # Assuming a common limit

# Symbols
WYRM_SYMBOL = "W"
RAPTOR_SYMBOL = "R"
FIREBALL_SYMBOL = "F" # Assuming 'F' for Fireball card, test uses 'W' in hand for player's fireball
SHIELD_CARD_SYMBOL = "S"
HEAL_CARD_SYMBOL = "H"
GENERIC_MINION_SYMBOL = "M"
GENERIC_CARD_SYMBOL = "C"

# Names (assuming from support.py or similar)
WYRM_NAME = "Wyrm"
RAPTOR_NAME = "Raptor"
FIREBALL_NAME = "Fireball"
SHIELD_CARD_NAME = "Shield"
HEAL_CARD_NAME = "Heal"

# --- Basic Game Entity Classes ---
class Entity:
    def __init__(self, health: int, shield: int):
        self.health = health
        self.shield = shield
        self.max_health = health # Store initial health as max_health for some cards
        self.name = self.__class__.__name__

    def get_health(self) -> int:
        return self.health

    def get_shield(self) -> int:
        return self.shield

    def get_max_health(self) -> int:
        return self.max_health

    def apply_health(self, health_amount: int) -> None:
        self.health += health_amount
        # print(f"DEBUG: {self} received {health_amount} health, now {self.health} HP")

    def apply_shield(self, shield_amount: int) -> None:
        self.shield += shield_amount
        # print(f"DEBUG: {self} received {shield_amount} shield, now {self.shield} SP")
    
    def apply_damage(self, damage: int) -> None:
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
        # print(f"DEBUG: {self} took damage, now {self.health} HP, {self.shield} SP")

    def is_alive(self) -> bool:
        return self.health > 0

    def __str__(self) -> str:
        return f"{self.name}(H:{self.health},S:{self.shield})"

    def get_symbol(self) -> str: # Fallback
        if hasattr(self, 'symbol'):
            return self.symbol
        return "E"


class Card:
    def __init__(self, name: str, cost: int, description: str = ""):
        self.name = name
        self.cost = cost
        self.description = description
        self.effect = {} # Default

    def get_name(self) -> str:
        return self.name

    def get_cost(self) -> int:
        return self.cost

    def get_effect(self) -> dict:
        return self.effect

    def is_permanent(self) -> bool: # True for minions, False for spells
        return False

    def get_symbol(self) -> str:
        return GENERIC_CARD_SYMBOL

    def __str__(self) -> str:
        return f"{self.name}({self.get_symbol()})"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}', {self.cost})"


class SpellCard(Card):
    def __init__(self, name: str, cost: int, effect: dict, symbol: str):
        super().__init__(name, cost)
        self.effect = effect
        self._symbol = symbol
    
    def get_symbol(self) -> str:
        return self._symbol

class FireballCard(SpellCard):
    def __init__(self, name: str = FIREBALL_NAME, cost: int = 3, initial_delay: int = 0, damage_val: int = 3):
        super().__init__(name, cost, {DAMAGE: damage_val}, FIREBALL_SYMBOL if initial_delay == 0 else str(initial_delay))
        self.current_delay = initial_delay
        self.base_damage = damage_val
        self.effect = {DAMAGE: self.base_damage} # Effect updates if delay changes

    def get_symbol(self) -> str:
        return str(self.current_delay) if self.current_delay > 0 else FIREBALL_SYMBOL

    def register_turn(self) -> None:
        if self.current_delay > 0:
            self.current_delay -= 1
            # print(f"DEBUG: Fireball {self.name} ticked, delay now {self.current_delay}")
        # Update effect if needed, though damage is usually static unless specified
        self.effect = {DAMAGE: self.base_damage}


class MinionCard(Card): # Represents a minion card in hand
    def __init__(self, name: str, cost: int, health: int, shield: int, symbol: str, minion_type: type):
        super().__init__(name, cost)
        self.health = health
        self.shield = shield
        self._symbol = symbol
        self.minion_type = minion_type # e.g., Wyrm, Raptor class for board instantiation

    def is_permanent(self) -> bool:
        return True

    def get_symbol(self) -> str:
        return self._symbol

    def create_minion_on_board(self) -> 'Minion': # Forward declaration
        # print(f"DEBUG: Creating {self.minion_type.__name__} with H:{self.health}, S:{self.shield} for board")
        return self.minion_type(self.health, self.shield)


class Minion(Entity): # Represents a minion on the board
    def __init__(self, health: int, shield: int, name: str, cost: int, effect: dict = None):
        super().__init__(health, shield)
        self.name = name
        self.cost = cost # Cost to play from hand, less relevant on board
        self.effect = effect if effect else {} # Attack effect

    def get_effect(self) -> dict: # This is for ATTACK effect
        return self.effect

    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list['Minion'], enemy_minions: list['Minion']) -> Entity:
        # Default minion attack: target enemy hero if alive, else first enemy minion
        if enemy_hero.is_alive():
            return enemy_hero
        for m in enemy_minions:
            if m.is_alive():
                return m
        return None
    
    def get_symbol(self) -> str: # Overridden by subclasses
        return GENERIC_MINION_SYMBOL

    def __str__(self) -> str: # For board representation
        return f"{self.get_symbol()},{self.health},{self.shield}"


class Wyrm(Minion):
    ON_PLAY_EFFECT = {HEALTH: 1, SHIELD: 1}
    ATTACK_EFFECT = {DAMAGE: 1} # Assuming Wyrms have a basic attack effect

    def __init__(self, health: int, shield: int):
        super().__init__(health, shield, WYRM_NAME, 2, self.ATTACK_EFFECT)

    def get_symbol(self) -> str:
        return WYRM_SYMBOL

    # This is Wyrm's ON-PLAY effect targeting logic
    def choose_target_on_play(self, ally_hero: Entity, ally_minions: list[Minion]) -> Entity:
        # Copied from user's a2.py (lines 359-376 of snippet)
        # Ensure 'self' (the Wyrm instance being played) is part of ally_minions for this context
        # This method is called on the Wyrm instance itself.
        
        # The 'ally_minions' list passed here should already include this Wyrm instance.
        # The Wyrm itself is one of the potential targets.

        all_ally_entities = [ally_hero] + ally_minions # Minions list already contains self
        
        if not all_ally_entities: return None

        all_ally_entities_health = [e.get_health() for e in all_ally_entities]
        if not all_ally_entities_health: return None
        lowest_health = min(all_ally_entities_health)
        
        lowest_health_entities = [e for e in all_ally_entities if e.get_health() == lowest_health]
        
        if ally_hero in lowest_health_entities:
            return ally_hero
        
        # If hero not chosen, and lowest_health_entities is not empty,
        # the first one is the leftmost (hero, then minions in order).
        # Since hero wasn't chosen, it must be a minion.
        if lowest_health_entities:
            # To ensure 'self' is chosen if it's the leftmost 1HP minion and hero isn't 1HP:
            # The list `all_ally_entities` is `[ally_hero] + ally_minions`.
            # `lowest_health_entities` preserves this relative order for tied entities.
            # So `lowest_health_entities[0]` will be the hero if it's tied and lowest,
            # otherwise it's the leftmost minion from `ally_minions` that's tied and lowest.
            return lowest_health_entities[0]
        return None

    # This is Wyrm's ATTACK targeting logic (inherited or can be specific)
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Minion], enemy_minions: list[Minion]) -> Entity:
        # Wyrm attack: target enemy minion with lowest health, else enemy hero
        living_enemy_minions = [m for m in enemy_minions if m.is_alive()]
        if not living_enemy_minions:
            return enemy_hero if enemy_hero.is_alive() else None

        target = living_enemy_minions[0]
        for m in living_enemy_minions[1:]:
            if m.get_health() < target.get_health():
                target = m
        return target


class Raptor(Minion):
    def __init__(self, health: int, shield: int):
        super().__init__(health, shield, RAPTOR_NAME, 2) # Effect is dynamic

    def get_symbol(self) -> str:
        return RAPTOR_SYMBOL

    def get_effect(self) -> dict: # Attack effect
        return {DAMAGE: self.health} # Dynamically uses current health

    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Minion], enemy_minions: list[Minion]) -> Entity:
        # Copied from user's a2.py (lines 389-399 of snippet)
        living_enemy_minions = [m for m in enemy_minions if m.is_alive()]
        if not living_enemy_minions:
            return enemy_hero if enemy_hero.is_alive() else None

        highest_health_minion = living_enemy_minions[0]
        for i in range(1, len(living_enemy_minions)):
            current_minion = living_enemy_minions[i]
            if current_minion.get_health() > highest_health_minion.get_health():
                highest_health_minion = current_minion
        return highest_health_minion


class CardDeck:
    def __init__(self, cards: list[Card]):
        self.cards = list(cards)

    def draw_cards(self, count: int) -> list[Card]:
        drawn = []
        for _ in range(count):
            if not self.is_empty():
                drawn.append(self.cards.pop(0))
        return drawn

    def is_empty(self) -> bool:
        return not self.cards

    def remaining_count(self) -> int:
        return len(self.cards)
    
    def __str__(self) -> str:
        return ",".join(c.get_symbol() for c in self.cards)
    
    def __repr__(self) -> str:
        return f"CardDeck({[repr(c) for c in self.cards]})"


class Hero(Entity):
    def __init__(self, health: int, shield: int, max_energy: int, deck: CardDeck, hand: list[Card], name: str = "Hero"):
        super().__init__(health, shield)
        self.name = name
        self.max_health = health # Hero max health for display/logic
        self.max_energy = max_energy
        self.energy = max_energy # Start with max energy
        self.deck = deck
        self.hand = list(hand)

    def is_alive(self) -> bool: # As per "health and deck size are both above 0"
        return self.health > 0 and self.deck.remaining_count() > 0

    def get_energy(self) -> int:
        return self.energy
    
    def get_max_energy(self) -> int:
        return self.max_energy

    def get_hand(self) -> list[Card]:
        return self.hand

    def new_turn(self) -> None:
        # print(f"DEBUG: {self.name} new_turn starts. Hand: {[str(c) for c in self.hand]}")
        for card_in_hand in self.hand:
            if isinstance(card_in_hand, FireballCard):
                card_in_hand.register_turn()
        
        cards_to_draw = MAX_HAND_SIZE - len(self.hand)
        if cards_to_draw > 0:
            drawn = self.deck.draw_cards(cards_to_draw)
            self.hand.extend(drawn)
            # print(f"DEBUG: {self.name} drew {len(drawn)} cards. Hand size: {len(self.hand)}")

        if self.max_energy < 10: # Assuming cap of 10
            self.max_energy += 1
        self.energy = self.max_energy
        # print(f"DEBUG: {self.name} new_turn ends. Energy: {self.energy}/{self.max_energy}. HP: {self.health}")

    def __str__(self) -> str:
        hand_str = ",".join(c.get_symbol() for c in self.hand)
        return f"{self.health},{self.shield},{self.max_energy};{str(self.deck)};{hand_str}"


class HearthModel_Debug:
    def __init__(self, player_hero: Hero, player_minions: list[Minion], 
                 enemy_hero: Hero, enemy_minions: list[Minion]):
        self.player = player_hero
        self.active_player_minions = list(player_minions)
        self.enemy = enemy_hero
        self.active_enemy_minions = list(enemy_minions)
        print("DEBUG: HearthModel_Debug initialized.")
        print(f"DEBUG: Initial Player: {self.player} | Minions: {[str(m) for m in self.active_player_minions]}")
        print(f"DEBUG: Initial Enemy: {self.enemy} | Minions: {[str(m) for m in self.active_enemy_minions]}")


    def get_player_minions(self) -> list[Minion]:
        return self.active_player_minions

    def get_enemy_minions(self) -> list[Minion]:
        return self.active_enemy_minions

    def remove_defeated_entities(self):
        self.active_player_minions = [m for m in self.active_player_minions if m.is_alive()]
        self.active_enemy_minions = [m for m in self.active_enemy_minions if m.is_alive()]
        # print("DEBUG: remove_defeated_entities called.")
        # print(f"DEBUG: Player minions now: {[str(m) for m in self.active_player_minions]}")
        # print(f"DEBUG: Enemy minions now: {[str(m) for m in self.active_enemy_minions]}")


    def _apply_effects_and_handle_deaths(self, effect_dict: dict, target_entity: Entity, source_description: str):
        if target_entity and effect_dict:
            print(f"DEBUG: Applying effect {effect_dict} from {source_description} to {target_entity} (Pre-HP: {target_entity.get_health()}, SP: {target_entity.get_shield()})")
            if HEALTH in effect_dict: target_entity.apply_health(effect_dict[HEALTH])
            if SHIELD in effect_dict: target_entity.apply_shield(effect_dict[SHIELD])
            if DAMAGE in effect_dict: target_entity.apply_damage(effect_dict[DAMAGE])
            print(f"DEBUG: Target {target_entity} (Post-HP: {target_entity.get_health()}, SP: {target_entity.get_shield()})")
        self.remove_defeated_entities()

    def has_won(self) -> bool:
        return not self.enemy.is_alive() and not any(m.is_alive() for m in self.active_enemy_minions)

    def has_lost(self) -> bool:
        return not self.player.is_alive() and not any(m.is_alive() for m in self.active_player_minions)

    def play_card(self, card_in_hand: Card, target: Entity = None, slot: int = -1) -> bool:
        print(f"DEBUG: Player attempts to play {card_in_hand} (Cost: {card_in_hand.get_cost()}) with Energy: {self.player.get_energy()}")
        if card_in_hand.get_cost() > self.player.get_energy():
            print(f"DEBUG: Not enough energy to play {card_in_hand}.")
            return False

        self.player.energy -= card_in_hand.get_cost()
        self.player.hand.remove(card_in_hand)
        print(f"DEBUG: Player played {card_in_hand}. Energy left: {self.player.get_energy()}")

        if isinstance(card_in_hand, MinionCard):
            if len(self.active_player_minions) < MAX_MINIONS:
                new_minion = card_in_hand.create_minion_on_board()
                self.active_player_minions.append(new_minion)
                print(f"DEBUG: Player summoned {new_minion} to board. Player minions: {[str(m) for m in self.active_player_minions]}")
                # Handle on-play for player's minions if any (e.g. Player's Wyrm)
                if isinstance(new_minion, Wyrm):
                    on_play_target = new_minion.choose_target_on_play(self.player, self.active_player_minions)
                    if on_play_target:
                        print(f"DEBUG: Player's {new_minion} on-play targets {on_play_target}")
                        self._apply_effects_and_handle_deaths(Wyrm.ON_PLAY_EFFECT, on_play_target, f"Player's {new_minion} on-play")
            else:
                print(f"DEBUG: Player board full, cannot summon {card_in_hand.get_name()}.")
        elif isinstance(card_in_hand, SpellCard):
            if target:
                print(f"DEBUG: Player's spell {card_in_hand} targets {target}")
                self._apply_effects_and_handle_deaths(card_in_hand.get_effect(), target, f"Player's spell {card_in_hand}")
            else: # Some spells might not need target or target self
                print(f"DEBUG: Player's spell {card_in_hand} (no explicit target or self-target). Applying to player hero.")
                self._apply_effects_and_handle_deaths(card_in_hand.get_effect(), self.player, f"Player's spell {card_in_hand}")
        
        self.remove_defeated_entities()
        return True

    def enemy_play_card(self, card_to_play: Card, chosen_target_for_enemy_spell: Entity = None) -> bool:
        print(f"DEBUG: Enemy attempts to play {card_to_play} (Cost: {card_to_play.get_cost()}) with Energy: {self.enemy.get_energy()}")
        if card_to_play.get_cost() > self.enemy.get_energy():
            print(f"DEBUG: Enemy not enough energy for {card_to_play}.")
            return False

        self.enemy.energy -= card_to_play.get_cost()
        # Assuming card_to_play is directly from hand and needs removal by identity/index
        # For simplicity, let's assume it's removed correctly before this call or handled by caller
        # self.enemy.hand.remove(card_to_play) # This might fail if card_to_play is a copy
        print(f"DEBUG: Enemy played {card_to_play}. Energy left: {self.enemy.get_energy()}")

        if isinstance(card_to_play, MinionCard):
            if len(self.active_enemy_minions) < MAX_MINIONS:
                new_minion = card_to_play.create_minion_on_board()
                self.active_enemy_minions.append(new_minion) # Add to board first
                print(f"DEBUG: Enemy summoned {new_minion} to board. Enemy minions: {[str(m) for m in self.active_enemy_minions]}")
                
                # Handle Wyrm's on-play effect specifically
                if isinstance(new_minion, Wyrm):
                    # CRITICAL LOGGING POINT: Enemy hero health before Wyrm's on-play target selection
                    print(f"CRITICAL_DEBUG: Enemy Hero HP before {new_minion} on-play target selection: {self.enemy.get_health()}")
                    print(f"CRITICAL_DEBUG: Enemy Minions on board before {new_minion} on-play: {[str(m) for m in self.active_enemy_minions]}")
                    
                    # Pass a copy of the current minions list that includes the new_minion
                    on_play_target = new_minion.choose_target_on_play(self.enemy, list(self.active_enemy_minions))
                    
                    if on_play_target:
                        print(f"CRITICAL_DEBUG: Enemy's {new_minion} on-play effect targets: {on_play_target}")
                        self._apply_effects_and_handle_deaths(Wyrm.ON_PLAY_EFFECT, on_play_target, f"Enemy's {new_minion} on-play")
                    else:
                        print(f"CRITICAL_DEBUG: Enemy's {new_minion} on-play effect chose NO target.")
                # Other minion on-play effects could be handled here
            else:
                print(f"DEBUG: Enemy board full, cannot summon {card_to_play.get_name()}.")
        elif isinstance(card_to_play, SpellCard):
            if chosen_target_for_enemy_spell:
                print(f"DEBUG: Enemy's spell {card_to_play} targets {chosen_target_for_enemy_spell}")
                self._apply_effects_and_handle_deaths(card_to_play.get_effect(), chosen_target_for_enemy_spell, f"Enemy's spell {card_to_play}")
            else: # E.g. Heal self
                 print(f"DEBUG: Enemy's spell {card_to_play} (no explicit target or self-target). Applying to enemy hero.")
                 self._apply_effects_and_handle_deaths(card_to_play.get_effect(), self.enemy, f"Enemy's spell {card_to_play}")

        self.remove_defeated_entities()
        return True


    def end_turn_instrumented(self) -> list[str]:
        print("\nDEBUG: ===== End Turn Initiated =====")
        enemy_played_card_names = []

        # 0. Initial state
        print(f"DEBUG (Start of End Turn): Player HP: {self.player.get_health()}, Enemy HP: {self.enemy.get_health()}")
        print(f"DEBUG: Player Minions: {[str(m) for m in self.active_player_minions]}")
        print(f"DEBUG: Enemy Minions: {[str(m) for m in self.active_enemy_minions]}")

        # 1. Player's minions attack
        print("\nDEBUG: --- 1. Player's minions attack ---")
        for minion in list(self.get_player_minions()): # Iterate copy
            if not minion.is_alive(): 
                print(f"DEBUG: Player's {minion} is not alive, skipping attack.")
                continue
            print(f"DEBUG: Player's {minion} (HP: {minion.get_health()}) choosing target.")
            target = minion.choose_target(self.player, self.enemy, self.active_player_minions, self.active_enemy_minions)
            if target:
                print(f"DEBUG: Player's {minion} targets {target} (HP: {target.get_health()}) with effect {minion.get_effect()}")
                self._apply_effects_and_handle_deaths(minion.get_effect(), target, f"Player's {minion}")
            else:
                print(f"DEBUG: Player's {minion} chose no target.")
            if self.has_won() or self.has_lost():
                print("DEBUG: Game ended after player's minion attacks.")
                return enemy_played_card_names
        self.remove_defeated_entities() # Ensure cleanup

        # 2. Enemy hero: new turn sequence
        print("\nDEBUG: --- 2. Enemy hero: new turn sequence ---")
        print(f"DEBUG: Enemy HP before new_turn: {self.enemy.get_health()}, Deck: {self.enemy.deck.remaining_count()}")
        self.enemy.new_turn()
        print(f"DEBUG: Enemy HP after new_turn: {self.enemy.get_health()}, Energy: {self.enemy.get_energy()}/{self.enemy.get_max_energy()}, Hand: {[str(c) for c in self.enemy.get_hand()]}")
        
        # Original check: if not self.enemy.is_alive():
        # Test check: if self.enemy.get_health() <= 0:
        if self.enemy.get_health() <= 0: # Using the modified liveness from user's test
            print(f"DEBUG: Enemy hero has <= 0 HP ({self.enemy.get_health()}) after new_turn. Skipping enemy turn.")
            # If player's new_turn is also skipped, need to consider that.
            # For now, let's assume the original spec: "If the enemy hero is defeated, nothing more happens."
            # This implies player also doesn't get their new_turn sequence if enemy is defeated here.
            return enemy_played_card_names
        print(f"DEBUG: Enemy hero is alive (HP: {self.enemy.get_health()}) and proceeds with turn.")


        # 3. Enemy hero plays cards
        print("\nDEBUG: --- 3. Enemy hero plays cards ---")
        print(f"DEBUG: Enemy hand before playing: {[str(c) for c in self.enemy.get_hand()]}, Energy: {self.enemy.get_energy()}")
        still_can_play = True
        # Create a copy of the hand to iterate over, as playing cards modifies the original hand
        
        # Simplified enemy AI: iterate once, play affordable cards from left.
        # The test implies a more complex AI that might rescan.
        # For this debug, let's try a simple pass or the user's loop structure.
        
        # Using user's loop structure for enemy card play
        temp_enemy_hand = list(self.enemy.get_hand()) # Iterate over a copy for stable indexing if main hand changes
        hand_indices_played_this_turn = [] # To avoid re-playing or issues with list modification

        while still_can_play:
            if not (self.enemy.get_health() > 0) : # Check if enemy is still capable of playing
                print(f"DEBUG: Enemy hero HP is {self.enemy.get_health()}, cannot play more cards.")
                break
            
            played_a_card_this_scan = False
            current_hand_for_scan = list(self.enemy.get_hand()) # Fresh copy for each scan pass
            
            card_played_in_current_pass = False
            for hand_idx, card_to_play in enumerate(current_hand_for_scan):
                print(f"DEBUG: Enemy considering card: {card_to_play} (Cost: {card_to_play.get_cost()}), Energy: {self.enemy.get_energy()}")

                if card_to_play.get_cost() > self.enemy.get_energy():
                    print(f"DEBUG: Enemy cannot afford {card_to_play}.")
                    continue

                chosen_target_for_enemy_spell = None
                if not card_to_play.is_permanent(): # Spell card
                    effect = card_to_play.get_effect()
                    # Simplified AI: Damage player if possible, else target self if beneficial (e.g. Heal)
                    if DAMAGE in effect and self.player.is_alive():
                        chosen_target_for_enemy_spell = self.player
                        print(f"DEBUG: Enemy spell {card_to_play} will target Player Hero {self.player}")
                    elif HEALTH in effect and self.enemy.is_alive(): # e.g. Heal
                        chosen_target_for_enemy_spell = self.enemy
                        print(f"DEBUG: Enemy spell {card_to_play} will target Enemy Hero {self.enemy}")
                    elif self.enemy.is_alive(): # Default for other spells if no clear target
                         chosen_target_for_enemy_spell = self.enemy # Or could be None if no valid target
                         print(f"DEBUG: Enemy spell {card_to_play} will target self (default) {self.enemy}")


                # Find the actual card in the enemy's hand to pass to enemy_play_card
                # This is tricky if hand modified. Best to get card by value if unique or by original index.
                # For simplicity, we assume card_to_play is the one.
                # A more robust way: find card_to_play in self.enemy.get_hand() by identity or unique properties.
                
                # Find the card in the *actual current hand* to attempt to play
                actual_card_to_play_from_hand = None
                original_hand_list = self.enemy.get_hand()
                for c_in_h in original_hand_list:
                    # This assumes card_to_play from the copied list can be identified in the live hand
                    # This might be problematic if cards are not unique enough or if __eq__ is not well-defined
                    if c_in_h is card_to_play: # Check identity first
                        actual_card_to_play_from_hand = c_in_h
                        break
                if not actual_card_to_play_from_hand: # Fallback if identity check fails, try by name and cost (less robust)
                    for c_in_h in original_hand_list:
                        if c_in_h.get_name() == card_to_play.get_name() and c_in_h.get_cost() == card_to_play.get_cost():
                             # This is still risky if multiple identical cards
                             actual_card_to_play_from_hand = c_in_h
                             # To make it slightly more robust for this loop, we'd need to track played cards
                             break 
                
                if not actual_card_to_play_from_hand:
                    print(f"DEBUG: Could not find card {card_to_play} in enemy's current hand to play. Skipping.")
                    continue


                if self.enemy_play_card(actual_card_to_play_from_hand, chosen_target_for_enemy_spell):
                    enemy_played_card_names.append(actual_card_to_play_from_hand.get_name())
                    # Remove the played card from the enemy's hand
                    # This needs to be done carefully by identity or a reliable index
                    try:
                        self.enemy.get_hand().remove(actual_card_to_play_from_hand)
                        print(f"DEBUG: Removed {actual_card_to_play_from_hand} from enemy hand.")
                    except ValueError:
                        print(f"ERROR_DEBUG: Failed to remove {actual_card_to_play_from_hand} from enemy hand after playing.")

                    played_a_card_this_scan = True
                    card_played_in_current_pass = True
                    print(f"DEBUG: Enemy successfully played {actual_card_to_play_from_hand}. Restarting scan of hand.")
                    break # Breaks from inner for loop (scan of current_hand_for_scan)
                else:
                    print(f"DEBUG: Enemy failed to play {actual_card_to_play_from_hand} (e.g. no valid slot for minion).")
            
            if not card_played_in_current_pass: # If a full scan of the hand yielded no plays
                still_can_play = False # Exit the outer while loop
                print("DEBUG: Enemy made a full pass of hand, no card played. Ending card play phase.")
            
            if self.has_won() or self.has_lost():
                print("DEBUG: Game ended after enemy played a card.")
                return enemy_played_card_names
        self.remove_defeated_entities()

        # 4. Enemy's minions attack
        print("\nDEBUG: --- 4. Enemy's minions attack ---")
        for minion in list(self.get_enemy_minions()): # Iterate copy
            if not minion.is_alive():
                print(f"DEBUG: Enemy's {minion} is not alive, skipping attack.")
                continue
            # Check if player hero and all player minions are dead
            player_has_targetable_entities = self.player.is_alive() or any(m.is_alive() for m in self.active_player_minions)
            if not player_has_targetable_entities:
                print(f"DEBUG: Enemy's {minion} has no valid targets (player hero and minions defeated).")
                break 

            print(f"DEBUG: Enemy's {minion} (HP: {minion.get_health()}) choosing target.")
            target = minion.choose_target(self.enemy, self.player, self.active_enemy_minions, self.active_player_minions)
            if target:
                print(f"DEBUG: Enemy's {minion} targets {target} (HP: {target.get_health()}) with effect {minion.get_effect()}")
                self._apply_effects_and_handle_deaths(minion.get_effect(), target, f"Enemy's {minion}")
            else:
                print(f"DEBUG: Enemy's {minion} chose no target.")
            if self.has_won() or self.has_lost():
                print("DEBUG: Game ended after enemy's minion attacks.")
                return enemy_played_card_names
        self.remove_defeated_entities()

        # 5. Player: new turn sequence (if game not over)
        print("\nDEBUG: --- 5. Player: new turn sequence ---")
        # Original: if self.player.is_alive() and not (self.has_won() or self.has_lost()):
        # Test: if self.player.get_health() > 0 and not (self.has_won() or self.has_lost()):
        if self.player.get_health() > 0 and not (self.has_won() or self.has_lost()):
            print(f"DEBUG: Player HP before new_turn: {self.player.get_health()}")
            self.player.new_turn()
            print(f"DEBUG: Player HP after new_turn: {self.player.get_health()}, Energy: {self.player.get_energy()}/{self.player.get_max_energy()}, Hand: {[str(c) for c in self.player.get_hand()]}")
        else:
            print("DEBUG: Player is not alive or game ended, skipping player's new turn sequence.")
        
        print("\nDEBUG: ===== End Turn Finished =====")
        return enemy_played_card_names

    def __str__(self) -> str:
        player_hero_str = str(self.player)
        player_minions_str = ";".join([str(m) for m in self.active_player_minions])
        enemy_hero_str = str(self.enemy)
        enemy_minions_str = ";".join([str(m) for m in self.active_enemy_minions])
        return f"{player_hero_str}|{player_minions_str}|{enemy_hero_str}|{enemy_minions_str}"

# --- Helper to build cards/minions based on test setup ---
def build_cards_debug(symbols: list[str], for_hand: bool = False) -> list:
    items = []
    for sym in symbols:
        if for_hand: # Create Card objects for hand/deck
            if sym == 'R': items.append(MinionCard(RAPTOR_NAME, 2, 1, 0, RAPTOR_SYMBOL, Raptor)) # Assume 1/0 for hand card to board
            elif sym == 'W': items.append(FireballCard(cost=2, damage_val=2)) # Player's 'W' Fireball, cost 2, 2 damage? Test implies.
            elif sym == '3': items.append(FireballCard(cost=3, initial_delay=3, damage_val=3)) # A different Fireball
            elif sym == 'S': items.append(SpellCard(SHIELD_CARD_NAME, 1, {SHIELD: 5}, SHIELD_CARD_SYMBOL))
            elif sym == 'H': items.append(SpellCard(HEAL_CARD_NAME, 2, {HEALTH: 3}, HEAL_CARD_SYMBOL))
            # Enemy hand cards from test: ['W', 'W', 'H', '0', 'S']
            # 'W' for enemy hand could be WyrmPlayableCard or another Fireball. Let's assume Wyrm.
            elif sym == '0': items.append(FireballCard(cost=3, initial_delay=0, damage_val=3)) # '0' is Fireball ready
            else: items.append(Card(f"UnknownCard({sym})", 1)) # Fallback
        else: # Create Minion objects directly for board
            if sym == 'W': items.append(Wyrm(1, 0))
            elif sym == 'R': items.append(Raptor(1, 0))
            else: items.append(Minion(1,0, f"UnknownMinion({sym})", 0)) # Fallback
    return items

def build_enemy_hand_cards_debug(symbols: list[str]) -> list[Card]:
    items = []
    # Enemy hand: ['W', 'W', 'H', '0', 'S']
    for sym in symbols:
        if sym == 'W': items.append(MinionCard(WYRM_NAME, 2, 1, 0, WYRM_SYMBOL, Wyrm)) # Wyrm card
        elif sym == 'H': items.append(SpellCard(HEAL_CARD_NAME, 2, {HEALTH: 3}, HEAL_CARD_SYMBOL))
        elif sym == '0': items.append(FireballCard(name="EnemyFireball",cost=3, initial_delay=0, damage_val=3)) # Ready Fireball
        elif sym == 'S': items.append(SpellCard(SHIELD_CARD_NAME, 1, {SHIELD: 5}, SHIELD_CARD_SYMBOL))
        else: items.append(Card(f"UnknownEnemyCard({sym})", 1))
    return items


# --- Main Test Scenario Setup & Execution ---
if __name__ == "__main__":
    print("--- Debug Script for test_end_turn ---")

    # Player setup from test_end_turn
    player_card_symbols = ['S', 'H', '1', 'R', 'W', 'S', 'H', '0', '0', 'R', 'S', 'H', '0', '0', 'R', 'S', 'H', '0', '0', 'R']
    player_deck_cards = build_cards_debug(player_card_symbols, for_hand=True)
    player_deck = CardDeck(player_deck_cards)
    
    player_hand_symbols = ['R', 'W', '3', 'S', 'H'] # R, Fireball(W), Fireball(3), Shield, Heal
    player_hand_cards = build_cards_debug(player_hand_symbols, for_hand=True)
    player_hero = Hero(health=10, shield=10, max_energy=5, deck=player_deck, hand=player_hand_cards, name="PlayerHero")
    
    player_minion_symbols = ['W', 'R'] # Wyrm(1,0), Raptor(1,0) on board
    player_initial_minions = build_cards_debug(player_minion_symbols, for_hand=False)

    # Enemy setup from test_end_turn
    enemy_card_symbols = ['R', 'W', 'S', 'H', 'R', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9']
    enemy_deck_cards = build_cards_debug(enemy_card_symbols, for_hand=True) # Assuming 'R' and 'W' are minion cards
    enemy_deck = CardDeck(enemy_deck_cards)

    enemy_hand_symbols = ['W', 'W', 'H', '0', 'S'] # WyrmCard, WyrmCard, Heal, Fireball(0), Shield
    enemy_hand_cards = build_enemy_hand_cards_debug(enemy_hand_symbols)
    enemy_hero = Hero(health=20, shield=5, max_energy=5, deck=enemy_deck, hand=enemy_hand_cards, name="EnemyHero")

    enemy_minion_symbols = ['R', 'R', 'R', 'R', 'R'] # Five Raptor(1,0) on board
    enemy_initial_minions = build_cards_debug(enemy_minion_symbols, for_hand=False)

    # Initialize Model
    model = HearthModel_Debug(
        player_hero, 
        player_initial_minions,
        enemy_hero,
        enemy_initial_minions
    )
    print("\nDEBUG: ===== Initial Model State =====")
    print(str(model))

    # Simulate pre-end_turn actions from test_end_turn
    print("\nDEBUG: ===== Simulating pre-end_turn card plays by Player =====")
    # 1. Player plays first card from hand (RaptorCard)
    if model.player.get_hand():
        card_to_play1 = model.player.get_hand()[0] # Should be RaptorCard
        print(f"DEBUG: Player pre-play 1: Card is {card_to_play1}")
        # Minions don't need an explicit target for summoning in this simplified play_card
        model.play_card(card_to_play1) 
    else:
        print("DEBUG: Player hand empty for first pre-play.")
    print(f"DEBUG: Model state after player pre-play 1: {str(model)}")


    # 2. Player plays second card from hand (Fireball 'W') targeting enemy hero
    if len(model.player.get_hand()) > 0: # Hand was modified
        # The original hand was ['R', 'W', '3', 'S', 'H']. After playing 'R', hand[0] is now 'W'.
        card_to_play2 = model.player.get_hand()[0] # Should be FireballCard ('W')
        print(f"DEBUG: Player pre-play 2: Card is {card_to_play2}")
        if isinstance(card_to_play2, FireballCard):
             model.play_card(card_to_play2, target=model.enemy)
        else:
            print(f"DEBUG: Expected Fireball for pre-play 2, got {type(card_to_play2)}")
            model.play_card(card_to_play2, target=model.enemy) # Attempt anyway
    else:
        print("DEBUG: Player hand empty for second pre-play.")
    print(f"DEBUG: Model state after player pre-play 2: {str(model)}")
    print(f"DEBUG: Enemy Hero HP before first end_turn: {model.enemy.get_health()}")


    # Call the instrumented end_turn
    print("\nDEBUG: ===== CALLING end_turn_instrumented (First Call) =====")
    played_by_enemy = model.end_turn_instrumented()
    print(f"\nDEBUG: Cards played by enemy: {played_by_enemy}")

    print("\nDEBUG: ===== Final Model State after first end_turn =====")
    final_state_str = str(model)
    print(final_state_str)

    # Compare with expected from test (manually or by diffing output)
    # Expected: '10,1[70 chars],W,S,H,R,9,9,9,9,9,9,9,9,9,9;1,S|R,2,1;R,2,1;R,1,0;W,1,0;W,1,0'
    # Your output was: '10,1[70 chars],W,S,H,R,9,9,9,9,9,9,9,9,9,9;1,S|R,2,1;R,2,1;W,2,1;W,2,1'
    # The player part and enemy hero part matched in the diff. Focus on enemy minions.
    # Expected enemy minions: R,2,1;R,2,1;R,1,0;W,1,0;W,1,0
    # Your enemy minions:   R,2,1;R,2,1;W,2,1;W,2,1

    print("\n--- End of Debug Script ---")
