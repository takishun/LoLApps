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
    st.markdown(
        """
        <div style='text-align: center;'>
            <h1>🎮 LoL Apps</h1>
            <h3>League of Legends ウェブアプリ集</h3>
            <p style='color: #666; font-size: 1.1em;'>
                LoLをもっと楽しく、もっと上手くなるための<br>
                ちょっとした便利なウェブアプリを集めたサイトです
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # サイト紹介
    st.markdown("""
    ### 🌟 LoL Apps について

    **LoL Apps** は、League of Legends プレイヤーのための学習・診断ツールを提供する
    無料のウェブアプリケーションサイトです。

    - 🎯 **楽しく学べる** - ゲーム感覚で知識を身につけられるクイズ形式
    - 🔍 **自己分析** - あなたのプレイスタイルを診断して最適なロールを発見
    - 📱 **簡単アクセス** - ブラウザだけで、いつでもどこでも利用可能
    - 🆓 **完全無料** - すべての機能を無料で使えます

    初心者から上級者まで、すべてのサモナーに役立つツールを目指しています！
    """)

    st.divider()

    # アプリ一覧
    st.header("📱 公開中のアプリ")
    st.markdown("")

    # 装備金額クイズ
    with st.container():
        st.markdown("### ⚔️ 装備金額クイズ")

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown("""
            **装備の価格を覚えてゴールド管理を極めよう！**

            表示された装備アイテムの合計金額を計算するクイズアプリです。
            装備の価格を正確に把握することで、より戦略的なプレイが可能になります。

            **主な機能:**
            - 🎚️ 3段階の難易度選択（簡単・普通・難しい）
            - 📊 スコアと正答率の記録
            - 🔥 連続正解でコンボを狙おう
            - 💡 答えを見る機能で学習サポート

            **こんな人におすすめ:**
            - 装備の価格を覚えたい初心者
            - ゴールド管理を改善したい中級者
            - 完璧な知識を目指す上級者
            """)

        with col2:
            st.info("""
            **対象ユーザー**
            🔰 初心者
            ⭐ 中級者
            💎 上級者

            **所要時間**
            ⏱️ 1問 約30秒

            **難易度**
            📈 選択可能
            (2-6個の装備)
            """)

            if st.button("🎯 クイズに挑戦", key="equipment_quiz", type="primary", use_container_width=True):
                st.switch_page("pages/1_装備金額クイズ.py")

    st.divider()

    # ロール診断
    with st.container():
        st.markdown("### 🎮 ロール診断")

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown("""
            **5つの質問であなたにピッタリのロールを発見！**

            プレイスタイルや好みに基づいて、あなたに最も適したロールを診断します。
            まだメインロールが決まっていない人、新しいロールに挑戦したい人におすすめです。

            **診断内容:**
            - ❓ 5つの質問に答えるだけ（約2分）
            - 🎯 プレイスタイル、戦闘距離、得意な判断など
            - 📊 5つのロール全てとの相性を表示
            - 📝 各ロールの詳しい説明とおすすめチャンピオン

            **診断できるロール:**
            - 🛡️ トップレーン（タンク・ファイター）
            - 🌳 ジャングル（マップ全体を制圧）
            - ⚡ ミッドレーン（キャリー・メイジ）
            - 🏹 ADC（持続ダメージ）
            - 💚 サポート（味方を支える）
            """)

        with col2:
            st.info("""
            **対象ユーザー**
            🔰 初心者
            ⭐ 中級者

            **所要時間**
            ⏱️ 約2分

            **診断精度**
            📊 5段階評価
            詳細な相性分析
            """)

            if st.button("✨ 診断を始める", key="role_quiz", type="primary", use_container_width=True):
                st.switch_page("pages/2_ロール診断.py")

    st.divider()

    # 今後の予定
    st.header("🚀 今後の予定")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **🎯 クイズ系**
        - チャンピオン能力クイズ
        - ルーンクイズ
        - ゲーム知識クイズ
        """)

    with col2:
        st.markdown("""
        **📊 診断・分析系**
        - プレイスタイル診断
        - チャンピオン推薦
        - チーム構成分析
        """)

    with col3:
        st.markdown("""
        **🛠️ ツール系**
        - ビルドガイド
        - カウンターチェック
        - タイマー・計算機
        """)

    st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <p style='color: #888;'>
            ご要望やアイデアがありましたら、お気軽にお知らせください！<br>
            今後も便利なツールを追加していきます 🎉
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # フッター
    access_count = st.session_state.get('home_total_access_count', 0)
    st.markdown(
        f"""
        <div style='text-align: center; color: #666; padding: 20px 0;'>
            <p style='margin: 10px 0;'>
                <strong>LoL Apps</strong> - League of Legends ファンのためのウェブアプリサイト
            </p>
            <p style='margin: 5px 0; font-size: 0.9em;'>
                🎮 楽しく学べる | 📊 自己分析 | 🆓 完全無料
            </p>
            <p style='margin: 15px 0; font-size: 0.85em;'>
                👥 総訪問者数: <strong>{access_count:,}</strong>
            </p>
            <p style='margin: 10px 0; font-size: 0.8em; color: #999;'>
                ※ League of Legends および関連する全ての商標は Riot Games, Inc. に帰属します<br>
                本サイトは非公式のファンサイトです
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
