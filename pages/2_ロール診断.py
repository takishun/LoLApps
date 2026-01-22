import streamlit as st
import json
from pathlib import Path

# アクセスカウンター関連
ACCESS_COUNTER_FILE = Path("access_counter_role.json")

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
    if 'role_access_counted' not in st.session_state:
        current_count = load_access_count()
        new_count = current_count + 1
        save_access_count(new_count)
        st.session_state.role_access_counted = True
        st.session_state.role_total_access_count = new_count
    else:
        st.session_state.role_total_access_count = load_access_count()

def initialize_session_state():
    """セッション状態の初期化"""
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'result_calculated' not in st.session_state:
        st.session_state.result_calculated = False

# 5つの質問と選択肢
QUESTIONS = [
    {
        "question": "あなたの好きなプレイスタイルは？",
        "options": [
            {"text": "チームを守り、前線で戦う", "roles": {"Top": 3, "Support": 2, "Jungle": 1}},
            {"text": "高いダメージを出して敵を倒す", "roles": {"Mid": 3, "ADC": 2, "Top": 1}},
            {"text": "味方をサポートして勝利に貢献", "roles": {"Support": 3, "Jungle": 2, "Mid": 1}},
            {"text": "マップ全体を動き回って影響を与える", "roles": {"Jungle": 3, "Mid": 2, "Support": 1}},
        ]
    },
    {
        "question": "好きな戦闘距離は？",
        "options": [
            {"text": "近接戦闘で敵と殴り合う", "roles": {"Top": 3, "Jungle": 2, "Support": 1}},
            {"text": "中距離から魔法やスキルで攻撃", "roles": {"Mid": 3, "Support": 2, "Top": 1}},
            {"text": "遠距離から安全に攻撃", "roles": {"ADC": 3, "Mid": 2, "Support": 1}},
            {"text": "距離は気にしない、状況に応じて", "roles": {"Jungle": 2, "Mid": 2, "Support": 2}},
        ]
    },
    {
        "question": "ゲームのどの時間帯で活躍したい？",
        "options": [
            {"text": "序盤から積極的に戦いたい", "roles": {"Jungle": 3, "Top": 2, "Support": 2}},
            {"text": "中盤でチームファイトを主導したい", "roles": {"Mid": 3, "Jungle": 2, "Top": 1}},
            {"text": "後半の集団戦で真価を発揮したい", "roles": {"ADC": 3, "Mid": 2, "Top": 2}},
            {"text": "全ての時間帯で安定して貢献したい", "roles": {"Support": 3, "Jungle": 2, "Mid": 1}},
        ]
    },
    {
        "question": "どのような判断が得意？",
        "options": [
            {"text": "1対1の戦闘の駆け引き", "roles": {"Top": 3, "Mid": 2, "ADC": 1}},
            {"text": "マップ全体の状況把握と戦略", "roles": {"Jungle": 3, "Mid": 2, "Support": 2}},
            {"text": "集団戦での立ち位置とタイミング", "roles": {"ADC": 3, "Mid": 2, "Support": 2}},
            {"text": "味方を守るタイミングとスキル使用", "roles": {"Support": 3, "Top": 1, "Jungle": 1}},
        ]
    },
    {
        "question": "リスクとリターンの好みは？",
        "options": [
            {"text": "ハイリスク・ハイリターンで一発逆転", "roles": {"Mid": 3, "Jungle": 2, "Top": 2}},
            {"text": "ローリスクで確実にダメージを出す", "roles": {"ADC": 3, "Top": 1, "Mid": 1}},
            {"text": "リスクは低く、味方を支える", "roles": {"Support": 3, "Top": 1, "ADC": 1}},
            {"text": "計算されたリスクでチャンスを掴む", "roles": {"Jungle": 3, "Mid": 2, "Top": 1}},
        ]
    }
]

# ロールの説明
ROLE_DESCRIPTIONS = {
    "Top": {
        "emoji": "🛡️",
        "name": "トップレーン",
        "description": "トップレーンは孤独な戦場。1対1での戦いに強く、序盤から中盤にかけてレーンで相手を圧倒します。タンクやファイターが多く、チームファイトでは前線を張る役割です。",
        "champions": "ダリウス、ガレン、フィオラ、ケイル、セト、など"
    },
    "Jungle": {
        "emoji": "🌳",
        "name": "ジャングル",
        "description": "マップ全体を見渡し、どこに行くべきか判断する戦略的なロール。中立モンスターを狩りながら経験値とゴールドを稼ぎ、各レーンにガンクして味方を助けます。マップ全体への影響力が最も大きいです。",
        "champions": "リー・シン、カジックス、エリス、グレイブス、アムム、など"
    },
    "Mid": {
        "emoji": "⚡",
        "name": "ミッドレーン",
        "description": "マップの中央で戦い、高いダメージで敵を倒すロール。メイジやアサシンが多く、集団戦で大ダメージを出すか、敵の重要なターゲットを瞬殺します。キャリー能力が高く、ゲームを決める力を持ちます。",
        "champions": "ゼド、アーリ、シンドラ、オリアナ、ヤスオ、など"
    },
    "ADC": {
        "emoji": "🏹",
        "name": "ADC（ボットレーン）",
        "description": "持続的な物理ダメージを担当するロール。序盤は弱いですが、アイテムを積むことで後半の集団戦で最も高いダメージを出せるようになります。ポジショニングが重要で、生き残りながらダメージを出す技術が求められます。",
        "champions": "ジンクス、ケイトリン、エズリアル、ヴェイン、ジン、など"
    },
    "Support": {
        "emoji": "💚",
        "name": "サポート",
        "description": "ADCと共にボットレーンで戦い、味方全体をサポートするロール。回復やシールド、CC（群衆制御）で味方を守り、敵を妨害します。ビジョンコントロールも担当し、チームの目となります。ゴールドが少なくても活躍できます。",
        "champions": "スレッシュ、ルル、ナミ、レオナ、ブリッツクランク、など"
    }
}

