DOMAIN = "multipack"
API_BASE_URL = "https://mp.gmone.co.kr/api"

COMMANDS = {
    "vehicle_start": {"name": "원격 시동 켜기", "cmd": "VEHICLE_START", "icon": "mdi:car-start"},      
    "vehicle_stop":  {"name": "원격 시동 끄기", "cmd": "VEHICLE_STOP", "icon": "mdi:car"},       
    "door_lock":     {"name": "도어 잠금", "cmd": "DOOR_LOCK", "icon": "mdi:lock"},
    "door_unlock":   {"name": "도어 열기", "cmd": "DOOR_UNLOCK", "icon": "mdi:lock-open"},
    "window_open":   {"name": "창문 열기", "cmd": "WINDOW_OPEN", "icon": "mdi:window-open"},
    "window_close":  {"name": "창문 닫기", "cmd": "WINDOW_CLOSE", "icon": "mdi:window-closed"},
    "trunk_open":    {"name": "트렁크 열기", "cmd": "TRUNK_OPEN", "icon": "mdi:car"},
    "trunk_close":   {"name": "트렁크 닫기", "cmd": "TRUNK_CLOSE", "icon": "mdi:car"},
    "panic":         {"name": "경적", "cmd": "PANIC", "icon": "mdi:car-horn"},
    "sunroof_open":  {"name": "썬루프 열기", "cmd": "SUNROOF_OPEN", "icon": "mdi:car"},
    "sunroof_close": {"name": "썬루프 닫기", "cmd": "SUNROOF_CLOSE", "icon": "mdi:car"},
    "sunroof_tilt":  {"name": "썬루프 틸트", "cmd": "SUNROOF_TILT", "icon": "mdi:car"}       
}
