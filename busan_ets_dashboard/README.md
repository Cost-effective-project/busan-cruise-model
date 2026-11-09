# BUSAN CRUISE INSIGHT — 부산항 크루즈 예측 대시보드

부산항 크루즈 입항건수와 승객 수의 예측 결과를 시각화하는 **Streamlit 대시보드**입니다.

이 앱은 이미 계산하여 `dashboard_data.json`에 저장한 결과를 보여주는 **고정형 대시보드**입니다. 앱을 열거나 새로고침할 때 ETS 모형을 다시 학습하지 않습니다.

- **배포된 대시보드:** https://busan-cruise-insight.streamlit.app/
- **GitHub 저장소:** https://github.com/Cost-effective-project/busan-cruise-model
- **Streamlit Cloud 실행 파일:** `busan_ets_dashboard/app.py` (`main` 브랜치)
- **별도 월별 갱신형 대시보드:** https://busan-cruise-ets.streamlit.app/ (`submission_dashboard/app.py`)

## 1. 프로젝트 구조

GitHub에 업로드한 저장소를 기준으로 한 주요 구조입니다.

```text
busan-cruise-model/
├── busan_ets_dashboard/
│   ├── app.py                  # 이 README의 실행 대상
│   ├── dashboard_data.json     # 저장된 예측·검증 결과
│   ├── requirements.txt        # 이 앱 실행에 필요한 라이브러리
│   ├── README.md
│   ├── images/
│   │   └── sidebar_ship.png    # 사이드바 선박 이미지
│   └── styles/
│       └── styles.css          # 대시보드 스타일
├── data/
│   └── 크루즈입항.csv
├── forecast/                   # 별도 예측 분석 자료
└── submission_dashboard/       # 별도 월별 갱신형 대시보드
    ├── app.py
    ├── engine.py
    ├── history.py
    ├── requirements.txt
    ├── README.md
    └── templates/
        ├── raw_template.csv
        └── schedule_template.csv
```

> **주의:** 이전 로컬 작업 폴더 `C:\work\cruise`와 GitHub 업로드용 폴더 `C:\work\busan-cruise-model-upload`는 서로 다른 폴더입니다. 이 README는 **GitHub 업로드용 저장소**를 기준으로 작성했습니다. `.venv/`, `pyproject.toml`, `uv.lock`은 위 GitHub 배포 구조에 포함하지 않습니다.

## 2. Windows / PyCharm에서 로컬 실행

PyCharm에서 GitHub 업로드용 프로젝트(`C:\work\busan-cruise-model-upload`)를 열고, 필요한 라이브러리가 설치될 Python 환경을 선택합니다.

### 방법 A: 대시보드 폴더에서 실행 (권장)

PowerShell 터미널에 다음 명령어를 순서대로 입력합니다.

```powershell
cd C:\work\busan-cruise-model-upload\busan_ets_dashboard
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.port 8501
```

브라우저에서 **http://localhost:8501** 로 접속합니다. `python`은 선택한 가상환경의 Python이어야 합니다.

다른 위치에 저장소를 복제했다면 첫 번째 명령어의 경로를 실제 위치로 바꾸면 됩니다.

### 방법 B: 저장소 루트에서 실행

```powershell
cd C:\work\busan-cruise-model-upload
python -m pip install -r .\busan_ets_dashboard\requirements.txt
python -m streamlit run .\busan_ets_dashboard\app.py --server.port 8501
```

이미지·스타일 등 부속 파일은 `busan_ets_dashboard/` 아래의 원래 위치를 유지해야 합니다.

## 3. 월별 갱신형 대시보드와 함께 실행

이 대시보드는 `8501` 포트, 별도 월별 갱신형 대시보드는 `8502` 포트를 사용하면 동시에 실행할 수 있습니다.

**첫 번째 터미널 (고정형 대시보드):**

```powershell
cd C:\work\busan-cruise-model-upload\busan_ets_dashboard
python -m streamlit run app.py --server.port 8501
```

