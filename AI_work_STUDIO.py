import streamlit as st
from openai import OpenAI

# =========================================================
# 基本設定
# =========================================================

st.set_page_config(
    page_title="AI WORK STUDIO",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI WORK STUDIO")
st.caption("LP分析・改善・HTML自動生成アシスタント")


# =========================================================
# OpenAI接続
# =========================================================

try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("OpenAI APIキーが設定されていません。")
    st.stop()


# =========================================================
# AIへ送る共通処理
# =========================================================

def ask_ai(instruction, html):

    response = client.responses.create(
        model="gpt-5.4-mini",
        instructions=instruction,
        input=html
    )

    return response.output_text


# =========================================================
# 入力欄
# =========================================================

st.subheader("① LPのHTMLを貼り付け")

html = st.text_area(
    "分析・改善したいLPのHTMLを貼り付けてください",
    height=400,
    placeholder="""<!DOCTYPE html>
<html>
<head>
...
</head>
<body>
...
</body>
</html>"""
)


# =========================================================
# ボタン
# =========================================================

col1, col2 = st.columns(2)

with col1:
    analyze_button = st.button(
        "🔍 LPをAI分析",
        use_container_width=True
    )

with col2:
    improve_button = st.button(
        "✨ 改善版HTMLを作る",
        use_container_width=True
    )


# =========================================================
# AI分析
# =========================================================

if analyze_button:

    if not html.strip():

        st.warning("HTMLを貼り付けてください。")

    else:

        with st.spinner("AIがLPを分析しています..."):

            try:

                instruction = """
あなたは日本トップクラスの
LPマーケター・コピーライター・Web制作責任者です。

入力されたLPのHTMLを分析してください。

目的は
「見た目を褒めること」ではなく
「問い合わせ・予約・購入を増やすこと」です。

次の項目を100点満点で評価してください。

1. ファーストビュー
2. キャッチコピー
3. ターゲットの明確さ
4. ベネフィット
5. 信頼性
6. CTA
7. スマートフォンでの見やすさ
8. 不安解消
9. 料金・オファー
10. 成約導線

最初に

【総合点】
○○ / 100点

と表示してください。

その後、

【良いところ】

【重大な問題点】

【最優先で直す3項目】

【具体的な改善案】

【おすすめキャッチコピー】

【CTA改善案】

【成約率を上げるために追加すべき要素】

の順番で回答してください。

抽象論ではなく、
実際にLPを書き換えられるレベルまで
具体的に提案してください。

医療・健康関連LPの場合は、
誇大表現や効果を保証する表現にも注意してください。
"""

                result = ask_ai(instruction, html)

                st.success("分析完了")

                st.subheader("📊 AI分析結果")

                st.markdown(result)

            except Exception as e:

                st.error(f"エラーが発生しました：{e}")


# =========================================================
# 改善HTML生成
# =========================================================

if improve_button:

    if not html.strip():

        st.warning("HTMLを貼り付けてください。")

    else:

        with st.spinner(
            "AIが成約率を意識した改善版LPを作っています..."
        ):

            try:

                instruction = """
あなたはトップクラスの
LPマーケター、コピーライター、
UI/UXデザイナー、Webエンジニアです。

入力されたLPのHTMLを分析して、
問い合わせ・予約・購入につながりやすい
改善版HTMLを作成してください。

重要条件：

・元LPの良い部分は残す
・ファーストビューを強化
・誰向けのサービスか明確にする
・ベネフィットを分かりやすくする
・CTAを強化
・スマートフォン最優先
・読みやすい余白
・料金を分かりやすくする
・FAQを改善
・信頼性を高める
・問い合わせまでの導線を短くする
・不自然な煽り表現は禁止
・存在しない口コミや実績を捏造しない
・医療効果を保証しない
・元HTMLに存在しない資格や実績を勝手に追加しない

特に重要：

ユーザーがそのまま保存して使える
完全なHTMLを生成してください。

<!DOCTYPE html>
から
</html>
まで省略せず生成してください。

説明文をHTMLの前後に付けず、
完成したHTMLコードだけを出力してください。
"""

                improved_html = ask_ai(
                    instruction,
                    html
                )

                # Markdownコードブロックが付いた場合に除去
                improved_html = improved_html.strip()

                if improved_html.startswith("```html"):
                    improved_html = improved_html[7:]

                elif improved_html.startswith("```"):
                    improved_html = improved_html[3:]

                if improved_html.endswith("```"):
                    improved_html = improved_html[:-3]

                improved_html = improved_html.strip()

                st.success("改善版LPが完成しました！")

                st.subheader("🚀 改善版LPコード")

                st.code(
                    improved_html,
                    language="html"
                )

                st.divider()

                st.subheader("👀 改善版LPプレビュー")

                st.caption("AIが作成した改善版LPを実際の表示で確認できます。")

                st.components.v1.html(
                    improved_html,
                    height=800,
                    scrolling=True
                 )

                st.divider()                
                
                st.download_button(
                    label="⬇️ 改善版HTMLをダウンロード",
                    data=improved_html,
                    file_name="improved_lp.html",
                    mime="text/html",
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"エラーが発生しました：{e}")


# =========================================================
# 使い方
# =========================================================

st.divider()

st.subheader("💡 使い方")

st.markdown("""
**STEP 1**  
現在使っているLPのHTMLを貼り付ける

**STEP 2**  
「🔍 LPをAI分析」を押す

**STEP 3**  
改善ポイントを確認する

**STEP 4**  
「✨ 改善版HTMLを作る」を押す

**STEP 5**  
完成したHTMLをダウンロードする
""")
# ==========================================================
# 改善版LP プレビュー・ダウンロード
# ==========================================================

if "improved_html" in st.session_state:

    improved_html = st.session_state["improved_html"]

    st.divider()

    st.subheader("👀 改善版LPプレビュー")

    st.caption("AIが作成した改善版LPを実際の表示で確認できます。")

    # プレビュー表示
    st.components.v1.html(
        improved_html,
        height=800,
        scrolling=True
    )

    st.divider()

    st.subheader("📥 改善版LPを保存")

    st.download_button(
        label="⬇️ 改善版HTMLをダウンロード",
        data=improved_html,
        file_name="ayumi_improved_lp.html",
        mime="text/html",
        use_container_width=True
    )
