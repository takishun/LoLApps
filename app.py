import streamlit as st
import random

# LoLの装備データ（アイテム名と金額）
EQUIPMENT_DATA = {
    # 伝説級アイテム
    "インフィニティ・エッジ": 3400,
    "トリニティ・フォース": 3333,
    "ブレード・オブ・ザ・ルインド・キング": 3200,
    "クラーケン・スレイヤー": 3100,
    "ガレオ・フォース": 3100,
    "イモータル・シールドボウ": 3400,
    "デスダンス": 3300,
    "ガーディアン・エンジェル": 3200,
    "ソーンメイル": 2700,
    "ランデュイン・オーメン": 2700,
    "フォース・オブ・ネイチャー": 2800,
    "ラバドン・デスキャップ": 3600,
    "ゾーニャの砂時計": 3250,
    "ヴォイド・スタッフ": 3000,
    "リーチ・オブ・シャドウフレイム": 3000,
    "ルーデン・テンペスト": 3200,
    "ライレイ・クリスタルセプター": 3000,
    "デモニック・エンブレイス": 3000,
    "ブラック・クリーバー": 3100,
    "セリルダの怨恨": 3000,
    "夜の収穫者": 3200,
    "リフトメーカー": 3200,
    "サンファイア・イージス": 3200,
    "ガントレット・オブ・フロストファイア": 2800,
    "ターボケミタンク": 2800,
    "エコー・オブ・ヘリア": 2800,
    "ムーンストーン・リニューアー": 2300,
    "シュレリアの戦歌": 2300,
    "ロケット・ベルト": 3200,

    # 基本アイテム
    "ロングソード": 350,
    "クロス・オブ・エイギリティ": 600,
    "ピッケル": 875,
    "BFソード": 1300,
    "ルビークリスタル": 400,
    "チェイン・ベスト": 800,
    "アンプトーム": 1250,
    "ニードレスリー・ラージロッド": 1250,
    "ブラスティング・ワンド": 850,
    "ロスト・チャプター": 1300,
    "クロース・アーマー": 300,
    "ヌル=マジック・マント": 450,
    "リカーブ・ボウ": 1000,
    "ドラン・ブレード": 450,
    "ドラン・リング": 400,
    "ドラン・シールド": 450,

    # コンポーネントアイテム
    "ヴァンパイア・セプター": 900,
    "フィエンディッシュ・コーデックス": 900,
    "スティンガー": 1100,
    "ヘクステック・オルタネーター": 1050,
    "セレイテッド・ダーク": 800,
    "ラストウィスパー": 1300,
    "シーン": 700,
    "グレイシャル・バックラー": 900,
    "エイテル・ウィスプ": 850,
    "キンドルジェム": 800,
    "ウォーデン・メイル": 1000,
    "スペクターズ・カウル": 1100,
    "バンビーズ・シンダー": 1000,
    "カリブディス・クロー": 1100,
    "リーサル・テンポ": 1200,
    "サイフォニング・ストライク": 900,

    # ブーツ
    "バーサーカー・グリーブス": 1100,
    "ソーサラー・シューズ": 1100,
    "プレート・スティール・キャップ": 1100,
    "マーキュリー・トレッド": 1100,
    "アイオニア・ブーツ": 900,
    "スウィフトネス・ブーツ": 900,
    "モビリティ・ブーツ": 900,
}

def initialize_session_state():
    """セッション状態の初期化"""
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'current_equipment' not in st.session_state:
        st.session_state.current_equipment = []
    if 'correct_answer' not in st.session_state:
        st.session_state.correct_answer = 0
    if 'answered' not in st.session_state:
        st.session_state.answered = False
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = 'easy'
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False

def generate_quiz(difficulty):
    """難易度に応じてクイズを生成"""
    if difficulty == 'easy':
        num_items = random.randint(2, 3)
    elif difficulty == 'medium':
        num_items = random.randint(3, 4)
    else:  # hard
        num_items = random.randint(4, 6)

    equipment_list = list(EQUIPMENT_DATA.items())
    selected_equipment = random.sample(equipment_list, num_items)

    st.session_state.current_equipment = selected_equipment
    st.session_state.correct_answer = sum(price for _, price in selected_equipment)
    st.session_state.answered = False
    st.session_state.show_answer = False

