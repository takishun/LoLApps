import streamlit as st
import json
from pathlib import Path

# アクセスカウンター関連
ACCESS_COUNTER_FILE = Path("access_counter_home.json")

def load_access_count():
    """アクセスカウントを読み込む"""
    if ACCESS_COUNTER_FILE.exists():
        try:
            with open(ACCESS_COUNTER_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('count', 0)
        except Exception:
            return 0
    return 0

def save_access_count(count):
    """アクセスカウントを保存する"""
    try:
        with open(ACCESS_COUNTER_FILE, 'w', encoding='utf-8') as f:
            json.dump({'count': count}, f)
    except Exception:
        pass

def increment_access_count():
    """アクセスカウントをインクリメント"""
    if 'home_access_counted' not in st.session_state:
        current_count = load_access_count()
        new_count = current_count + 1
        save_access_count(new_count)
        st.session_state.home_access_counted = True
        st.session_state.home_total_access_count = new_count
    else:
        st.session_state.home_total_access_count = load_access_count()

def main():
    st.set_page_config(
        page_title="LoL Apps - ホーム",
        page_icon="🎮",
        layout="centered"
    )

    increment_access_count()

    # ヘッダー
    st.title("🎮 LoL Apps")
    st.markdown("League of Legends の楽しいアプリ集です！")

    st.divider()

    # アプリ一覧
    st.header("📱 アプリ一覧")

    # 装備金額クイズ
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("## ⚔️")
        with col2:
            st.markdown("### 装備金額クイズ")
            st.markdown("表示された装備の合計金額を計算しよう！装備の価格を覚えるのに最適なクイズアプリです。")

            if st.button("🎯 クイズに挑戦", key="equipment_quiz", use_container_width=True):
                st.switch_page("pages/1_装備金額クイズ.py")

    st.divider()

    # ロール診断
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown("## 🎮")
        with col2:
            st.markdown("### ロール診断")
            st.markdown("5つの質問に答えて、あなたに合ったロールを見つけよう！トップ、ジャングル、ミッド、ADC、サポートの中からあなたにピッタリのロールを診断します。")

            if st.button("✨ 診断を始める", key="role_quiz", use_container_width=True):
                st.switch_page("pages/2_ロール診断.py")

    st.divider()

    # アプリ情報
    st.header("ℹ️ このアプリについて")

    st.markdown("""
    このアプリは、League of Legends (LoL) をより楽しむためのツール集です。

    **現在利用可能なアプリ:**
    - ⚔️ **装備金額クイズ** - 装備の価格を学べるクイズアプリ
    - 🎮 **ロール診断** - あなたに合ったロールを診断

    **今後追加予定:**
    - チャンピオン能力クイズ
    - ルーン推薦システム
    - ビルドガイド
    - その他...

    楽しんでください！ 🎉
    """)

    st.divider()

    # フッター
    access_count = st.session_state.get('home_total_access_count', 0)
    st.markdown(
        f"""
        <div style='text-align: center; color: #666;'>
            <small>League of Legends ファンのためのアプリ集</small><br>
            <small>👥 訪問者数: {access_count:,}</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
