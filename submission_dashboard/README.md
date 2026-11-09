# 부산항 크루즈 월별 갱신형 ETS 대시보드 — 실행 안내

이 문서는 **`submission_dashboard/app.py`**를 로컬 PyCharm 환경에서 실행하고, GitHub Organization 레포지터리 및 Streamlit Community Cloud의 배포 위치를 확인하는 방법을 설명합니다.

> **구분:** 이 앱은 `busan_ets_dashboard/app.py`(저장된 JSON 결과를 보여주는 **BUSAN CRUISE INSIGHT**)와 다른 대시보드입니다. 이 앱은 사용자가 CSV를 업로드하면 입항수·승객수 ETS 전망을 새로 계산합니다.

## 1. 최종 프로젝트 구조

GitHub 레포지터리: <https://github.com/Cost-effective-project/busan-cruise-model>

```text
busan-cruise-model/
├── busan_ets_dashboard/
│   └── app.py                    # 첫 번째 Streamlit 대시보드
├── data/
│   └── 크루즈입항.csv              # 분석용 원본 자료; 본 앱은 자동 로드하지 않음
├── forecast/
│   └── forecast_enter.ipynb     # 별도 시계열 분석 노트북
└── submission_dashboard/
    ├── app.py                    # 이 문서의 실행 대상
    ├── engine.py                 # 입항·승객 데이터 처리 및 ETS 예측
    ├── history.py                # 예측 기록 JSON 생성·평가
    ├── requirements.txt          # 이 대시보드 전용 설치 패키지
    ├── templates/
    │   ├── raw_template.csv      # 원자료 CSV 헤더 양식
    │   └── schedule_template.csv # 예정 스케줄 CSV 헤더 양식
    └── README.md                 # 이 문서
```

- `app.py`, `engine.py`, `history.py`는 같은 `submission_dashboard/` 폴더에 둡니다.
- 다운로드용 CSV 양식 2개는 `submission_dashboard/templates/`에 보관합니다.
- `assets/workflow_demo.mp4` 및 `reference/baseline_2026-09_2027.json`은 코드에서 **존재할 때만** 사용하는 선택 파일입니다.
- `.venv/`는 개인 컴퓨터의 가상환경이므로 GitHub 업로드 대상에서 제외합니다. 이번 제출에서는 루트의 `pyproject.toml`, `uv.lock`도 제외하고 앱별 `requirements.txt`를 사용합니다.

## 2. PyCharm·PowerShell에서 로컬 실행

아래 명령어의 경로는 **GitHub 레포지터리를 `C:\work\busan-cruise-model-upload`에 내려받은 경우의 예시**입니다. 팀원의 컴퓨터에서는 실제 저장 위치에 맞게 첫 줄을 변경합니다.

### ① 프로젝트 최상위 폴더로 이동

```powershell
cd C:\work\busan-cruise-model-upload
```

### ② Python 가상환경 확인 및 패키지 설치

터미널 앞에 `(.venv)` 등이 표시되고 해당 가상환경에 필요한 패키지가 설치되어 있다면 다음을 실행합니다.

```powershell
python -m pip install -r .\submission_dashboard\requirements.txt
```

별도 가상환경을 직접 지정하려면, **본인 PC에 실제 존재하는 Python 경로**를 사용합니다. 이전 작업 PC의 가상환경을 사용하는 예시는 다음과 같습니다.

```powershell
& "C:\work\cruise\.venv\Scripts\python.exe" -m pip install -r .\submission_dashboard\requirements.txt
```

### ③ 제출용 대시보드 실행

가상환경이 활성화되어 있을 때:

```powershell
python -m streamlit run .\submission_dashboard\app.py --server.port 8502
```

가상환경 Python 실행 파일을 직접 지정할 때(경로는 본인 PC에 맞게 변경):

```powershell
& "C:\work\cruise\.venv\Scripts\python.exe" -m streamlit run .\submission_dashboard\app.py --server.port 8502
```

### ④ 브라우저에서 접속

<http://localhost:8502>

정상 실행되면 터미널에 `Local URL`이 표시됩니다. `8502` 포트를 다른 프로그램이 사용 중이라면 `--server.port 8503`처럼 변경합니다.

## 3. 첫 번째 대시보드와 동시에 실행

서로 다른 터미널에서 각기 다른 포트를 지정하면 동시에 실행할 수 있습니다. 다음 예시는 모두 **프로젝트 최상위 폴더**에서 실행합니다.

| 대시보드 | 로컬 실행 명령어 | 접속 주소 |
|---|---|---|
| BUSAN CRUISE INSIGHT | `python -m streamlit run .\busan_ets_dashboard\app.py --server.port 8501` | <http://localhost:8501> |
| 월별 갱신형 ETS (이 앱) | `python -m streamlit run .\submission_dashboard\app.py --server.port 8502` | <http://localhost:8502> |

