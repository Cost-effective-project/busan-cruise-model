# 제출용 대시보드 실행 안내

이 문서는 **`제출용 대시보드.py`**를 Windows의 PyCharm 터미널(PowerShell)에서 실행하는 방법을 정리한 것입니다.

> **주의:** `busan_ets_dashboard/app.py`와는 다른 대시보드입니다. 이 문서는 **`제출용 대시보드` 폴더**에 있는 파일을 실행할 때 사용합니다.

## 1. 프로젝트 폴더 구조

현재 작업 기준 경로는 `C:\work\cruise`입니다.

```text
C:\work\cruise\
├── .venv\
├── busan_ets_dashboard\
│   └── app.py                  # 기존 ETS 대시보드
├── data\
├── forecast\
└── 제출용 대시보드\
    ├── 제출용 대시보드.py       # 실행할 Streamlit 파일
    ├── engine.py              # 입항 데이터 처리·예측 관련 모듈
    ├── history.py             # 이력 관련 모듈
    ├── templates\
    │   └── raw_template.csv   # 원자료 CSV 헤더 양식
    └── README.md              # 이 문서
```

`engine.py`와 `history.py`는 `제출용 대시보드.py`에서 불러오므로 **세 Python 파일을 같은 폴더에 유지**해야 합니다. 다운로드 양식 파일은 코드가 찾는 **`templates/raw_template.csv`** 경로에 있어야 합니다. 앱의 다른 기능이 추가 파일을 요구할 수도 있습니다.

## 2. 실행 방법 (추천)

PyCharm에서 터미널을 열고 다음 두 줄을 순서대로 입력합니다.

### ① 제출용 대시보드 폴더로 이동

```powershell
cd "C:\work\cruise\제출용 대시보드"
```

### ② Streamlit 실행

이미 가상환경이 활성화되어 터미널 앞에 `(.venv)`가 보인다면:

```powershell
python -m streamlit run ".\제출용 대시보드.py" --server.port 8502
```

가상환경이 활성화되어 있는지 확실하지 않다면 아래와 같이 **가상환경 Python을 직접 지정**해도 됩니다.

```powershell
& "C:\work\cruise\.venv\Scripts\python.exe" -m streamlit run ".\제출용 대시보드.py" --server.port 8502
```

### ③ 브라우저에서 확인

```text
http://localhost:8502
```

정상 실행되면 Streamlit 터미널에도 `Local URL`이 표시됩니다. 브라우저가 자동으로 열리지 않으면 주소를 직접 입력합니다.

## 3. 기존 ETS 대시보드와 동시에 실행하기

기존 `busan_ets_dashboard/app.py`가 `8501` 포트에서 실행 중이어도, **새 PyCharm 터미널**을 열어 제출용 대시보드를 `8502` 포트로 실행할 수 있습니다.

| 구분 | 실행 파일 | 접속 주소 |
|---|---|---|
| 기존 ETS 대시보드 | `busan_ets_dashboard/app.py` | `http://localhost:8501` |
| 제출용 대시보드 | `제출용 대시보드/제출용 대시보드.py` | `http://localhost:8502` |

위 주소는 해당 포트로 실행한 경우에 해당합니다. `8502` 포트가 사용 중이라면 명령어의 `--server.port 8502`를 `--server.port 8503` 등으로 변경하고, 브라우저도 같은 포트로 접속합니다.

## 4. 종료 및 다시 실행

- **종료:** 실행 중인 PyCharm 터미널에서 `Ctrl + C`를 누릅니다.
- **다시 실행:** 위 **2번 실행 방법**을 반복합니다.
- **코드 수정 후:** Streamlit이 자동으로 다시 실행하거나 화면에 `Rerun`이 표시될 수 있습니다. 필요하면 브라우저를 새로고침합니다.

## 5. 자주 발생하는 오류

| 오류 | 확인할 내용 |
|---|---|
| `No module named 'engine'` | `engine.py`가 `제출용 대시보드.py`와 같은 폴더에 있는지 확인 |
| `No module named 'history'` | `history.py`가 같은 폴더에 있는지 확인 (`.venv`의 동명 파일은 프로젝트용 모듈이 아님) |
| `FileNotFoundError: ... templates\\raw_template.csv` | `제출용 대시보드/templates/raw_template.csv`가 있는지 확인. 최상위 `data` 폴더에만 두면 해결되지 않음 |
| `No module named 'streamlit'` | 올바른 가상환경 Python을 사용 중인지 확인. 해당 환경에 Streamlit이 설치되어 있어야 함 |
| 포트 사용 중 오류 | `--server.port 8503`처럼 사용하지 않는 포트로 변경 |
| `File does not exist` | `cd`로 이동한 폴더와 실행 파일명이 일치하는지 확인 |

**참고:** 이 문서는 대시보드의 **실행 경로와 터미널 명령어**를 안내합니다. ETS 예측 모형이나 분석 데이터의 계산 결과를 변경하는 내용은 포함하지 않습니다.
