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

현재 제공되는 기능은 다음과 같습니다

- dataset-info: 등록된 데이터셋에 대한 정보와 스키마를 조회할 수 있습니다.
- dataset-update: Deepflow의 데이터셋을 업데이트 합니다 (데이터셋 전송)

## Credential 설정하기

명령 수행시 고객에게 발급된 API키와 Tenant ID 가 입력되어야 합니다.

방법1. 파라메터로 입력

```shell
deepflow --tenant-id {apiKey} \
  --api-key {tenantId} \
  dataset-info
```

방법2. 환경변수로 등록하여 사용

- DEEPFLOW_API_KEY: API 키 입력
- DEEPFLOW_TENANT_ID: Tenant ID 입력

```shell
export DEEPFLOW_API_KEY={apiKey}
export DEEPFLOW_TENANT_ID={tenantId}

deepflow dataset-info
```


## 사용방법: 데이터셋 전송하기

Deepflow에 고객사의 데이터셋을 전송(업데이트) 하는 방법을 안내합니다.

### 데이터셋 스키마 조회하기

`dataset-info` 명령을 이용해 현재 고객사에 등록된 스키마 정보를 조회할 수 있습니다.

```shell
deepflow dataset-info
```

### 데이터 준비하기

데이터셋마다 각각의 파일로 스키마에 맞게 작성되어야 합니다. 컬럼명으로 데이터를 인식하므로 컬럼 순서는 맞추지 않아도 됩니다.
 
**데이터 요구사항**

- CSV 포맷으로 작성되어야 합니다.
- 문자열 인코딩은 UTF-8 이어야 합니다.
- 내용의 첫 행은 컬럼명이어야 합니다.
- 날짜 데이터의 작성
  - 모든 날짜 데이터는 `yyyy-MM-dd` 형태(ISO Date format)여야 합니다.
  - 만약 `yyyy-MM` 형태의 월 단위 값이라면 해당월의 1일로 만들면 됩니다 (예: 2025-02 인 경우 2025-02-01)
- 현재 한번에 보낼 수 있는 행 수는 10,000 건으로 제한되어 있습니다. 만약 다량의 데이터를 업데이트 해야 하는 경우 10,000건 단위로 끊어서 전송하여야 합니다.

### 데이터 전송하기

`dataset-update` 명령을 이용하여 처리 가능합니다.  
데이터셋 item_event 에 대해 data.csv 파일이 준비되었다면 아래 명령으로 전송할 수 있습니다.

```shell
deepflow dataset-update --dataset item_event --input data.csv
```

명령을 수행시 다음과 같은 프로세스로 동작합니다.

- 요청 내용 검증
- 데이터 전송용 Signed URL 발급
- Signed URL 에 데이터 전송 처리
- 데이터 검증 수행
- 데이터 마이그레이션 수행

데이터 검증 중 에러가 발생하면 마이그레이션이 수행되지 않고 전체 실패 처리 되며 데이터 검증 결과가 자세히 나타납니다.