def calculate_result():
    """回答からおすすめロールを計算"""
    role_scores = {"Top": 0, "Jungle": 0, "Mid": 0, "ADC": 0, "Support": 0}

    for q_idx, answer_idx in st.session_state.answers.items():
        roles = QUESTIONS[q_idx]["options"][answer_idx]["roles"]
        for role, score in roles.items():
            role_scores[role] += score

    # スコアの高い順にソート
    sorted_roles = sorted(role_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_roles

def reset_quiz():
    """クイズをリセット"""
    st.session_state.quiz_started = False
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.result_calculated = False

def main():
    st.set_page_config(
        page_title="LoL ロール診断",
        page_icon="🎮",
        layout="centered"
    )

    initialize_session_state()
    increment_access_count()

    # ヘッダー
    st.title("🎮 LoL ロール診断")
    st.markdown("5つの質問に答えて、あなたに合ったロールを見つけよう！")

    # クイズ開始前
    if not st.session_state.quiz_started:
        st.divider()
        st.markdown("""
        ### 📋 診断について

        League of Legends には5つのロールがあります：
        - 🛡️ **トップレーン** - タンクやファイター、1対1が得意
        - 🌳 **ジャングル** - マップ全体を動き回り、戦略的にプレイ
        - ⚡ **ミッドレーン** - 高火力でキャリー、ゲームメイカー
        - 🏹 **ADC** - 後半に強力な持続ダメージ
        - 💚 **サポート** - 味方を支え、チームに貢献

        あなたのプレイスタイルに最も合ったロールを診断します！
        """)

        st.divider()

        if st.button("🚀 診断を開始する", type="primary", use_container_width=True):
            st.session_state.quiz_started = True
            st.rerun()

    # クイズ進行中
    elif st.session_state.quiz_started and not st.session_state.result_calculated:
        current_q = st.session_state.current_question

        # 進捗バー
        progress = (current_q / len(QUESTIONS))
        st.progress(progress, text=f"質問 {current_q + 1} / {len(QUESTIONS)}")

        st.divider()

        # 質問表示
        question_data = QUESTIONS[current_q]
        st.subheader(f"質問 {current_q + 1}")
        st.markdown(f"### {question_data['question']}")

        st.write("")  # スペース

        # 選択肢
        for idx, option in enumerate(question_data["options"]):
            if st.button(
                option["text"],
                key=f"q{current_q}_opt{idx}",
                use_container_width=True
            ):
                st.session_state.answers[current_q] = idx

                if current_q < len(QUESTIONS) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.session_state.result_calculated = True
                    st.rerun()

        # 戻るボタン
        if current_q > 0:
            st.divider()
            if st.button("⬅️ 前の質問に戻る"):
                st.session_state.current_question -= 1
                st.rerun()

    # 結果表示
    elif st.session_state.result_calculated:
        sorted_roles = calculate_result()
        top_role = sorted_roles[0][0]
        top_score = sorted_roles[0][1]

        st.success("✨ 診断完了！")
        st.divider()

        # 1位のロール
        role_info = ROLE_DESCRIPTIONS[top_role]
        st.markdown(f"## {role_info['emoji']} あなたにおすすめのロールは...")
        st.markdown(f"# **{role_info['name']}**")

        st.markdown(f"### 説明")
        st.info(role_info['description'])

        st.markdown(f"### おすすめチャンピオン")
        st.markdown(f"🦸 {role_info['champions']}")

        st.divider()

        # 全ロールのスコア
        st.markdown("### 📊 各ロールとの相性")

        for role, score in sorted_roles:
            role_info = ROLE_DESCRIPTIONS[role]
            percentage = (score / max(s for _, s in sorted_roles)) * 100
            st.markdown(f"**{role_info['emoji']} {role_info['name']}**")
            st.progress(percentage / 100)
            st.caption(f"スコア: {score}")
            st.write("")

        st.divider()

        # もう一度診断
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 もう一度診断する", use_container_width=True):
                reset_quiz()
                st.rerun()
        with col2:
            if st.button("🏠 ホームに戻る", use_container_width=True):
                st.switch_page("app.py")

    # フッター
    st.divider()

    # アクセスカウンター表示
    access_count = st.session_state.get('role_total_access_count', 0)
    st.markdown(
        f"""
        <div style='text-align: center; color: #666;'>
            <small>あなたに合ったロールを診断するクイズアプリです</small><br>
            <small>👥 訪問者数: {access_count:,}</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
