# Multipack - Home Assistant 통합

🚗 Home Assistant에서 쉐비타운 멀티팩 커넥티드 차량을 원격으로 제어할 수 있습니다.

## 주요 기능

- 원격 엔진 시동/정지
- 도어 잠금/열기
- 창문, 트렁크 제어
- 경적(패닉) 작동
- 썬루프 제어
- 명령 실행 로그 (센서)

## 설치

### HACS (권장)

1. HACS > Integrations > Explore & Add Repositories
2. `https://github.com/the-xero/ha-chevytown-multipack` 추가
3. **Multipack** 설치 > HA 재시작

### 수동 설치

1. `custom_components/multipack/`을 `config/custom_components/`에 복사
2. Home Assistant 재시작

## 설정

**설정 > 기기 및 서비스 > 통합 추가 > Multipack**

다음 정보를 입력하세요:
- **사용자 ID**: Multipack 계정 ID
- **API Key**: Multipack API 키

> ⚠️ **주의**
> 설정 후 처음 연동 시, API 인증 검증을 위해 자동으로 **도어 잠금 명령이 1회 실행됩니다**. 
> 이 구성 요소는 단순 명령을 전송하는 기능만 수행합니다. 명령 전송의 성공여부는 전용 앱에서 확인하셔야 합니다.

## 사용 예시

### Lovelace UI

```yaml
type: button
entity: button.multipack_vehicle_start
name: 원격 시동
icon: mdi:car-start
```

### 자동화

```yaml
automation:
  - alias: "차량 준비"
    trigger:
      platform: time
      at: "07:30:00"
    action:
      service: button.press
      target:
        entity_id: button.multipack_vehicle_start
```

## 문제 해결

- 로그 확인: **설정 > 시스템 > 로그**
- 재시작 후에도 작동 안 함: `custom_components/multipack/` 폴더 확인
- API 인증 오류: ID/KEY 재확인
- 설정 시 도어가 잠겼다면 API 검증이 정상 작동한 것입니다

## 라이선스

MIT © @the-xero