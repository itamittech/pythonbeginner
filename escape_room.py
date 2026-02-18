"""
Text Adventure Game
===================
Architecture: Single-script, data-driven design.
Game state is managed in a PlayerState dataclass.
Rooms/choices are defined as a nested dict — making it easy to extend
without touching game-loop logic (Open/Closed Principle).
"""

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Player State — single source of truth for runtime state
# ---------------------------------------------------------------------------
@dataclass
class PlayerState:
    inventory: set = field(default_factory=set)
    escaped: bool = False


# ---------------------------------------------------------------------------
# World Definition — data-driven; add new rooms/choices here freely
# Each top-level key is a main room.
# Each choice inside has: 'desc', optional 'item' to pick up,
# optional 'requires' (item needed), optional 'escape' flag.
# ---------------------------------------------------------------------------
WORLD = {
    "1": {
        "name": "Dark Forest",
        "choices": {
            "a": {
                "desc": "You search under a mossy rock and find a rusty KEY.",
                "item": "key"
            },
            "b": {
                "desc": "You climb a tree but find nothing useful. You climb back down.",
            },
            "0": {"desc": "Go back to the main hall.", "back": True}
        }
    },
    "2": {
        "name": "Old Kitchen",
        "choices": {
            "a": {
                "desc": "You open the pantry and find a juicy APPLE. You take it.",
                "item": "apple"
            },
            "b": {
                "desc": "You check the oven. It's cold and empty.",
            },
            "0": {"desc": "Go back to the main hall.", "back": True}
        }
    },
    "3": {
        "name": "Locked Door",
        "choices": {
            "a": {
                "desc": "You insert the key — the door swings open. You ESCAPE!",
                "requires": "key",
                "escape": True
            },
            "b": {
                "desc": "You ram the door with your shoulder. It doesn't budge.",
            },
            "0": {"desc": "Go back to the main hall.", "back": True}
        }
    },
    "4": {
        "name": "Dusty Library",
        "choices": {
            "a": {
                "desc": "You read an old journal. It hints: 'The key lies where moss grows.'",
            },
            "b": {
                "desc": "You pull a book — a secret passage reveals... a spider. Nope.",
            },
            "0": {"desc": "Go back to the main hall.", "back": True}
        }
    }
}


# ---------------------------------------------------------------------------
# Display Helpers
# ---------------------------------------------------------------------------
def show_main_menu():
    print("\n" + "=" * 45)
    print("  YOU WAKE UP IN A STRANGE MANSION.")
    print("  Where do you go?")
    print("=" * 45)
    for key, room in WORLD.items():
        print(f"  [{key}] {room['name']}")
    print("  [0] Quit")
    print("-" * 45)


def show_room_menu(room: dict, state: PlayerState):
    print(f"\n--- {room['name']} ---")
    print(f"  Inventory: {', '.join(state.inventory) if state.inventory else 'empty'}")
    print("  What do you do?")
    for key, choice in room["choices"].items():
        print(f"  [{key}] {choice['desc']}")
    print("-" * 35)


# ---------------------------------------------------------------------------
# Room Interaction — handles item pickup, escape, and requirement checks
# ---------------------------------------------------------------------------
def handle_room(room_key: str, state: PlayerState):
    room = WORLD[room_key]

    while True:
        show_room_menu(room, state)
        choice_key = input("  Your choice: ").strip().lower()

        if choice_key not in room["choices"]:
            print("  Invalid choice, try again.")
            continue

        choice = room["choices"][choice_key]

        # Back to main hall
        if choice.get("back"):
            return

        # Check if an item is required (e.g., key to open door)
        required = choice.get("requires")
        if required and required not in state.inventory:
            print(f"  [!] You need a {required} to do that.")
            continue

        # Narrate the outcome
        print(f"\n  >> {choice['desc']}")

        # Pick up item if present and not already in inventory
        item = choice.get("item")
        if item and item not in state.inventory:
            state.inventory.add(item)
            print(f"  [+] {item.upper()} added to inventory.")

        # Escape condition
        if choice.get("escape"):
            state.escaped = True
            return

        # After an action (non-back), ask if they want to stay or leave
        again = input("\n  Stay in this room? (y/n): ").strip().lower()
        if again != "y":
            return


# ---------------------------------------------------------------------------
# Main Game Loop
# ---------------------------------------------------------------------------
def main():
    print("\n*** WELCOME TO THE MANSION ESCAPE ***")
    state = PlayerState()

    while not state.escaped:
        show_main_menu()
        choice = input("  Your choice: ").strip()

        if choice == "0":
            print("\n  You chose to quit. Goodbye!\n")
            break

        if choice not in WORLD:
            print("  Invalid option, try again.")
            continue

        handle_room(choice, state)

        if state.escaped:
            print("\n" + "=" * 45)
            print("  🎉 CONGRATULATIONS! You escaped the mansion!")
            inv = ', '.join(state.inventory)
            print(f"  Items collected: {inv}")
            print("=" * 45 + "\n")


if __name__ == "__main__":
    main()