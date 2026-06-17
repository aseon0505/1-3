# CSS 스타일
st.markdown("""
<style>
.main {
    background-color: #f5fff7;
}

.main-title {
    text-align: center;
    color: #1b5e20;
    font-size: 3rem;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #4caf50;
    font-size: 1.2rem;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

.big-banner {
    background: linear-gradient(135deg,#4CAF50,#81C784);
    color: white;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #388E3C;
}

[data-testid="stSidebar"] {
    background-color: #e8f5e9;
}
</style>
""", unsafe_allow_html=True)
