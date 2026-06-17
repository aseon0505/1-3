import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="Recycle Map",
    page_icon="♻️",
    layout="wide"
)

st.title("♻️ Recycle Map")
st.subheader("특수 분리수거 시설 찾기")

# -----------------------------
# 샘플 데이터
# -----------------------------
data = [
    ["천안시청", "폐건전지", 36.8151, 127.1139],
    ["천안시청", "폐형광등", 36.8151, 127.1139],
    ["불당동 행정복지센터", "의류수거함", 36.8100, 127.1080],
    ["신방동 주민센터", "소형가전", 36.7820, 127.1260],
    ["두정동 주민센터", "폐건전지", 36.8330, 127.1420],
    ["성정동 주민센터", "의류수거함", 36.8250, 127.1310]
]

df = pd.DataFrame(
    data,
    columns=["시설명", "종류", "lat", "lon"]
)

# -----------------------------
# 거리 계산 함수
# -----------------------------
def distance(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# -----------------------------
# 위치 입력
# -----------------------------
st.sidebar.header("검색 설정")

user_lat = st.sidebar.number_input(
    "위도",
    value=36.8151,
    format="%.6f"
)

user_lon = st.sidebar.number_input(
    "경도",
    value=127.1139,
    format="%.6f"
)

facility_type = st.sidebar.selectbox(
    "시설 종류",
    ["전체", "폐건전지", "의류수거함", "폐형광등", "소형가전"]
)

# -----------------------------
# 필터링
# -----------------------------
filtered = df.copy()

if facility_type != "전체":
    filtered = filtered[filtered["종류"] == facility_type]

# -----------------------------
# 거리 계산
# -----------------------------
if not filtered.empty:
    filtered["거리(km)"] = filtered.apply(
        lambda row: distance(
            user_lat,
            user_lon,
            row["lat"],
            row["lon"]
        ),
        axis=1
    )

    filtered = filtered.sort_values("거리(km)")

# -----------------------------
# 결과 출력
# -----------------------------
st.header("📍 주변 시설")

if filtered.empty:
    st.warning("검색 결과가 없습니다.")
else:
    st.dataframe(
        filtered[
            ["시설명", "종류", "거리(km)"]
        ].round(2),
        use_container_width=True
    )

    nearest = filtered.iloc[0]

    st.success(
        f"가장 가까운 시설은 "
        f"{nearest['시설명']} "
        f"({nearest['종류']}) "
        f"이며 약 "
        f"{nearest['거리(km)']:.2f}km 떨어져 있습니다."
    )

# -----------------------------
# 지도
# -----------------------------
st.header("🗺️ 지도")

map_df = filtered[["lat", "lon"]]

if not map_df.empty:
    st.map(map_df)

# -----------------------------
# 분리배출 가이드
# -----------------------------
st.header("📚 분리배출 가이드")

guides = {
    "폐건전지":
        """
        • 일반쓰레기로 버리지 않기
        • 전용 수거함 이용
        • 누액이 있는 경우 비닐에 밀봉
        """,

    "의류수거함":
        """
        • 세탁 후 배출
        • 젖은 옷 금지
        • 신발은 묶어서 배출
        """,

    "폐형광등":
        """
        • 깨지지 않게 배출
        • 전용 수거함 이용
        • 일반 종량제 봉투 금지
        """,

    "소형가전":
        """
        • 배터리 제거 가능 시 제거
        • 주민센터 수거함 이용
        • 재활용센터 이용 가능
        """
}

item = st.selectbox(
    "품목 선택",
    list(guides.keys())
)

st.info(guides[item])

# -----------------------------
# 푸터
# -----------------------------
st.markdown("---")
st.caption("환경 보호를 위한 올바른 분리배출 습관을 실천해보세요.")
