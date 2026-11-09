"""부산항 크루즈 예측 대시보드 (저장된 JSON 예측 결과 표시)."""

from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from html import escape
from typing import Any

import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dashboard_data.json"
IMAGE_DIR = BASE_DIR / "images"
STYLE_FILE = BASE_DIR / "styles" / "styles.css"

# 선박 이미지는 images/sidebar_ship.png에서 읽어 HTML에 표시합니다.
SIDEBAR_SHIP_ICON_BASE64 = base64.b64encode(
    (IMAGE_DIR / "sidebar_ship.png").read_bytes()
).decode("ascii")

st.set_page_config(
    page_title="BUSAN CRUISE INSIGHT | 부산항 크루즈 예측",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 화면 디자인은 styles/styles.css에서 관리합니다.
st.markdown(
    "\n<style>\n" + STYLE_FILE.read_text(encoding="utf-8") + "</style>\n",
    unsafe_allow_html=True,
)


def read_data() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {}
    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except (OSError, ValueError):
        st.warning("데이터 설정 파일을 읽을 수 없습니다. 빈 대시보드로 표시합니다.")
        return {}


def present(value: Any, suffix: str = "") -> str:
    if value is None or value == "":
        return '<span class="dash">—</span>'
    if isinstance(value, bool):
        return '<span class="dash">—</span>'
    if isinstance(value, (int, float)):
        formatted = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
    else:
        formatted = str(value)
    return f"{escape(formatted)}{escape(suffix)}"


def card(
    label: str,
    value: Any = None,
    suffix: str = "",
    card_type: str = "info",
    detail: str | None = None,
) -> None:
    klass = "kpi-card" if card_type == "kpi" else "info-card"
    description_html = (
        f'<div class="card-detail">{escape(detail)}</div>' if detail else ""
    )
    st.markdown(
        f'<div class="{klass}"><div class="card-label">{escape(label)}</div>'
        f'<div class="card-value">{present(value, suffix)}</div>'
        f'{description_html}</div>',
        unsafe_allow_html=True,
    )


def info_cards(model: dict[str, Any]) -> None:
    # All model-specific text and periods are maintained in dashboard_data.json.
    cols = st.columns(3, gap="small")
    with cols[0]:
        card(
            "⚙️ 모델 형태",
            model.get("model_type"),
            detail=model.get("model_explanation"),
        )
    with cols[1]:
        card("🗄️ 학습 기간", model.get("training_period"))
    with cols[2]:
        card("📊 예측 기간", model.get("forecast_period"))


def metric_table(
    metrics: dict[str, Any], *, is_arrival: bool, validation_note: str = ""
) -> None:
    # English abbreviations on the first line, Korean meanings and units below.
    unit = "건" if is_arrival else "명"
    labels = [
        ("MAE", f"(평균절대오차, {unit})"),
        ("RMSE", f"(평균 제곱근 오차, {unit})"),
        ("MAPE", "(평균 절대 백분율 오차, %)"),
        ("WAPE", "(가중 절대 백분율 오차, %)"),
    ]
    headers = "".join(
        f'<th><span class="metric-en">{abbr}</span>'
        f'<span class="metric-ko">{meaning}</span></th>'
        for abbr, meaning in labels
    )
    cells = "".join(
        f'<td>{present(metrics.get(abbr.lower()))}</td>'
        for abbr, _ in labels
    )
    st.markdown(
        '<table class="performance"><thead><tr>'
        '<th>구분</th>' + headers +
        '</tr></thead><tbody><tr><td>ETS (선정)</td>' + cells +
        '</tr></tbody></table>',
        unsafe_allow_html=True,
    )
    if validation_note:
        st.markdown(
            f'<div class="note">{escape(validation_note)}</div>',
            unsafe_allow_html=True,
        )


def note_card(title: str, lines: list[str] | None, *, results: bool = False) -> None:
    safe_lines = lines if isinstance(lines, list) else []
    out = []
    for value in safe_lines:
        if not value or value == "—":
            continue
        safe_value = escape(str(value))
        # Bold formatting is supported for these fixed interpretation messages.
        safe_value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe_value)
        out.append(f'<div class="{"item" if results else "reason-item"}">🔵 &nbsp;{safe_value}</div>')
    if results:
        st.markdown('<div class="results-card"><div class="title">' + escape(title) + '</div>' + "".join(out) + '</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="reason-card"><div class="reason-title">📌 ' + escape(title) + '</div>' + "".join(out) + '</div>', unsafe_allow_html=True)


