# 커스텀 디바이스 설정
custom_devices = {
"""
모바일 디바이스 추가
context = browser.new_context(**custom_devices["Galaxy S24"])로 실행
new_context는 playwright에서 제공하는 내장 함수
"""
    "Galaxy S24": {
        "user_agent": "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "viewport": {"width": 412, "height": 915},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    },
    "iPhone 16": {
        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/537.36",
        "viewport": {"width": 430, "height": 932},
        "device_scale_factor": 3,
        "is_mobile": True,
        "has_touch": True,
    }
}
