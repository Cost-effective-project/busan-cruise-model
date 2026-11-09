# BUSAN CRUISE INSIGHT — 부산항 크루즈 예측 대시보드

## 현재 프로젝트 구조

현재 PyCharm 프로젝트 루트는 **`C:\work\cruise`**이며, 실제 Streamlit 앱은 그 아래 **`busan_ets_dashboard`** 폴더에 있습니다.

```text
C:\work\cruise\
├── .venv/                      # 프로젝트 가상환경
├── busan_ets_dashboard/       # 실제 Streamlit 대시보드
│   ├── images/                # 대시보드 이미지 파일
│   ├── styles/                # 대시보드 스타일 파일
│   ├── app.py                 # 실행할 Streamlit 앱
│   ├── dashboard_data.json    # 저장된 예측·검증 결과
│   ├── README.md              # 이 문서
│   └── requirements.txt       # 대시보드 실행용 라이브러리
├── data/                       # 프로젝트 데이터 폴더
├── forecast/                   # 분석 관련 폴더
├── pyproject.toml
├── uv.lock
└── 제출용 대시보드.py         # 프로젝트 루트의 별도 Python 파일
```

> **중요:** 이 README의 실행 대상은 `C:\work\cruise\busan_ets_dashboard\app.py`입니다. 프로젝트 루트의 `제출용 대시보드.py`와 구분해 주세요.
>
> `images/`와 `styles/` 내부 파일명은 현재 폴더 화면만으로 확인되지 않았으므로 위 구조에는 폴더까지만 표시했습니다.

## PyCharm에서 실행 (권장: 대시보드 폴더에서 실행)

PyCharm 터미널이 `(.venv) PS C:\work\cruise>`로 시작하고 가상환경이 활성화되어 있다면, 다음 순서로 실행합니다.

**1. 실제 앱 폴더로 이동**

```powershell
cd .\busan_ets_dashboard
```

터미널 경로가 `C:\work\cruise\busan_ets_dashboard`인지 확인합니다.

**2. 필요한 라이브러리 설치 (최초 실행 또는 환경 변경 시)**

```powershell
python -m pip install -r requirements.txt
```

**3. Streamlit 앱 실행**

```powershell
python -m streamlit run app.py
```

정상적으로 실행되면 터미널에 표시되는 `Local URL`(일반적으로 `http://localhost:8501`)로 접속합니다.

### 프로젝트 루트에서 이동하지 않고 실행하는 방법

터미널 위치가 **`C:\work\cruise`**일 때만 다음과 같이 하위 폴더의 경로를 지정할 수 있습니다.

```powershell
python -m pip install -r .\busan_ets_dashboard\requirements.txt
python -m streamlit run .\busan_ets_dashboard\app.py
```

앱 내부에서 이미지나 스타일 파일을 현재 작업 폴더 기준 상대 경로로 읽는 경우에는 경로 문제가 생길 수 있으므로, **위의 권장 방법처럼 `busan_ets_dashboard` 폴더로 이동한 뒤 실행**하는 것이 안전합니다.

### 자주 발생하는 경로 오류

- `File does not exist: app.py`: 현재 폴더에 `app.py`가 없는 상태에서 `python -m streamlit run app.py`를 실행했을 때 발생합니다.
- 프로젝트 루트 `C:\work\cruise`에서는 `app.py`가 바로 아래에 있지 않으므로 `python -m streamlit run .\busan_ets_dashboard\app.py`처럼 **하위 폴더를 명시**해야 합니다.
- 이미 `busan_ets_dashboard` 안으로 이동했다면 `python -m streamlit run .\busan_ets_dashboard\app.py`가 아니라 **`python -m streamlit run app.py`**를 실행합니다. 그렇지 않으면 폴더명이 중복됩니다.
- 현재 위치와 파일 존재 여부를 확인하려면 아래 명령을 사용합니다.

  ```powershell
  Get-Location
  Test-Path .\app.py
  Test-Path .\busan_ets_dashboard\app.py
  ```

  `Test-Path`는 경로가 존재하면 `True`, 없으면 `False`를 반환합니다. 현재 위치에 따라 둘 중 하나가 `True`가 되는 것이 정상입니다.

## 이미지 및 스타일 관리

- **사이드바 선박 그림**: `busan_ets_dashboard/images/sidebar_ship.png` (기존 README 기준 필수). 기존 `app.py`에서 추출한 원본 PNG 바이트 그대로이며, 외관과 크기는 변경하지 않았습니다.
- **상단 배너 그림**: `busan_ets_dashboard/images/header_banner.png` (기존 README 기준 선택). 배너 이미지 원본이 제공되지 않았던 당시에는 포함하지 않았습니다. 해당 이름으로 파일을 추가하면 기존 앱 코드의 동작에 따라 사용할 수 있습니다.
- **대체 배너 그림**: `busan_ets_dashboard/images/header_banner_fallback.png` (기존 README 기준 선택). `header_banner.png`가 없을 때 사용하는 지원 경로입니다.
- **스타일 폴더**: 현재 프로젝트에 `busan_ets_dashboard/styles/`가 있습니다. 실제 파일명과 로딩 방식은 `app.py`에서 확인하세요.
- 배너 파일이 없을 때 기존 코드가 제공하는 그라데이션 배경을 사용하도록 구성되어 있습니다.

## 데이터 및 버전 기준

이 앱은 예측을 재학습하지 않습니다. `busan_ets_dashboard/dashboard_data.json`에 저장된 예측 결과를 시각화합니다. **기존 README에 기재된 대시보드 수치는 `statsmodels 0.14.6` 환경에서 산출된 결과를 유지**합니다.

- 입항건수 ETS(A,N,A) 2027년 다이렉트 예측: **419.19건**
- 승객 수 ETS(A,Ad,A) 2027년 예측: **1,247,850.14명**
- JSON의 모델 설정, 성능 지표, 월별 결과, 예측구간, 문구는 이번 **README 경로 수정 작업에서 변경하지 않았습니다.**
- 별도 분석(원본 CSV, IPYNB, ETS 학습 스크립트)을 재실행하려면 그에 맞는 의존성이 추가로 필요합니다. **기존 README 기준 이 대시보드 실행에는 `statsmodels`가 필요하지 않습니다.**
- 별도 최종 예측 분석 노트북의 `statsmodels 0.15.0` 기준 결과와, 이 대시보드 JSON의 `0.14.6` 기준 결과를 혼합하지 않습니다.

## 변경 범위 및 주의 사항

이번 수정은 **프로젝트 폴더 구조에 따른 README 안내 수정만 수행**했습니다. `app.py`, `dashboard_data.json`, `requirements.txt`, 이미지, 스타일, 원본 데이터, 예측 모형은 수정하지 않았습니다.

기존 README에 기록되어 있던 앱 정리 이력은 다음과 같습니다.

- 기존 `app.py`에 포함되어 있던 약 36KB의 Base64 선박 PNG를 `images/sidebar_ship.png`로 분리했습니다.
- 선박 이미지를 PNG 파일에서 다시 Base64로 읽도록 경로만 변경했습니다. HTML 이미지 출력 형식과 CSS는 그대로입니다.
- 선택적 배너 경로를 `images/`로 통일했습니다. 배너가 없는 경우 기존 그라데이션 표시를 유지합니다.
- 기존 정리 작업에서는 `requirements.txt`의 버전 범위와 앱의 문구 수정사항을 보존했습니다.

이미지 경로 또는 파일명을 변경한 후에는 Streamlit 앱을 재실행하세요.