def model_page(topic: str, data: dict[str, Any]) -> None:
    is_arrival = topic == "입항건수 예측"
    model = data.get("model", {})
    validation = data.get("validation", {})
    model_type = model.get("model_type", "")
    desc = model.get("model_description", "")
    st.markdown(
        f'<div class="explainer"><div class="explainer-title">🔷 &nbsp;예측 모델: {escape(str(model_type))}</div>'
        f'<div class="explainer-desc">{escape(str(desc))}</div></div>',
        unsafe_allow_html=True,
    )
    info_cards(model)
    validation_period = validation.get("period", "")
    validation_basis = validation.get("basis", "")
    st.markdown(
        '<div class="validation-header">'
        '<div class="panel-header">모델 성능 검증</div>'
        f'<span class="validation-period">({escape(str(validation_period))} 검증, 데이터 내 {escape(str(validation_basis))} 기준)</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([2.2, 1], gap="medium")
    with left:
        metric_table(
            data.get("metrics", {}),
            is_arrival=is_arrival,
            validation_note=validation.get("note", ""),
        )
    with right:
        note_card("해석", data.get("interpretation", []))


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def forecast_chart(monthly: list[dict[str, Any]] | None, y_label: str) -> None:
    months = [f"{i}월" for i in range(1, 13)]
    monthly = monthly if isinstance(monthly, list) else []
    lookup = {int(d.get("month", -1)): d for d in monthly if isinstance(d, dict) and str(d.get("month", "")).isdigit()}

    def vals(key: str) -> list[float | None]:
        return [lookup.get(i, {}).get(key) if is_number(lookup.get(i, {}).get(key)) else None for i in range(1, 13)]

    scheduled = vals("scheduled")
    predicted = vals("forecast")
    low = vals("lower")
    high = vals("upper")
    has_any = any(is_number(v) for row in [scheduled, predicted, low, high] for v in row)

    fig = go.Figure()
    if any(v is not None for v in scheduled):
        fig.add_bar(x=months, y=scheduled, marker_color="#a5caff", name="입항 예정" if "입항" in y_label else "승객 예정")
    if any(v is not None for v in low) and any(v is not None for v in high):
        fig.add_trace(go.Scatter(x=months,y=low,mode="lines",line=dict(color="#ec8597",dash="dash",width=1.5),showlegend=False,hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=months,y=high,mode="lines",line=dict(color="#ec8597",dash="dash",width=1.5),fill="tonexty",fillcolor="rgba(235,99,123,0.14)",name="95% 근사 예측구간"))
    if any(v is not None for v in predicted):
        fig.add_trace(go.Scatter(x=months,y=predicted,mode="lines+markers",line=dict(color="#1267db",width=3),marker=dict(size=7,color="white",line=dict(color="#1267db",width=2)),name="ETS 예측"))
    if not has_any:
        # Plotly needs a category anchor to draw 1~12월 labels even with no observations.
        fig.add_trace(go.Scatter(x=months, y=[None] * 12, mode="markers", showlegend=False, hoverinfo="skip"))
        fig.add_annotation(x="6월",y=0.5,xref="x",yref="paper",text="데이터 미입력 · 월별 차트 영역",showarrow=False,font=dict(size=16,color="#8da4c3"))
    fig.update_layout(
        height=330, margin=dict(l=5,r=5,t=12,b=20),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#ffffff",
        bargap=.38,font=dict(family="Malgun Gothic, sans-serif",color="#284468"),
        showlegend=False,  # 상단 HTML 범례만 표시하여 Plotly 범례 중복 제거
        xaxis=dict(type="category",categoryorder="array",categoryarray=months,tickfont=dict(size=11),showline=True,linecolor="#c9d9f0",gridcolor="#ebf0fa"),
        yaxis=dict(title=y_label if has_any else "",showticklabels=has_any,showgrid=True,gridcolor="#e5edfa",zeroline=False),
    )
    if not has_any:
        fig.update_yaxes(range=[0, 1],tickvals=[0,.25,.5,.75,1],showticklabels=False)
    if "승객" in y_label:
        fig.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})