**두 번째 터미널 (월별 갱신형 대시보드):**

```powershell
cd C:\work\busan-cruise-model-upload\submission_dashboard
python -m streamlit run app.py --server.port 8502
```

두 번째 앱의 라이브러리가 설치되지 않았다면 해당 폴더의 `requirements.txt`를 먼저 설치해야 합니다. 자세한 내용은 `submission_dashboard/README.md`를 참고하세요.

## 4. 데이터 및 예측 결과 기준

이 앱의 표시값은 `busan_ets_dashboard/dashboard_data.json`을 기준으로 합니다.

| 항목 | JSON에 저장된 2027년 예측값 |
| --- | ---: |
| 크루즈 입항건수 — ETS(A,N,A) | 약 **419.19건** |
| 크루즈 승객 수 — ETS(A,Ad,A) | 약 **1,247,850.14명** |

- 위 수치는 **예측값**이지 확정 실적이 아닙니다.
- 기존 대시보드 JSON은 `statsmodels 0.14.6` 환경에서 산출된 결과를 유지합니다.
- 별도 최종 분석 노트북의 `statsmodels 0.15.0` 기반 결과와 수치를 혼용하지 않습니다.
- 이 대시보드의 실행 자체에는 ETS 재학습이 필요하지 않으므로, 별도 분석용 라이브러리인 `statsmodels`를 이 앱의 실행 의존성에 임의로 추가할 필요는 없습니다.
- 데이터를 새로 계산하여 보여주려면 별도 분석 과정을 거쳐 `dashboard_data.json`을 갱신해야 합니다. **앱 새로고침만으로 예측 결과가 갱신되지는 않습니다.**

## 5. 배포 및 코드 업데이트

Streamlit Community Cloud에서 다음 설정으로 배포한 앱입니다.

| 항목 | 설정 |
| --- | --- |
| 저장소 | `Cost-effective-project/busan-cruise-model` |
| 브랜치 | `main` |
| Main file path | `busan_ets_dashboard/app.py` |
| 앱 URL | https://busan-cruise-insight.streamlit.app/ |

GitHub에 반영된 코드·데이터 변경 사항은 Streamlit Cloud 앱 업데이트에 사용됩니다. **README만 수정하는 경우 예측 모형이나 저장된 JSON 결과는 바뀌지 않습니다.**

## 6. 자주 발생하는 문제

| 증상 | 확인할 사항 |
| --- | --- |
| `File does not exist: app.py` | 현재 폴더가 `busan_ets_dashboard`인지 확인합니다. 저장소 루트에서는 `busan_ets_dashboard/app.py`로 실행합니다. |
| `No module named 'streamlit'` | 활성화한 Python 환경에 `requirements.txt`의 라이브러리를 설치했는지 확인합니다. |
| 이미지 또는 CSS가 표시되지 않음 | `images/sidebar_ship.png`, `styles/styles.css`가 폴더 안에 유지되어 있는지 확인합니다. |
| `Port 8501 is already in use` | 기존 실행을 종료하거나 다른 포트(`--server.port 8503` 등)로 실행합니다. |
| 클라우드 앱이 계속 흰색 로딩 화면을 보임 | 강력 새로고침 또는 시크릿 창에서 확인하고, 필요하면 해당 사이트 데이터 삭제 후 다시 접속합니다. 배포 로그도 함께 확인합니다. |
| 예측값이 자동으로 바뀌지 않음 | 정상입니다. 이 앱은 `dashboard_data.json`에 저장된 결과를 표시합니다. |

실행 종료는 해당 터미널에서 **Ctrl + C**를 누르면 됩니다.

---

이 README는 **실행 경로와 배포 안내를 최신화한 문서**입니다. 이 문서의 변경 자체는 `app.py`, `dashboard_data.json`, 이미지, CSS, 라이브러리 버전 또는 예측 결과를 변경하지 않습니다.
