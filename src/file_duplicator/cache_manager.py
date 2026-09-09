import json
import os

from .constants import CACHE_FILE

# 캐시 파일 저장 경로 설정
# CACHE_FILE = "cache_data.json"


def save_cache(data):
    """
    데이터를 JSON 형식의 캐시 파일로 저장합니다.
    :param data: 저장할 딕셔너리 데이터
    """
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        # print(f"✅ 캐시 저장 성공: {CACHE_FILE}")
    except Exception as e:
        print(f"❌ 캐시 저장 실패: {e}")



def load_cache():
    """
    저장된 캐시 파일을 불러옵니다. 파일이 없으면 빈 딕셔너리를 반환합니다.
    :return: 불러온 딕셔너리 데이터
    """
    if not os.path.exists(CACHE_FILE):
        print("ℹ️ 저장된 캐시 파일이 없습니다. 기본값을 사용합니다.")
        return {}
        
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # print(f"✅ 캐시 불러오기 성공: {data}")
            return data
    except (json.JSONDecodeError, Exception) as e:
        print(f"❌ 캐시 불러오기 실패 (파일 손상 등): {e}")
        return {}



def get_cache(key):
    """
    load_cache 후 키 값을 바로 찾아 리턴.
    """
    
    cache = load_cache()
    if key in cache:
        return cache[key]
    return None


def update_cache(key, value):
    """
    load cache 후 값을 입력하고 바로 덮어씀.
    """
    cache = load_cache()
    cache[key] = value
    save_cache(cache)


# 사용 예시 (테스트용)
if __name__ == "__main__":
    print("--- 1. 첫 실행 (캐시 파일이 없는 상태) ---")
    user_settings = load_cache()
    
    print("\n--- 2. 새로운 데이터 캐시 저장 ---")
    # 저장할 데이터 예시 (EXE 실행 시 유지하고 싶은 모든 데이터 가능)
    current_data = {
        "user_id": "user_123",
        "last_login": "2026-09-09",
        "window_width": 1280,
        "window_height": 720,
        "auto_login": True
    }
    save_cache(current_data)
    
    print("\n--- 3. 저장 후 다시 캐시 불러오기 ---")
    saved_settings = load_cache()
    print(f"최종 불러온 데이터: {saved_settings}")