def forecast_page(topic: str, data: dict[str, Any]) -> None:
    is_arrival = topic == "입항건수 예측"
    forecast_data = data.get("forecast_summary", {})
    if is_arrival:
        labels = [
            "🗓️ 2027년 예정된 입항 스케줄",
            "🚢 모델이 예측한 2027년 입항건수",
            "↔️ 예정 대비 예측 편차",
        ]
        summary_keys = ["scheduled", "predicted", "difference"]
    else:
        peak_month = forecast_data.get("peak_month")
        peak_text = f" ({peak_month}월)" if isinstance(peak_month, int) and 1 <= peak_month <= 12 else ""
        labels = [
            "👥 모델이 예측한 2027년 승객 수",
            "📊 2027년 월평균 예측 승객 수",
            f"📈 2027년 최대 예측 승객 수{peak_text}",
        ]
        # Without a 2027 ship-capacity schedule, do not fabricate capacity/difference KPIs.
        summary_keys = ["predicted", "monthly_average", "peak_value"]
    cols = st.columns(3, gap="small")
    for col, label, key in zip(cols, labels, summary_keys):
        with col:
            value = forecast_data.get(key)
            unit = ("건" if is_arrival else "명") if is_number(value) else ""
            card(label, value, suffix=unit, card_type="kpi")
    title = "월별 입항 건수 예측 및 예정 건수 비교" if is_arrival else "2027년 월별 ETS 승객 수 예측"
    st.markdown(f'<div class="panel-header">{title}</div>', unsafe_allow_html=True)
    left, right = st.columns([3.25, 1.2], gap="medium")
    with left:
        monthly_rows = data.get("monthly", [])
        has_monthly_interval = (
            isinstance(monthly_rows, list)
            and len(monthly_rows) == 12
            and all(
                isinstance(row, dict)
                and is_number(row.get("lower"))
                and is_number(row.get("upper"))
                for row in monthly_rows
            )
        )
        has_scheduled = isinstance(monthly_rows, list) and any(
            isinstance(row, dict) and is_number(row.get("scheduled"))
            for row in monthly_rows
        )
        legend = '<div class="legend-row">'
        if has_scheduled:
            legend += '<span><i class="legend-bullet"></i> 예정 스케줄</span>'
        legend += '<span><i class="legend-blue"></i> ETS 예측</span>'
        if has_monthly_interval:
            legend += '<span><i class="legend-red"></i> 95% 근사 예측구간</span>'
        legend += '</div>'
        st.markdown(legend, unsafe_allow_html=True)
        forecast_chart(monthly_rows, "입항 건수" if is_arrival else "승객 수")
        if is_arrival:
            st.markdown(
                '<div class="note">'
                '※ 2027년 입항건수 출처: 부산항만공사 크루즈 스케줄'
                '</div>',
                unsafe_allow_html=True,
            )
            if not has_monthly_interval:
                annual_interval = data.get("forecast_provenance", {}).get(
                    "annual_direct_95_approx_interval", {}
                )
                lower = annual_interval.get("lower")
                upper = annual_interval.get("upper")
                if is_number(lower) and is_number(upper):
                    st.markdown(
                        '<div class="note">※ 2027년 <b>연간</b> ETS 다이렉트 95% 근사 예측구간: '
                        f'<b>{lower:,.2f}~{upper:,.2f}건</b>. 노트북에 저장된 출력에서 '
                        '월별 95% 구간 수치를 확인할 수 없어 그래프에는 표시하지 않았습니다.</div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown(
                '<div class="note">'
                '※ 2027년 승객 수(승객정원) 출처: 부산항만공사 크루즈 스케줄'
                '</div>',
                unsafe_allow_html=True,
            )
    with right:
        note_card("운영계획 참고사항", data.get("key_results", []), results=True)


