import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="MBTI x 포켓몬 단짝 찾기",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 파스텔 하늘색 테마 & 큰 글씨 CSS 주입
st.markdown("""
<style>
    /* 전체 배경 하늘색 그라데이션 및 폰트 설정 */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        color: #0f172a;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    /* 메인 타이틀 */
    .title-box {
        text-align: center;
        background: rgba(255, 255, 255, 0.85);
        padding: 25px 20px;
        border-radius: 24px;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.15);
        margin-bottom: 25px;
        border: 2px solid #7dd3fc;
    }
    
    .title-box h1 {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #0284c7 !important;
        margin: 0 0 10px 0 !important;
    }
    
    .title-box p {
        font-size: 1.15rem !important;
        color: #0369a1 !important;
        margin: 0 !important;
    }

    /* 카드 컨테이너 */
    .card-container {
        background-color: #ffffff;
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 12px 30px rgba(2, 132, 199, 0.12);
        border: 2px solid #e0f2fe;
        text-align: center;
        margin-top: 15px;
    }

    /* 태그 스타일 */
    .badge {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0284c7;
        padding: 6px 16px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 12px;
    }

    .mbti-badge {
        display: inline-block;
        background-color: #0284c7;
        color: #ffffff;
        padding: 6px 16px;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 15px;
    }

    /* 포켓몬 이름 */
    .pokemon-title {
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        color: #0f172a !important;
        margin: 8px 0 15px 0 !important;
    }

    /* 설명 상자 */
    .desc-box {
        background-color: #f0f9ff;
        border-left: 5px solid #0284c7;
        padding: 16px 20px;
        border-radius: 12px;
        text-align: left;
        margin-top: 20px;
        font-size: 1.15rem;
        line-height: 1.7;
        color: #1e293b;
    }

    /* 드롭다운 라벨 및 컨트롤 크기 확대 */
    div[data-baseweb="select"] {
        font-size: 1.2rem !important;
    }
    
    .stSelectbox label {
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        color: #0369a1 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 16가지 MBTI 포켓몬 데이터베이스
POKEMON_DATA = {
    "ISTJ": {
        "kor_name": "거북왕",
        "eng_name": "Blastoise",
        "id": 9,
        "type": "💧 물",
        "trait": "성실하고 신뢰감 높은 해결사",
        "reason": "묵묵하고 책임감이 강하여 어떤 위기 속에서도 결코 흔들리지 않습니다. ISTJ의 원칙주의적인 성향과 깊은 신뢰를 쌓아 평생을 함께할 든든한 단짝입니다."
    },
    "ISFJ": {
        "kor_name": "해피너스",
        "eng_name": "Blissey",
        "id": 242,
        "type": "⚪ 노말",
        "trait": "따뜻하고 자상한 수호자",
        "reason": "타인을 진심으로 챙기고 보살피는 헌신적인 포켓몬입니다. 세심한 배려심을 가진 ISFJ 옆에서 따뜻한 온기와 안식처를 더해줍니다."
    },
    "INFJ": {
        "kor_name": "가디안",
        "eng_name": "Gardevoir",
        "id": 282,
        "type": "🔮 초능력 / 🧚 페어리",
        "trait": "신비롭고 깊은 통찰력의 예언자",
        "reason": "트레이너의 마음을 깊이 이해하며 끝까지 충성을 다하는 포켓몬입니다. 깊은 생각과 이상을 품은 INFJ와 영혼의 콤비를 이룹니다."
    },
    "INTJ": {
        "kor_name": "뮤츠",
        "eng_name": "Mewtwo",
        "id": 150,
        "type": "🔮 초능력",
        "trait": "냉철한 전략가이자 지성파",
        "reason": "독보적인 지능과 압도적인 통찰력을 지니고 있습니다. 장기적 비전을 설계하는 INTJ와 함께 세계를 완벽하게 분석해 나갈 궁극의 파트너입니다."
    },
    "ISTP": {
        "kor_name": "루카리오",
        "eng_name": "Lucario",
        "id": 448,
        "type": "🥊 격투 / ⚙️ 강철",
        "trait": "침착하고 세련된 실전파",
        "reason": "상황 파악이 빠르고 과묵하면서도 문제 해결 능력이 매우 뛰어납니다. 손재주가 좋고 임기응변에 강한 ISTP와 최고의 콤비를 자랑합니다."
    },
    "ISFP": {
        "kor_name": "메타몽",
        "eng_name": "Ditto",
        "id": 132,
        "type": "⚪ 노말",
        "trait": "유연하고 예술적인 변신술사",
        "reason": "상대방과 환경에 맞춰 마음껏 형태를 바꾸는 온화한 매력이 있습니다. 자유롭고 온화한 ISFP에게 편안함과 즐거움을 선물합니다."
    },
    "INFP": {
        "kor_name": "님피아",
        "eng_name": "Sylveon",
        "id": 700,
        "type": "🧚 페어리",
        "trait": "풍부한 감성과 감수성의 소유자",
        "reason": "안테나 같은 리본으로 상대의 마음을 여는 따뜻한 포켓몬입니다. 다정한 마음과 깊은 이상을 꿈꾸는 INFP의 마음을 완벽히 이해해 줍니다."
    },
    "INTP": {
        "kor_name": "후딘",
        "eng_name": "Alakazam",
        "id": 65,
        "type": "🔮 초능력",
        "trait": "끊임없이 탐구하는 천재 학자",
        "reason": "IQ 5000에 달하는 놀라운 기억력과 호기심을 자랑합니다. 지적 호기심과 논리적 분석을 좋아하는 INTP에게 더없는 대화 상대가 되어줍니다."
    },
    "ESTP": {
        "kor_name": "피카츄",
        "eng_name": "Pikachu",
        "id": 25,
        "type": "⚡ 전기",
        "trait": "에너지 넘치는 모험가",
        "reason": "순발력이 뛰어나고 언제나 새로운 자극과 모험을 즐깁니다. 행동력이 넘치는 ESTP와 만나면 세상 어디든 즐거운 무대가 됩니다."
    },
    "ESFP": {
        "kor_name": "푸린",
        "eng_name": "Jigglypuff",
        "id": 39,
        "type": "⚪ 노말 / 🧚 페어리",
        "trait": "사랑스러운 무대의 슈퍼스타",
        "reason": "사람들의 시선을 집중시키고 무대를 밝히는 화려한 매력이 있습니다. 흥과 사교성이 넘치는 ESFP의 활력을 더욱 빛나게 해줍니다."
    },
    "ENFP": {
        "kor_name": "이브이",
        "eng_name": "Eevee",
        "id": 133,
        "type": "⚪ 노말",
        "trait": "무한한 가능성을 가진 꿈나무",
        "reason": "어디로든 진화할 수 있는 다재다능함과 상상력을 품고 있습니다. 톡톡 튀는 아이디어와 열정이 가득한 ENFP와 완벽하게 닮았습니다."
    },
    "ENTP": {
        "kor_name": "팬텀",
        "eng_name": "Gengar",
        "id": 94,
        "type": "👻 고스트 / ☠️ 독",
        "trait": "재치 있는 개구쟁이 아이디어맨",
        "reason": "유쾌하고 엉뚱한 장난으로 좌중을 사로잡는 분위기 메이커입니다. 신선한 자극과 창의적 논쟁을 즐기는 ENTP의 최고의 장난 콤비입니다."
    },
    "ESTJ": {
        "kor_name": "윈디",
        "eng_name": "Arcanine",
        "id": 59,
        "type": "🔥 불꽃",
        "trait": "위엄 있고 당당한 리더",
        "reason": "용맹함과 강한 리더십으로 주위를 이끄는 늠름한 포켓몬입니다. 체계적이고 확실한 주관을 가진 ESTJ와 완벽한 시너지를 이룹니다."
    },
    "ESFJ": {
        "kor_name": "토게키스",
        "eng_name": "Togekiss",
        "id": 468,
        "type": "⚪ 노말 / 🕊️ 비행",
        "trait": "행복과 평화를 나누는 천사",
        "reason": "다정한 기운을 퍼뜨리며 주변 사람들에게 친절을 베폅니다. 분위기를 밝게 만들고 친목을 중요시하는 ESFJ와 꼭 닮은 친구입니다."
    },
    "ENFJ": {
        "kor_name": "망나뇽",
        "eng_name": "Dragonite",
        "id": 149,
        "type": "🐉 드래곤 / 🕊️ 비행",
        "trait": "마음이 넓은 다정한 조력자",
        "reason": "바다에서 조난당한 사람을 구해주는 헌신적인 리더형 포켓몬입니다. 주위 사람들을 이끌며 긍정적인 에너지를 전하는 ENFJ의 단짝입니다."
    },
    "ENTJ": {
        "kor_name": "리자몽",
        "eng_name": "Charizard",
        "id": 6,
        "type": "🔥 불꽃 / 🕊️ 비행",
        "trait": "열정적이고 야망 넘치는 지배자",
        "reason": "강한 승부욕과 추진력으로 어떤 목표든 당당히 개척해 나갑니다. 뛰어난 지도력과 원대한 목표를 가진 ENTJ의 열정과 똑같이 닮아있습니다."
    }
}

# 4. 앱 헤더 화면
st.markdown("""
<div class="title-box">
    <h1>⚡ MBTI x 포켓몬 단짝 찾기</h1>
    <p>나의 성격 유형과 꼭 닮은 운명의 단짝 포켓몬을 만나보세요!</p>
</div>
""", unsafe_allow_html=True)

# 5. MBTI 선택 셀렉트박스
mbti_list = list(POKEMON_DATA.keys())
selected_mbti = st.selectbox(
    "👉 당신의 MBTI 유형을 선택해 주세요:",
    options=["선택하세요..."] + mbti_list,
    index=0
)

# 6. 결과 출력
if selected_mbti != "선택하세요...":
    # 축하 폭죽 효과!
    st.balloons()
    
    data = POKEMON_DATA[selected_mbti]
    # 공식 PokeAPI 고화질 이미지 URL
    img_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['id']}.png"
    
    # 결과 카드 생성
    st.markdown(f"""
    <div class="card-container">
        <div class="mbti-badge">{selected_mbti} 유형의 단짝</div>
        <div class="pokemon-title">{data['kor_name']} <span style="font-size:1.3rem; color:#64748b;">({data['eng_name']})</span></div>
        <div>
            <span class="badge">타입: {data['type']}</span>
            <span class="badge" style="background-color:#fef3c7; color:#d97706;">{data['trait']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 포켓몬 이미지 표시
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(img_url, use_container_width=True)
        
    # 어울리는 이유 설명
    st.markdown(f"""
    <div class="desc-box">
        💡 <strong>{data['kor_name']}이(가) {selected_mbti}의 단짝인 이유:</strong><br><br>
        {data['reason']}
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("👆 위 드롭다운 목록에서 MBTI를 선택하면 어울리는 포켓몬이 나타납니다!")
