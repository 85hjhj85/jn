import streamlit as st
import time
import pandas as pd

# 1. 페이지 설정 (커피와 샌드위치 이모티콘으로 변경)
st.set_page_config(page_title="샌드위치 & 커피 키오스크", page_icon="🥪", layout="wide")

# 2. 세션 상태 초기화
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'total_price' not in st.session_state:
    st.session_state.total_price = 0

# 3. 메뉴 데이터
menu_items = {
    "☕ 커피 & 음료": {
        "아메리카노": 4500,
        "카페라떼": 5000,
        "바닐라라떼": 5500,
        "복숭아 아이스티": 3500
    },
    "🥪 샌드위치": {
        "클럽 샌드위치": 7500,
        "에그마요 샌드위치": 6500,
        "BLT 샌드위치": 7000,
        "치킨 데리야끼": 8000
    }
}

# 4. 사이드바 - 실시간 장바구니
st.sidebar.title("🛒 내 장바구니")
if not st.session_state.cart:
    st.sidebar.info("장바구니가 비어 있습니다.")
else:
    # 장바구니 데이터를 표 형태로 보여주기
    df_cart = pd.DataFrame(st.session_state.cart)
    st.sidebar.table(df_cart)
    st.sidebar.subheader(f"합계: {st.session_state.total_price}원")
    
    if st.sidebar.button("🗑️ 전체 삭제"):
        st.session_state.cart = []
        st.session_state.total_price = 0
        st.rerun()

# 5. 메인 화면
st.title("🥪 브런치 키오스크 ☕")
st.write("신선한 샌드위치와 향긋한 커피를 주문해보세요.")

tabs = st.tabs(list(menu_items.keys()))

for i, category in enumerate(menu_items):
    with tabs[i]:
        cols = st.columns(4)
        for j, (name, price) in enumerate(menu_items[category].items()):
            with cols[j % 4]:
                st.container(border=True).markdown(f"**{name}**\n\n{price}원")
                if st.button(f"추가", key=f"btn_{name}"):
                    st.session_state.cart.append({"메뉴": name, "가격": price})
                    st.session_state.total_price += price
                    st.toast(f"{name}가 추가되었습니다!", icon="✅")
                    time.sleep(0.5) # 토스트 메시지를 보여주기 위한 잠깐의 대기
                    st.rerun()

# 6. 고퀄리티 결제 섹션
st.divider()
if st.button("💳 결제하기 (카드/삼성페이)", use_container_width=True, type="primary"):
    if st.session_state.cart:
        # 결제 진행 애니메이션
        with st.status("🚀 결제 처리 중...", expanded=True) as status:
            st.write("카드 정보를 확인하고 있습니다...")
            time.sleep(1)
            st.write("은행 서버와 통신 중입니다...")
            time.sleep(1)
            st.write("결제 승인 완료!")
            status.update(label="결제 완료!", state="complete", expanded=False)
        
        # 영수증 출력
        st.balloons()
        st.success("🎉 주문이 성공적으로 접수되었습니다!")
        
        with st.expander("📄 주문 영수증 확인 (클릭)", expanded=True):
            st.markdown("### [ 영수증 ]")
            st.write(f"**주문 일시:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
            st.divider()
            for item in st.session_state.cart:
                st.write(f"{item['메뉴']} : {item['가격']}원")
            st.divider()
            st.subheader(f"총 결제 금액: {st.session_state.total_price}원")
            st.write("맛있게 준비해 드릴게요! 잠시만 기다려주세요.")
        
        # 결제 후 데이터 초기화 (영수증을 보여준 후 리셋하고 싶다면 여기에 추가 로직 가능)
        # 여기서는 영수증 확인을 위해 리셋 버튼을 따로 만들거나, 일정 시간 뒤 리셋되게 할 수 있음
        if st.button("새로 주문하기"):
            st.session_state.cart = []
            st.session_state.total_price = 0
            st.rerun()
            
    else:
        st.error("장바구니가 비어 있어 결제할 수 없습니다.")
       