`python`은 해당 앱의 필요 패키지가 설치된 환경이어야 합니다. 두 앱에 서로 다른 라이브러리 버전이 필요하면 가상환경을 분리하여 실행하는 편이 안전합니다.

## 4. Streamlit Community Cloud 배포

이미 사용 중인 배포 정보는 다음과 같습니다.

| 항목 | 설정 |
|---|---|
| Repository | `Cost-effective-project/busan-cruise-model` |
| Branch | `main` |
| Main file path | `submission_dashboard/app.py` |
| Requirements | `submission_dashboard/requirements.txt` |
| 배포 주소 | <https://busan-cruise-ets.streamlit.app/> |

2026-11-09 배포 로그에서 `requirements.txt` 패키지 설치와 Streamlit 서버 시작이 확인되었으며, 브라우저의 사이트 데이터를 삭제한 뒤 **접속이 정상적으로 되는 것도 확인**했습니다. 다만 실제 CSV 업로드부터 ETS 재학습 및 결과 다운로드까지의 전체 기능 테스트는 별도로 수행해야 합니다.

**첫 번째 앱 주소:** <https://busan-cruise-insight.streamlit.app/>

이 앱의 배포 로그에는 Python **3.14.10**, `statsmodels==0.14.6`이 사용된 것으로 나타났습니다. 별도 최종 예측 분석 노트북의 `statsmodels==0.15.0` 결과와 버전을 혼동하지 마세요. 배포 시 사용하는 세부 패키지 버전은 이 폴더의 `requirements.txt`를 기준으로 관리합니다.

## 5. 앱 사용 방법과 데이터 준비

1. 왼쪽 사이드바에서 **누적 입출항 원자료 CSV**를 업로드합니다. `data/크루즈입항.csv`가 GitHub에 존재하더라도 이 앱이 이를 자동으로 불러오지는 않습니다.
2. 필요한 경우 **선택 연도 예정 스케줄 CSV**를 추가 업로드합니다.
3. 원자료의 마지막 기록월과 **실제 수집이 완료된 월**을 구분하여 확인합니다.
4. 기록이 없는 월은 자동으로 실제 무입항이라고 단정하지 말고 확인합니다.
5. 예측 연도를 선택해 **ETS 재학습·예측 실행** 버튼을 누릅니다.
6. 예측 그래프, 월별 비교표, 근사 예측구간을 확인하고 필요한 CSV 및 예측 기록 JSON을 내려받습니다.

**원자료 필수 열:** `입출`, `입항일시`, `호출부호`, `선명`, `승객`  
**예정 스케줄 필수 열:** `입항예정일`, `선명`, `승객정원수`

헤더 양식은 대시보드 사이드바의 **CSV 헤더 양식**에서 내려받을 수 있습니다. 업로드 자료는 분석·예측 입력이며, 공개 클라우드 서버에 영구 보관되는 파일 저장소로 취급하지 않습니다. 예측 기록은 별도로 JSON을 내려받아 보관합니다.

## 6. 종료·재실행 및 오류 해결

- **로컬 앱 종료:** 앱을 실행한 터미널에서 `Ctrl + C`를 누릅니다.
- **로컬 재실행:** 2번의 실행 명령을 다시 입력합니다.
- **GitHub 코드 반영:** 수정 내용을 커밋·푸시한 뒤 Streamlit Cloud의 재배포 상태를 확인합니다.

| 증상 | 확인할 내용 |
|---|---|
| `File does not exist: app.py` | 현재 작업 폴더와 `submission_dashboard/app.py` 경로 확인 |
| `No module named 'engine'` 또는 `'history'` | `engine.py`, `history.py`가 `submission_dashboard/app.py`와 같은 폴더에 있는지 확인 |
| `templates/raw_template.csv` 또는 `templates/schedule_template.csv` 관련 오류 | `submission_dashboard/templates/` 안의 두 CSV 확인 |
| `No module named 'streamlit'` | 올바른 가상환경과 `submission_dashboard/requirements.txt` 설치 여부 확인 |
| 의존성 설치 중 `Invalid requirement` | 배포 실행 파일 경로와 `requirements.txt` 위치 및 파일명 확인. 과거의 공백 있는 폴더명 대신 `submission_dashboard` 사용 |
| 로컬 포트 충돌 | `--server.port 8503`처럼 사용하지 않는 포트 지정 |
| 클라우드 서버는 실행됐지만 화면이 계속 로딩됨 | 시크릿 창에서 확인 후 사이트 데이터/캐시 점검, 최신 배포 로그 확인 |
| 새 CSV로 예측을 실행할 수 없음 | 필수 열, 실제 완료월, 무입항 확인 항목, 예측 오류 메시지 확인 |

**참고:** 이 README는 실행 및 배포 안내용입니다. 폴더명 및 파일명 변경은 ETS 모형의 계산 방식이나 기존 분석 결과를 변경하지 않습니다.