def check_answer(user_answer):
    """回答をチェック"""
    st.session_state.answered = True
    st.session_state.total_questions += 1

    if user_answer == st.session_state.correct_answer:
        st.session_state.score += 1
        st.session_state.streak += 1
        return True
    else:
        st.session_state.streak = 0
        return False

def reset_stats():
    """統計をリセット"""
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.total_questions = 0
    st.session_state.answered = False
    st.session_state.show_answer = False

def main():
    st.set_page_config(
        page_title="LoL 装備金額クイズ",
        page_icon="⚔️",
        layout="centered"
    )

    initialize_session_state()

    # ヘッダー
    st.title("⚔️ LoL 装備金額クイズ")
    st.markdown("表示された装備の合計金額を計算しよう！")

    # サイドバー - 設定と統計
    with st.sidebar:
        st.header("⚙️ 設定")

        # 難易度選択
        difficulty = st.radio(
            "難易度:",
            ["easy", "medium", "hard"],
            index=["easy", "medium", "hard"].index(st.session_state.difficulty),
            format_func=lambda x: {
                "easy": "簡単 (2-3個)",
                "medium": "普通 (3-4個)",
                "hard": "難しい (4-6個)"
            }[x]
        )

        if difficulty != st.session_state.difficulty:
            st.session_state.difficulty = difficulty
            if st.session_state.current_equipment:
                generate_quiz(difficulty)

        st.divider()

        st.header("📊 統計")
        st.metric("スコア", f"{st.session_state.score}/{st.session_state.total_questions}")
        st.metric("連続正解", st.session_state.streak)

        if st.session_state.total_questions > 0:
            accuracy = (st.session_state.score / st.session_state.total_questions) * 100
            st.metric("正答率", f"{accuracy:.1f}%")

        st.divider()

        if st.button("📊 統計をリセット", use_container_width=True):
            reset_stats()
            st.rerun()

    # 初回またはクイズがない場合は新しいクイズを生成
    if not st.session_state.current_equipment:
        generate_quiz(st.session_state.difficulty)

    # 装備表示
    st.subheader("装備リスト")

    for item_name, price in st.session_state.current_equipment:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{item_name}**")
        with col2:
            if st.session_state.show_answer or st.session_state.answered:
                st.markdown(f"🪙 {price:,}")
            else:
                st.markdown("🪙 ???")

    st.divider()

    # 回答欄
    if not st.session_state.answered:
        st.subheader("回答")

        col1, col2 = st.columns([3, 1])

        with col1:
            user_answer = st.number_input(
                "合計金額を入力:",
                min_value=0,
                step=100,
                key="answer_input"
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("回答する", type="primary", use_container_width=True):
                if user_answer > 0:
                    is_correct = check_answer(user_answer)
                    st.rerun()
                else:
                    st.warning("金額を入力してください")

        if st.button("💡 答えを見る", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()

    else:
        # 結果表示
        is_correct = st.session_state.score > 0 and st.session_state.streak > 0

        if is_correct:
            st.success(f"🎉 正解！合計金額は {st.session_state.correct_answer:,} ゴールドです！")
        else:
            st.error(f"❌ 不正解。正解は {st.session_state.correct_answer:,} ゴールドでした。")

        if st.button("➡️ 次の問題", type="primary", use_container_width=True):
            generate_quiz(st.session_state.difficulty)
            st.rerun()

    # 答えを見る場合の表示
    if st.session_state.show_answer and not st.session_state.answered:
        st.info(f"💡 正解: {st.session_state.correct_answer:,} ゴールド")

        if st.button("➡️ 次の問題", use_container_width=True):
            generate_quiz(st.session_state.difficulty)
            st.rerun()

    # フッター
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <small>League of Legends の装備金額を使用したクイズアプリです</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
