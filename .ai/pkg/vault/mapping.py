"""
Vault type-to-folder mapping operations.

Handles mapping entry types to their folder locations in the vault.
"""


def get_folder_prefix_for_type(entry_type: str) -> str:
    """
    Map entry type to folder prefix.
    
    Args:
        entry_type: The type of vault entry (e.g., "npc", "location").
    
    Returns:
        Folder prefix for the entry type.
    """
    type_to_prefix = {
        "template": "00 Templates",
        "arc": "01 Arcs",
        "player": "02 Players",
        "npc": "03 NPCs",
        "session": "04 Sessions",
        "faction": "05 Factions",
        "location": "06 Locations",
        "hook": "07 Hooks",
        "scene": "08 Scenes",
        "item": "09 Items",
        "lore": "10 Lore",
        "spren": "31 Spren"
    }
    return type_to_prefix.get(entry_type, "")


def get_folder_from_type(entry_type: str) -> str:
    """
    Return the folder path for a vault entry type.
    
    Args:
        entry_type: The type of vault entry.
    
    Returns:
        Folder path for the entry type.
    """
    return get_folder_prefix_for_type(entry_type)


def get_filepath_from_name_and_type(name: str, entry_type: str) -> str:
    """
    Reconstruct filepath from name and type.
    
    Args:
        name: The entry name.
        entry_type: The entry type.
    
    Returns:
        Full filepath including folder and .md extension.
    """
    prefix = get_folder_from_type(entry_type)
    if prefix:
        return f"{prefix}/{name}.md"
    else:
        return f"{name}.md"


def get_filepath_from_name(name: str, file_type: str) -> str:
    """
    Reconstruct filepath from name and type (alias for consistency).
    
    Args:
        name: The entry name.
        file_type: The entry type.
    
    Returns:
        Full filepath including folder and .md extension.
    """
    folder = get_folder_from_type(file_type)
    if folder:
        return f"{folder}/{name}.md"
    else:
        raise ValueError(f"Invalid type: {file_type} for entry {name}")
