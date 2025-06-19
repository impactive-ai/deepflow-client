# Deepflow API Client

Deepflow 고객사용 API 클라이언트 입니다.

## Features

- 고객사 데이터셋 스키마 열람
- 고객사 데이터셋 업데이트 (데이터 전송)

## 요구사항

- Python 3.8 이상
- git (모듈 설치시 필요)

## 설치방법

```shell
pip install git+https://github.com/impactive-ai/deepflow-client.git --upgrade
```

## 사용 방법

정상적으로 설치되면 `deepflow` 명령으로 작업을 수행할 수 있습니다.

```shell
deepflow
deepflow -h
deepflow --version
```

`-h` 스위치로 커맨드에 대한 도움말을 언제든지 열람하실 수 있습니다.


## Credential 설정하기

명령 수행시 고객에게 발급된 API키가 입력되어야 합니다.

방법1. 파라메터로 입력

```shell
deepflow --api-key {tenantId} \
  dataset-info
```

방법2. 환경변수로 등록하여 사용

- DEEPFLOW_API_KEY: API 키 입력


```shell
export DEEPFLOW_API_KEY={apiKey}

deepflow dataset-info
```

## Migration guide from 0.xx to version 1.0

**API 키 체계 변경**  
내부적으로 서버 및 인증체계를 통합하여 API Key 가 다시 발급되었습니다. 
또한 기존에 DEEPFLOW_TENANT_ID, DEEPFLOW_API_KEY 두 변수를 선언해야 했던 것을 DEEPFLOW_API_KEY 하나만 선언하여 사용하도록 하였습니다. 

**dataset-update 커맨드가 dataset-persist 커맨드로 변경되었습니다.**  
이 변경은 커맨드명의 변경을 넘어 처리 방식의 큰 개선을 가져왔습니다.
- 기존에 클라이언트에서 처리되던 전처리 작업들을 모두 제거하고 모든 작업을 서버에서 처리하도록 개선
- 기존에 현재 한번에 보낼 수 있는 행 수 제약이 없어짐
- 기존 대비 처리에 소요되는 시간이 최대 3배 정도 단축
- 처리 상황을 실시간으로 표시

```shell
deepflow dataset-persist item_event -i source_item_event.csv
```

**dataset-info 커맨드가 dataset 커맨드로 변경 되었습니다.**  
기존에는 dataset-info 에 일반정보와 함께 각 스키마의 상세정보가 모두 표시되었습니다만 
스키마를 여러개 가진 고객사는 표시되는 내용이 너무 많아 필요한 정보를 찾기가 불편하다는 피드백이 있었습니다.  
그래서 일반 목록 표시와 상세 정보 표시 동작을 구분하였습니다. 자세한 내용은 아래 가이드를 참조하세요.


## Guide

Deepflow에 고객사의 데이터셋을 전송(업데이트) 하는 방법을 안내합니다.

### 데이터셋 스키마 조회하기

`dataset` 명령을 이용해 현재 고객사에 등록된 데이터셋과 상세정보 조회가 가능합니다.

```shell
# 일반 정보 표시
deepflow dataset
# 특정 데이터셋의 상세정보 표시 (스키마, 파티션 정보)
deepflow dataset item_event
```

### 데이터 준비하기

데이터셋마다 각각의 파일로 스키마에 맞게 작성되어야 합니다.
 
**데이터 요구사항**

- CSV 포맷으로 작성되어야 합니다.
- 문자열 인코딩은 UTF-8 이어야 합니다.
- 내용의 첫 행은 컬럼명이어야 합니다.
- 날짜 데이터의 작성
  - 모든 날짜 데이터는 `yyyy-MM-dd` 형태(ISO Date format)여야 합니다.
  - 만약 `yyyy-MM` 형태의 월 단위 값이라면 해당월의 1일로 만들면 됩니다 (예: 2025-02 인 경우 2025-02-01)

### 데이터 전송하기

`dataset-persist` 명령을 이용하여 처리 가능합니다.  
데이터셋 item_event 에 대해 data.csv 파일이 준비되었다면 아래 명령으로 전송할 수 있습니다.

```shell
deepflow dataset-persist item_event -i data.csv
```

