import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="Recycle Map",
    page_icon="♻️",
    layout="wide"
)

# -----------------------------
# 데이터
# -----------------------------
facilities = [
    {"시설명": "천안시청", "종류": "폐건전지", "위도": 36.8151, "경도": 127.1139},
    {"시설명": "천안시청", "종류": "폐형광등", "위도": 36.8151, "경도": 127.1139},
    {"시설명": "불당동 행정복지센터", "종류": "의류수거함", "위도": 36.8100, "경도": 127.1080},
    {"시설명": "신방동 주민센터", "종류": "소형가전", "위도": 36.7820, "경도": 127.1260},
    {"시설명": "두정동 주민센터", "종류": "폐건전지", "위도": 36.8330, "경도": 127.1420},
    {"시설명": "성정동 주민센터", "종류": "의류수거함", "위도": 36.8250, "경도": 127.1310}
]

df = pd.DataFrame(facilities)

# -----------------------------
# 거리 계산
# -----------------------------
def distance(lat1, lon1, lat2, lon2):
    r = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c

# -----------------------------
# 제목
# -----------------------------
st.title("♻️ Recycle Map")
st.caption("특수 분리수거 시설을 쉽고 빠르게 찾아보세요")

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("검색 설정")

user_lat = st.sidebar.number_input(
    "현재 위치 위도",
    value=36.8151,
    format="%.6f"
)

user_lon = st.sidebar.number_input(
    "현재 위치 경도",
    value=127.1139,
    format="%.6f"
)

selected_type = st.sidebar.selectbox(
    "시설 종류",
    ["전체", "폐건전지", "폐형광등", "의류수거함", "소형가전"]
)

filtered = df.copy()

if selected_type != "전체":
    filtered = filtered[filtered["종류"] == selected_type]

if not filtered.empty:
    filtered["거리"] = filtered.apply(
        lambda row: distance(
            user_lat,
            user_lon,
            row["위도"],
            row["경도"]
        ),
        axis=1
    )

    filtered = filtered.sort_values("거리")

# -----------------------------
# 지도 (맨 위)
# -----------------------------
st.subheader("🗺️ 시설 위치")

if not filtered.empty:
    map_df = filtered.rename(
        columns={
            "위도": "lat",
            "경도": "lon"
        }
    )

    st.map(
        map_df[["lat", "lon"]],
        height=300
    )

# -----------------------------
# 통계 카드
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "검색된 시설",
        len(filtered)
    )

with col2:
    st.metric(
        "시설 종류",
        filtered["종류"].nunique()
        if not filtered.empty
        else 0
    )

with col3:
    st.metric(
        "전체 시설",
        len(df)
    )

# -----------------------------
# 가장 가까운 시설
# -----------------------------
if not filtered.empty:

    nearest = filtered.iloc[0]

    st.success(
        f"""
가장 가까운 시설

📍 {nearest['시설명']}
        
♻️ {nearest['종류']}

📏 {nearest['거리']:.2f} km
"""
    )

# -----------------------------
# 시설 목록
# -----------------------------
st.subheader("📍 시설 목록")

if filtered.empty:
    st.warning("검색 결과가 없습니다.")
else:
    show_df = filtered[
        ["시설명", "종류", "거리"]
    ].copy()

    show_df["거리"] = show_df["거리"].round(2)

    st.dataframe(
        show_df,
        use_container_width=True
    )

# -----------------------------
# 분리배출 가이드
# -----------------------------
st.subheader("📚 분리배출 가이드")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🔋 폐건전지",
        "💡 폐형광등",
        "👕 의류",
        "🖥️ 소형가전"
    ]
)

with tab1:
    st.info("""
• 일반쓰레기 금지

• 전용 수거함 이용

• 누액 시 비닐 밀봉
""")

with tab2:
    st.info("""
• 깨지지 않게 배출

• 전용 수거함 이용

• 종량제 봉투 금지
""")

with tab3:
    st.info("""
• 세탁 후 배출

• 젖은 의류 금지

• 신발은 한 쌍으로 묶기
""")

with tab4:
    st.info("""
• 배터리 제거 가능 시 제거

• 주민센터 수거함 이용

• 일반쓰레기 금지
""")

st.markdown("---")
st.caption("🌎 올바른 분리배출은 환경 보호의 첫걸음입니다.")
