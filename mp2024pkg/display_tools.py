from collections.abc import Iterable

def show_nested(item, level=1, max_depth=2):
    """Displays type, length, and example values of nested items up to the specified depth."""
    if level > max_depth:
        return

    # 아이템 타입과 길이 정보 확인
    item_type = type(item).__name__
    try:
        item_len = len(item)
    except TypeError:
        item_len = None  # 길이를 구할 수 없는 경우

    # 예시 문자열 생성 (중간 생략)
    item_str = repr(item)
    if len(item_str) > 50:
        example = f"{item_str[:25]} ... {item_str[-25:]}"
    else:
        example = item_str

    # 출력 정보 포맷팅
    info = f"{' ' * (level - 1) * 5}Level {level} - Type: {item_type}"
    if item_len is not None:
        info += f", Length: {item_len}"
    info += f", Example: {example}"
    
    print(info)

    # Iterable을 확인하고 길이 구할 수 없는 경우 반복하지 않음
    if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
        if item_len is None:
            return  # 길이를 구할 수 없는 객체는 반복하지 않음
        for subitem in item:
            show_nested(subitem, level + 1, max_depth)

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
        print()  # 공백 줄 추가
