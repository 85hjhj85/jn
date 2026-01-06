import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="디지털 키오스크 테스트", page_icon="🍔", layout="wide")

# 2. 세션 상태 초기화 (장바구니 저장용)
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'total_price' not in st.session_state:
    st.session_state.total_price = 0

# 3. 메뉴 데이터
menu_items = {
    "음료": {
        "아메리카노": 4500,
        "카페라떼": 5000,
        "복숭아 아이스티": 3500
    },
    "디저트": {
        "치즈 케이크": 6000,
        "초코 브라우니": 5500,
        "플레인 스콘": 3000
    }
}

# 4. 사이드바 - 장바구니 확인
st.sidebar.title("🛒 장바구니")
if not st.session_state.cart:
    st.sidebar.write("장바구니가 비어 있습니다.")
else:
    for i, item in enumerate(st.session_state.cart):
        st.sidebar.write(f"{i+1}. {item['name']} - {item['price']}원")
    st.sidebar.divider()
    st.sidebar.subheader(f"총 결제 금액: {st.session_state.total_price}원")
    
    if st.sidebar.button("장바구니 비우기"):
        st.session_state.cart = []
        st.session_state.total_price = 0
        st.rerun()

# 5. 메인 화면 - 메뉴판
st.title("🍔 미니 키오스크 시뮬레이터")
st.write("원하는 메뉴를 클릭하여 장바구니에 담아보세요.")

tabs = st.tabs(list(menu_items.keys()))

for i, category in enumerate(menu_items):
    with tabs[i]:
        cols = st.columns(3)
        for j, (name, price) in enumerate(menu_items[category].items()):
            with cols[j % 3]:
                st.info(f"**{name}**\n\n{price}원")
                if st.button(f"{name} 담기", key=f"btn_{name}"):
                    st.session_state.cart.append({"name": name, "price": price})
                    st.session_state.total_price += price
                    st.toast(f"{name}가 추가되었습니다!")
                    st.rerun()

# 6. 결제하기 버튼
st.divider()
if st.button("💳 결제하기", use_container_width=True):
    if st.session_state.cart:
        st.success(f"결제가 완료되었습니다! 총액: {st.session_state.total_price}원")
        st.balloons()
        # 결제 후 초기화
        st.session_state.cart = []
        st.session_state.total_price = 0
    else:
        st.error("장바구니에 상품을 담아주세요.")
