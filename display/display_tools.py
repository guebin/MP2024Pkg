from collections.abc import Iterable

def show_dict_info(dct):
    """Displays an overview of a dictionary's keys, type, length, and limited values."""
    print("Dictionary Overview:")
    print(f"Total keys: {len(dct.keys())}")
    print(f"Keys: {list(dct.keys())}\n")
    
    for i, (k, v) in enumerate(dct.items()):
        print(f"{i+1}. Key: '{k}'")
        print(f"   - Type: {type(v).__name__}")

        if hasattr(v, "__len__"):
            print(f"   - Length: {len(v)}")

        if len(str(v)) > 100:
            display_values = str(v)[:100] + "..."
        else:
            display_values = str(v)

        print(f"   - Values: {display_values}")
        print()


def show_nested(item, level=1, max_depth=2):
    """Displays type, length, and example values of nested items up to the specified depth."""
    if level > max_depth:
        return
    
    item_type = type(item).__name__
    item_len = len(item) if hasattr(item, '__len__') else None
    
    item_str = repr(item)
    if len(item_str) > 50:
        example = f"{item_str[:25]} ... {item_str[-25:]}"
    else:
        example = item_str

    info = f"{' ' * (level - 1) * 5}Level {level} - Type: {item_type}"
    if item_len is not None:
        info += f", Length: {item_len}"
    info += f", Example: {example}"
    
    print(info)

    if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
        for subitem in item:
            show_nested(subitem, level + 1, max_depth)
