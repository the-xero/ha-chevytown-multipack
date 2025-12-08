# Multipack - 쉐비타운 멀티팩 커넥티드

Home Assistant 통합으로 쉐비타운 멀티팩 API를 통해 차량을 제어합니다.

## 설치

HACS를 통해 설치하거나 `custom_components/multipack` 디렉터리에 파일을 복사하세요.

## 설정

**설정 > 기기 및 서비스 > 통합 추가 > Multipack**

다음 정보를 입력하세요:
- **자동차 이름**: 차량 이름 (예: "Malibu", "Equinox") - 엔티티 ID 접두사로 사용됨
- **사용자 ID**: Multipack 계정 ID
- **API Key**: Multipack API 키
- **알림 엔티티(선택)**: Companion 앱이 제공하는 last_notification 센서 ID (예: sensor.s24_ultra_last_notification). 이 값을 입력하면 명령 전송 후 해당 알림 메시지를 확인하여 실제 수행 결과(success/failure)를 판단합니다.

> ⚠️ **주의**   
> 설정 후 처음 연동 시, API 인증 검증을 위해 자동으로 **도어 잠금 명령이 1회 실행됩니다**.    
> 이 구성 요소는 단순 명령을 전송하는 기능만 수행합니다. 명령 전송의 성공여부는 전용 앱의 알림(또는 API 응답)이 확인될 때까지 보류될 수 있습니다.

## 기능

- 원격 시동 켜기/끄기
- 도어 잠금/해제
- 창문 열기/닫기
- 트렁크 열기/닫기
- 경적 울리기
- 썬루프 제어

## 요구사항

- Home Assistant 2023.12.0 이상
