import os 
import inspect
import types
import pandas as pd 
import IPython.display
#--#
from collections.abc import Iterable

def show_list(items, max_depth=2, max_head=5, max_tail=5):
    """Displays type, length, and content of nested list items in a structured format."""
    
    # Display overview of the list
    items_type = type(items).__name__
    try:
        items_len = len(items)
    except TypeError:
        items_len = None  # Length is undefined for non-sequence types
    
    print("List Overview:")
    if items_len is not None:
        print(f"Total items: {items_len}")

    # Display list items with head and tail view
    for index, item in enumerate(items):
        # Skip middle items, showing head and tail only
        if index >= max_head and index < items_len - max_tail:
            if index == max_head:
                print("...")
            continue

        item_type = type(item).__name__
        try:
            item_len = len(item)
        except TypeError:
            item_len = None

        # Print item details
        print(f"\n{index + 1}. list[{index}]")
        print(f"   - Type: {item_type}")
        if item_len is not None:
            print(f"   - Length: {item_len}")
        print(f"   - Value: {item}")

def show_dict(dct):
    """Displays type, length, and content of dictionary items in a structured format."""
    
    print("Dictionary Overview:")
    print(f"Total keys: {len(dct.keys())}")
    print(f"Keys: {list(dct.keys())}\n")
    
    for i, (key, value) in enumerate(dct.items()):
        print(f"{i + 1}. dict['{key}']")
        print(f"   - Type: {type(value).__name__}")

        # Display length if possible
        if hasattr(value, "__len__"):
            print(f"   - Length: {len(value)}")

        # Display value
        print(f"   - Value: {value}")

def tree(start_path='.', prefix='', max_depth=5, current_depth=0):
    """
    현재 디렉터리 구조를 트리 형식으로 출력하되, 지정된 깊이를 초과하거나 파일이 너무 많을 경우 생략한다.
    
    Parameters:
    - start_path: 탐색을 시작할 디렉터리 경로 (기본값: 현재 디렉터리 '.')
    - prefix: 트리 구조에서 들여쓰기 역할을 할 문자열
    - max_depth: 최대 탐색 깊이. 이 깊이를 초과하면 생략함.
    - current_depth: 현재 탐색 깊이 (내부적으로 사용됨)
    """
    if current_depth > max_depth:
        print(prefix + "└── ...")
        return

    files = os.listdir(start_path)
    files.sort()  # 알파벳 순으로 정렬
    
    # 파일이 너무 많으면 중간 생략
    if len(files) > 4:
        display_files = files[:2] + ["..."] + files[-1:]
    else:
        display_files = files

    for i, name in enumerate(display_files):
        path = os.path.join(start_path, name)
        if name == "...":
            print(prefix + "└── " + name)
            continue
        
        connector = '└── ' if i == len(display_files) - 1 else '├── '
        print(prefix + connector + name)
        
        if os.path.isdir(path):  # 디렉터리인 경우
            new_prefix = '    ' if i == len(display_files) - 1 else '│   '
            tree(path, prefix + new_prefix, max_depth, current_depth + 1)

def signature(func):
    """
    주어진 함수 또는 메서드의 서명을 보기 좋게 출력한다.
    
    Parameters:
    - func: 서명을 출력할 함수 또는 메서드
    """
    # 함수 또는 메서드의 서명을 가져오기
    try:
        sig = inspect.signature(func)
        # 인수 부분을 줄바꿈하여 보기 좋게 포맷팅
        parameters = "\n".join([f"    {name}: {param.annotation} = {param.default}" 
                                for name, param in sig.parameters.items()])
        return_annotation = sig.return_annotation

        # func가 함수일 경우 __qualname__을 사용, 그렇지 않으면 클래스 이름을 사용
        func_name = func.__qualname__ if hasattr(func, '__qualname__') else func.__class__.__name__

        # 서명 전체를 포맷팅하여 Markdown으로 출력
        formatted_signature = f"""```python
{func_name}(
{parameters}
) -> {return_annotation}
```"""

        IPython.display.display(IPython.display.Markdown(formatted_signature))

    except AttributeError:
        print("The provided object does not have a valid signature.")


def tab(module, include_private=False):
    """
    This function inspects the contents of a given module and returns details 
    about its components, including the name, type, and a brief description if possible.
    The output is sorted by type for better organization and displayed as a nested pandas DataFrame.
    
    Parameters:
    - module: The module to inspect.
    - include_private (bool): If True, includes private members (those starting with '_').
    """
    # List to hold information about module contents, grouped by type
    module_info = []

    for item_name in dir(module):
        # Optionally skip private and special methods/attzributes
        if not include_private and item_name.startswith('_'):
            continue

        # Get the item from the module
        item = getattr(module, item_name)

        # Determine type of the item
        item_type = type(item).__name__

        # Generate a full description using inspect.getdoc() without special characters
        description = inspect.getdoc(item)
        if description:
            # Remove leading/trailing whitespace and replace internal newlines
            description = description.strip()
        else:
            description = None  # Set to None if no description available

        # Append item information to list
        module_info.append({
            'Type': item_type,
            'Name': item_name,
            'Description': description
        })

    # Convert to DataFrame
    df = pd.DataFrame(module_info)

    # Add 'Description_present' column for sorting (True if Description exists, False otherwise)
    df['Description_present'] = df['Description'].notna()

    # Sort by 'Type', 'Description_present' (True first), then by 'Name'
    df = df.sort_values(
        by=['Type', 'Description_present', 'Name'],
        ascending=[True, False, True]
    ).drop(columns='Description_present')  # Drop temporary column after sorting

    # Set index for a nested view
    nested_df = df.set_index(['Type', 'Name'])

    # Apply styling to make 'Description' column left-aligned
    styled_df = nested_df.style.set_properties(subset=['Description'], **{'text-align': 'left'})
    return styled_df

def show(item, max_depth=2, max_head_items=5, max_tail_items=5, max_value_length=100000):
    """Displays type, length, and content of list or dictionary in a structured format, truncating long values."""
    def truncate_value(value):
        """Truncates the value to show only the first 100 and last 100 words if it is too long."""
        value_str = str(value)
        words = value_str.split()
        if len(words) > 200:
            return " ".join(words[:100]) + " ... " + " ".join(words[-100:])
        return value_str

    item_type = type(item).__name__
    
    try: 
        item.keys()
        print("Dictionary Overview:")
        print(f"Total keys: {len(item.keys())}")
        print(f"Keys: {list(item.keys())}\n")
        
        for i, (k, v) in enumerate(item.items()):
            print(f"{i+1}. dict['{k}']")
            print(f"   - Type: {type(v).__name__}")

            if hasattr(v, "__len__"):
                print(f"   - Length: {len(v)}")
            
            print(f"   - Values: {truncate_value(v)}")
    except:
        if isinstance(item, Iterable):
            try:
                item_len = len(item)
            except TypeError:
                item_len = None
            
            print("List Overview:")
            if item_len is not None:
                print(f"Total items: {item_len}")
            
            # Display list items with head and tail view
            for idx, subitem in enumerate(item):
                if idx >= max_head_items and idx < item_len - max_tail_items:
                    if idx == max_head_items:
                        print("...")
                    continue

                subitem_type = type(subitem).__name__
                try:
                    subitem_len = len(subitem)
                except TypeError:
                    subitem_len = None

                print(f"\n{idx + 1}. list[{idx}]")
                print(f"   - Type: {subitem_type}")
                if subitem_len is not None:
                    print(f"   - Length: {subitem_len}")
                print(f"   - Values: {truncate_value(subitem)}")    
        else:
            print(f"Unsupported item type: {item_type}")
