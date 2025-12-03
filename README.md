# Multipack 통합(Home Assistant)

이 통합을 사용하면 Home Assistant에서 쉐비타운 멀티팩 커넥티드 시공 차량을 원격으로 제어할 수 있습니다.  
엔진 시동, 도어 잠금/해제, 창문 및 트렁크 열기/닫기, 경적(패닉), 썬루프 제어 등을 Lovelace UI에서 편리하게 수행할 수 있습니다.

이 코드는 AI로 생성되어 제대로 동작하지 않을 수 있습니다.

---

## 기능

- 원격 엔진 시동 / 정지
- 도어 잠금 / 열기
- 창문 열기 / 닫기
- 트렁크 열기 / 닫기
- 경적(패닉) 작동
- 썬루프 열기 / 닫기 / 틸트
- 마지막 실행 명령 센서
- 명령 성공/실패 알림
- 각 기능별 Lovelace 버튼 제공

---

## 설치

### HACS 

1. **HACS > Integrations > Explore & Add Repositories** 로 이동
2. `https://github.com/the-xero/ha-chevytown-multipack` 추가
3. `multipack ` 설치 후 HA 재시작하여 사용

### 수동 설치

1. `custom_components/multipack/` 폴더를 Home Assistant `config/custom_components/` 경로에 복사
2. Home Assistant 재시작

---

## 설정

설치 후, **설정(Settings) > 장치 및 서비스(Devices & Services) > 통합 추가(Add Integration)** 에서 **Multipack** 선택  
아래 정보를 입력해야 합니다:

- **사용자 ID(User ID)**: Multipack 계정 ID
- **API 키(API Key)**: Multipack API 키

> 입력한 인증 정보는 Home Assistant에서 안전하게 저장되며 평문으로 표시되지 않습니다.

---

## Lovelace UI 예시

통합 설치 후, Lovelace 카드에서 차량을 제어할 수 있습니다:

```yaml
type: horizontal-stack
cards:
  - type: button
    entity: button.multipack_vehicle_start
    name: 원격 시동 켜기
    icon: mdi:car-start
  - type: button
    entity: button.multipack_vehicle_stop
    name: 원격 시동 끄기
    icon: mdi:car-stop
  - type: button
    entity: button.multipack_door_lock
    name: 도어 잠금
    icon: mdi:lock
  - type: button
    entity: button.multipack_door_unlock
    name: 도어 열기
    icon: mdi:lock-open
```
창문, 트렁크, 경적, 썬루프 버튼도 동일한 방식으로 추가 가능

---

## 센서

- `sensor.multipack_last_action`: 마지막으로 실행한 명령과 실행 결과(성공/실패)를 표시

---

## 알림

명령 실행 시, 설정된 모바일 기기나 워치 등으로 명령 실행 결과를 알림으로 받을 수 있습니다.

---

## 참고

- 스크립트가 정상적으로 실행되지 않을 경우, Home Assistant 로그를 확인하세요.
- HACS 또는 수동 설치 후, 반드시 Home Assistant를 재시작해야 합니다.
- `button` 엔티티를 Lovelace UI에서 사용하여 스크립트 실행이 가능합니다.
- 마지막 실행 명령 센서를 Lovelace에서 표시하면, 명령 성공/실패를 실시간으로 확인할 수 있습니다.

---

## 예시: 전체 Lovelace 카드 구성

```yaml
type: vertical-stack
cards:
  - type: horizontal-stack
    cards:
      - type: button
        entity: button.multipack_vehicle_start
        name: 원격 시동 켜기
        icon: mdi:car-start
      - type: button
        entity: button.multipack_vehicle_stop
        name: 원격 시동 끄기
        icon: mdi:car-stop
      - type: button
        entity: button.multipack_door_lock
        name: 도어 잠금
        icon: mdi:lock
      - type: button
        entity: button.multipack_door_unlock
        name: 도어 열기
        icon: mdi:lock-open

  - type: horizontal-stack
    cards:
      - type: button
        entity: button.multipack_window_close
        name: 창문 닫기
        icon: mdi:window-closed
      - type: button
        entity: button.multipack_window_open
        name: 창문 열기
        icon: mdi:window-open
      - type: button
        entity: button.multipack_trunk_open
        name: 트렁크 열기
        icon: mdi:car-back
      - type: button
        entity: button.multipack_trunk_close
        name: 트렁크 닫기
        icon: mdi:car-back

  - type: horizontal-stack
    cards:
      - type: button
        entity: button.multipack_panic
        name: 경적
        icon: mdi:car-horn
      - type: button
        entity: button.multipack_sunroof_close
        name: 썬루프 닫기
        icon: mdi:car-sunroof
      - type: button
        entity: button.multipack_sunroof_open
        name: 썬루프 열기
        icon: mdi:car-sunroof
      - type: button
        entity: button.multipack_sunroof_tilt
        name: 썬루프 틸트
        icon: mdi:car-sunroof
```