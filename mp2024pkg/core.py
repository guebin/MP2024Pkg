from collections.abc import Iterable
import os 
import inspect
import IPython.display

def show_list(item, max_depth=2, max_items=5):
    """Displays type, length, and content of nested items up to level 2."""
    
    # Level 1 information
    item_type = type(item).__name__
    try:
        item_len = len(item)
    except TypeError:
        item_len = None  # If length cannot be determined
    
    item_str = repr(item)
    if len(item_str) > 50:
        content = f"{item_str[:25]} ... {item_str[-25:]}"
    else:
        content = item_str
    
    info = f"Level 1 - Type: {item_type}"
    if item_len is not None:
        info += f", Length: {item_len}"
    info += f", Content: {content}"
    print(info)

    # Level 2 information (only if item is Iterable)
    if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
        if item_len is None:
            return  # Skip if length cannot be determined
        for idx, subitem in enumerate(item):
            if idx == max_items // 2 and item_len > max_items:
                print(f"     ...")
            elif idx >= max_items and idx < item_len - max_items // 2:
                continue

            subitem_type = type(subitem).__name__
            try:
                subitem_len = len(subitem)
            except TypeError:
                subitem_len = None
            
            subitem_str = repr(subitem)
            if len(subitem_str) > 50:
                sub_content = f"{subitem_str[:25]} ... {subitem_str[-25:]}"
            else:
                sub_content = subitem_str

            sub_info = f"     Level 2 - Type: {subitem_type}"
            if subitem_len is not None:
                sub_info += f", Length: {subitem_len}"
            sub_info += f", Content: {sub_content}"
            print(sub_info)

def show_dict(dct):
    print("Dictionary Overview:")
    print(f"Total keys: {len(dct.keys())}")
    print(f"Keys: {list(dct.keys())}\n")
    
    for i, (k, v) in enumerate(dct.items()):
        print(f"{i+1}. Key: '{k}'")
        print(f"   - Type: {type(v).__name__}")

        # 길이 확인이 가능한 타입인 경우 길이 정보 출력
        if hasattr(v, "__len__"):
            print(f"   - Length: {len(v)}")

        # Iterable 값의 길이를 제한해 출력
        if len(str(v)) > 100:
            display_values = str(v)[:100] + "..."  # 문자열 길이 제한 후 생략 표시
        else:
            display_values = str(v)

        # 값 출력
        print(f"   - Values: {display_values}")

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
    
    # 파일이 너무 많으면 앞 3개, 뒤 3개만 표시하고 중간 생략
    if len(files) > 6:
        display_files = files[:3] + ["..."] + files[-3:]
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
    # 함수의 서명을 가져오기
    sig = inspect.signature(func)
    # 인수 부분을 줄바꿈하여 보기 좋게 포맷팅
    parameters = "\n".join([f"    {name}: {param.annotation} = {param.default}" 
                            for name, param in sig.parameters.items()])
    return_annotation = sig.return_annotation

    # 서명 전체를 포맷팅하여 Markdown으로 출력
    formatted_signature = f"""```python
{func.__qualname__}(
{parameters}
) -> {return_annotation}
```"""

    IPython.display.display(IPython.display.Markdown(formatted_signature))
