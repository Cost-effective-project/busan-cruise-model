# 부산항 크루즈 입항 예측 프로젝트

부산항의 월별 크루즈 입항 기록을 바탕으로 **SARIMAX와 ETS 시계열 모형의 예측 성능을 비교**하고, 2027년 입항건수를 전망하는 프로젝트입니다. 분석 결과를 확인하는 정적 대시보드와 CSV 파일을 업로드해 예측을 새로 수행하는 갱신형 대시보드를 제공합니다.

## 대시보드 바로가기

| 구분 | 주요 기능 | 주소 |
|---|---|---|
| **BUSAN CRUISE INSIGHT** | 미리 계산한 예측·검증 결과를 시각화 (`dashboard_data.json` 기반) | [첫 번째 대시보드](https://busan-cruise-insight.streamlit.app/) |
| **월별 갱신형 ETS 대시보드** | 원본 CSV 및 선택적 예정 스케줄 CSV 업로드, ETS 예측 재계산 | [두 번째 대시보드](https://busan-cruise-ets.streamlit.app/) |

첫 번째 대시보드는 실행할 때 모델을 재학습하지 않습니다. 두 번째 대시보드는 업로드한 데이터로 예측을 새로 계산합니다.

## 저장소 구성

```text
busan-cruise-model/
├── README.md
├── busan_ets_dashboard/
│   ├── app.py
│   ├── dashboard_data.json
│   ├── images/
│   ├── styles/
│   ├── requirements.txt
│   └── README.md
├── data/
│   └── 크루즈입항.csv
├── forecast/
│   ├── forecast_enter.ipynb
│   ├── 입항수 예측 분석 리포트.md
│   ├── 승객수 예측 분석 리포트.md
│   ├── requirements.txt
│   └── README.md
└── submission_dashboard/
    ├── app.py
    ├── engine.py
    ├── history.py
    ├── templates/
    │   ├── raw_template.csv
    │   └── schedule_template.csv
    ├── requirements.txt
    └── README.md
```

각 폴더의 자세한 실행 및 분석 방법은 해당 폴더의 README를 참고하세요.

- [시계열 예측 분석 및 재현 방법](forecast/README.md)
- [BUSAN CRUISE INSIGHT 실행 안내](busan_ets_dashboard/README.md)
- [월별 갱신형 ETS 대시보드 실행 안내](submission_dashboard/README.md)

### 분석 리포트 바로가기

- [입항수 예측 분석 리포트](forecast/입항수%20예측%20분석%20리포트.md)
- [승객수 예측 분석 리포트](forecast/승객수%20예측%20분석%20리포트.md)

입항수와 승객 수 분석은 서로 구분되는 자료입니다. `forecast/forecast_enter.ipynb`는 **입항건수 예측 분석용 노트북**이며, 승객 수 예측의 분석 과정은 별도 **승객수 예측 분석 리포트**를 참고하세요.

## 분석 개요

- **분석 대상:** 부산항 월별 크루즈 입항건수
- **관측 기간:** 2013년 1월 ~ 2026년 9월
- **학습 기간:** 2013년 1월 ~ 2025년 12월
- **검증 기간:** 2026년 1월 ~ 9월 (9개월)
- **비교 모형:** SARIMAX, ETS
- **최종 활용 모형:** ETS(A,N,A) — 검증기간에서 상대적으로 낮은 예측오차를 보인 모형
- **2027년 입항건수 전망:** 분석 노트북 기준 약 **419.21건** (`statsmodels 0.15.0`), 첫 번째 대시보드 저장 결과 기준 약 **419.19건** (`statsmodels 0.14.6`)

두 환경의 예측 수치는 혼합하지 않습니다. 또한 ETS 모형의 잔차 자기상관 검정과 검증오차 등 한계가 있으므로 예측치를 확정 실적으로 해석하지 않습니다. 자세한 비교 지표와 분석상 유의사항은 [forecast README](forecast/README.md)에 기재했습니다.

## 데이터 출처 및 예정 스케줄

### 과거 크루즈 입항 실적

- **원자료 출처:** 해양수산부 **PORT-MIS(해운항만물류정보시스템)**, **선박입출항현황** 조회 화면
- **공식 조회 페이지:** [PORT-MIS 선박입출항현황](https://new.portmis.go.kr/portmis/websquare/websquare.jsp?w2xPath=/portmis/w2/main/index.xml&page=/portmis/w2/sp/vssl/vsch/UI-PM-SP-104-02.xml&menuId=1319&menuCd=M0182&menuNm=%EC%84%A0%EB%B0%95%EC%9E%85%EC%B6%9C%ED%95%AD%ED%98%84%ED%99%A9)
- **프로젝트 데이터:** `data/크루즈입항.csv` (분석에 사용한 원자료)
- **분석 기준:** 2013년 1월~2026년 9월 입항 실적을 전처리·월별 집계

**자료 공개에 관한 주의:** PORT-MIS에서 자료를 조회·다운로드할 수 있다는 사실만으로 원본 CSV의 제3자 재배포가 허용된다고 단정할 수는 없습니다. 이 저장소에는 현재 분석용 CSV가 포함되어 있으므로, 원자료 이용약관 또는 담당 기관의 재배포 조건을 별도로 확인해야 합니다. 재배포가 허용되지 않는 경우 해당 파일을 공개 저장소에서 제외하고 공식 조회 페이지를 통한 취득 방법을 안내해야 합니다.

### 2027년 크루즈 입항 예정 스케줄

- **출처:** [부산항만공사 체인포털 — 크루즈 스케줄](https://www.chainportal.co.kr/main/ko/cruise-schedule)
- **분석 당시 예정 건수:** **441건** (본 프로젝트에서 채택한 비교 기준값)
- **이용 방법:** 공식 사이트에서 스케줄을 조회하고 제공되는 엑셀 자료를 내려받아, `submission_dashboard/templates/schedule_template.csv` 형식에 맞게 CSV로 준비한 뒤 **월별 갱신형 ETS 대시보드**에 직접 업로드합니다.
- **공개 범위:** 실제 2027년 예정 스케줄 원본 CSV는 재배포 허용 여부가 확인되지 않아 저장소에 포함하지 않습니다. `schedule_template.csv`는 입력 양식이며 실제 스케줄 데이터가 아닙니다.

체인포털의 예정 스케줄은 조회 시점에 따라 달라집니다. 따라서 **441건은 분석 당시 조회한 값이지 현재 조회값이나 확정 입항 실적이 아닙니다.** 당시 조회 날짜와 원본 스냅샷은 별도로 확보하지 않았으므로 임의로 특정 날짜를 부여하지 않습니다.

2027년 입항건수의 ETS 분석 노트북 예측값은 약 **419.21건**이며, 441건 대비 약 **21.79건 낮습니다**. 이는 **전망과 계획의 차이**이지, 실제 관측값을 기준으로 한 예측오차가 아닙니다.

## 실행 환경 안내

- 대시보드별 Python 라이브러리는 각 폴더의 `requirements.txt`를 사용합니다.
- 분석 노트북은 `forecast/requirements.txt`를 사용하고, 현재 코드의 `../data/크루즈입항.csv` 상대경로에 맞게 **노트북 작업 디렉터리를 `forecast/`로 설정**합니다.
- 로컬 가상환경(`.venv/`), IDE 설정(`.idea/`), SSH 개인 키 등은 저장소에 업로드하지 않습니다.

> **참고:** 이 저장소의 예측 결과는 프로젝트의 분석 기준 시점과 사용 환경에 따라 산출되었습니다. 실제 입항 실적 및 최신 예정 스케줄을 반영하려면 자료 갱신과 재검증이 필요합니다.