def get_theme_image(preferred_name: str, fallback_name: str) -> Path | None:
    # All optional banner artwork belongs in the images/ directory.
    # If neither PNG exists, keep the original CSS gradient background.
    for filename in (preferred_name, fallback_name):
        path = IMAGE_DIR / filename
        if path.is_file():
            return path
    return None


def show_dashboard_banner() -> None:
    banner = get_theme_image('header_banner.png', 'header_banner_fallback.png')
    if banner is not None:
        encoded = base64.b64encode(banner.read_bytes()).decode('ascii')
        banner_style = (
            'background-image:'
            'linear-gradient(90deg,#EAF6FF 0%,rgba(234,246,255,.97) 28%,'
            'rgba(234,246,255,.66) 44%,rgba(234,246,255,0) 65%),'
            f"url('data:image/png;base64,{encoded}');"
        )
    else:
        banner_style = 'background-image:linear-gradient(105deg,#FFF 0%,#E7F4FF 58%,#C2E0FA 100%);'
    st.markdown(
        f'<div class="dashboard-frame-header" style="{banner_style}">'
        '<div class="dashboard-frame-header-text">'
        '<div class="dashboard-frame-title">BUSAN CRUISE INSIGHT</div>'
        '<div class="dashboard-frame-subtitle">'
        '부산항 크루즈 입항 패턴 기반 운영계획 검토 지원 대시보드'
        '</div></div></div>',
        unsafe_allow_html=True,
    )


raw = read_data()
with st.sidebar:
    # images/sidebar_ship.png의 원본 선박 이미지를 사이드바에 표시합니다.
    st.markdown(
        '<div class="sidebar-ship-figure">'
        f'<img src="data:image/png;base64,{SIDEBAR_SHIP_ICON_BASE64}" '
        'alt="크루즈 선박" width="120">'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sidebar-brand">'
        '<div class="sidebar-brand-title">BUSAN CRUISE<br>INSIGHT</div>'
        '<div class="sidebar-brand-desc">부산항 크루즈 운영계획 <br>검토 지원</div>'
        '</div><hr class="sidebar-brand-rule">',
        unsafe_allow_html=True,
    )
    topic = st.radio(
        '분석 메뉴', ['입항건수 예측', '승객 수 예측'],
        label_visibility='collapsed', index=0,
    )
    st.markdown(
        '<div style="height:20px"></div><hr class="sidebar-brand-rule">'
        '<div class="sidebar-bottom-note">메뉴를 선택해 예측 영역을 전환할 수 있습니다.</div>',
        unsafe_allow_html=True,
    )

show_dashboard_banner()

with st.container(key='dashboard-content'):
    prefix = '1-1' if topic == '입항건수 예측' else '1-2'
    content = raw.get('arrivals' if topic == '입항건수 예측' else 'passengers', {})

    path_placeholder = st.empty()
    subtitle = content.get('page_description', '')
    st.markdown(
        f'<div class="headline"><h1>{escape(topic)}</h1><p>{escape(str(subtitle))}</p></div>',
        unsafe_allow_html=True,
    )
    view = st.segmented_control(
        '화면 선택', ['모델 소개', '2027년 예측'],
        default='모델 소개', selection_mode='single', label_visibility='collapsed',
        key=f'view_{prefix}',
    )
    view = view or '모델 소개'
    path_placeholder.markdown(
        f'<div class="section-label">{prefix}. {topic} &gt; {view}</div>',
        unsafe_allow_html=True,
    )
    if view == '모델 소개':
        model_page(topic, content)
    else:
        forecast_page(topic, content)
