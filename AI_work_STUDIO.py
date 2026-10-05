import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI


# ============================================================
# 基本設定
# ============================================================

st.set_page_config(
    page_title="AI WORK STUDIO",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI WORK STUDIO")
st.caption("LP分析・改善・HTML自動生成アシスタント")


# ============================================================
# OpenAI接続
# ============================================================

try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)

except Exception:
    st.error("OpenAI APIキーが設定されていません。")
    st.stop()


# ============================================================
# AIに送る共通関数
# ============================================================

def ask_ai(instruction, html):

    prompt = f"""
あなたはLP制作・Webデザイン・コンバージョン改善の専門家です。

【指示】

{instruction}


【現在のHTML】

{html}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text


# ============================================================
# HTMLコードをきれいにする関数
# ============================================================

def clean_html(text):

    text = text.strip()

    if text.startswith("```html"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# ============================================================
# LP入力
# ============================================================

st.divider()

st.header("📝 LPのHTMLを入力")

html = st.text_area(
    "現在使っているLPのHTMLを貼り付けてください",
    height=500,
    placeholder="""<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <title>LP</title>
</head>

<body>

    ここにLPの内容

</body>

</html>"""
)


# ============================================================
# ボタン
# ============================================================

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


# ============================================================
# LP分析
# ============================================================

if analyze_button:

    if not html.strip():

        st.warning(
            "LPのHTMLを貼り付けてください。"
        )

    else:

        with st.spinner(
            "AIがLPを分析しています..."
        ):

            try:

                instruction = """
このLPを
集客・予約率・問い合わせ率の観点から
分析してください。


以下の項目ごとに
日本語で具体的に改善点を出してください。


1. ファーストビュー

2. キャッチコピー

3. 信頼性

4. 料金の見せ方

5. 予約・問い合わせ導線

6. スマートフォン表示

7. SEO

8. 全体構成

9. 成約率を上げるために
   優先して直すべき点


現在の良い部分は残しながら、

改善すべき点を
分かりやすく説明してください。
"""

                analysis_result = ask_ai(
                    instruction,
                    html
                )

                st.session_state[
                    "analysis_result"
                ] = analysis_result


            except Exception as e:

                st.error(
                    f"分析中にエラーが発生しました: {e}"
                )


# ============================================================
# 分析結果表示
# ============================================================

if "analysis_result" in st.session_state:

    st.divider()

    st.subheader(
        "🔍 AI分析結果"
    )

    st.markdown(
        st.session_state[
            "analysis_result"
        ]
    )


# ============================================================
# 改善版HTML生成
# ============================================================

if improve_button:

    if not html.strip():

        st.warning(
            "LPのHTMLを貼り付けてください。"
        )

    else:

        with st.spinner(
            "AIが改善版LPを作成しています..."
        ):

            try:

                instruction = """
以下のHTMLを、

集客と予約につながるLPとして
改善してください。


【重要】

・現在の良い部分は残す

・スマートフォン表示を最優先する

・読みやすくする

・ファーストビューを強くする

・予約や問い合わせにつながる
  導線を分かりやすくする

・CTAボタンを目立たせる

・信頼感のあるデザインにする

・HTMLを途中で省略しない

・DOCTYPEから
  html終了タグまで
  完全なHTMLを出力する

・Markdownの
  ```html
  は付けない

・説明文は不要

・完成したHTMLコードだけを
  出力する
"""


                improved_html = ask_ai(
                    instruction,
                    html
                )


                # Markdownコードブロック除去

                improved_html = clean_html(
                    improved_html
                )


                # 改善版を保存

                st.session_state[
                    "improved_html"
                ] = improved_html


                st.success(
                    "改善版LPが完成しました！"
                )


            except Exception as e:

                st.error(
                    f"改善版作成中にエラーが発生しました: {e}"
                )


# ============================================================
# 改善版LP
# コード・プレビュー・ダウンロード
# ============================================================

if "improved_html" in st.session_state:

    improved_html = st.session_state[
        "improved_html"
    ]


    st.divider()


    # --------------------------------------------------------
    # HTMLコード
    # --------------------------------------------------------

    st.subheader(
        "🚀 改善版LPコード"
    )


    st.code(
        improved_html,
        language="html"
    )


    # --------------------------------------------------------
    # プレビュー
    # --------------------------------------------------------

    st.divider()


    st.subheader(
        "👀 改善版LPプレビュー"
    )


    st.caption(
        "AIが作成した改善版LPを実際の表示で確認できます。"
    )


    components.html(
        improved_html,
        height=800,
        scrolling=True
    )


    # --------------------------------------------------------
    # ダウンロード
    # --------------------------------------------------------

    st.divider()


    st.subheader(
        "📥 改善版LPを保存"
    )


    st.download_button(
        label="⬇️ 改善版HTMLをダウンロード",
        data=improved_html,
        file_name="ayumi_improved_lp.html",
        mime="text/html",
        use_container_width=True
    )


# ============================================================
# 使い方
# ============================================================

st.divider()


st.subheader(
    "💡 使い方"
)


st.markdown(
    """
**STEP 1**

現在使っているLPのHTMLを貼り付ける


**STEP 2**

「🔍 LPをAI分析」を押す


**STEP 3**

改善ポイントを確認する


**STEP 4**

「✨ 改善版HTMLを作る」を押す


**STEP 5**

完成したHTMLを
プレビューしてダウンロードする
"""
)


# ============================================================
# AI追加修正機能
# ============================================================

if "improved_html" in st.session_state:


    st.divider()


    st.header(
        "🤖 AIに追加修正を指示"
    )


    st.caption(
        "現在の改善版LPに、さらに変更したい内容を入力してください。"
    )


    revision_instruction = st.text_area(
        "修正内容",

        placeholder="""例：

もっと高級感のあるデザインにして

LINE予約ボタンをもっと目立たせて

料金を松・竹・梅の3コースにして

ファーストビューをもっと強くして
""",

        height=150
    )


    revise_button = st.button(
        "✨ AIでもう一度修正する",
        use_container_width=True
    )


    # ========================================================
    # 追加修正実行
    # ========================================================

    if revise_button:


        if not revision_instruction.strip():


            st.warning(
                "修正したい内容を入力してください。"
            )


        else:


            with st.spinner(
                "AIがLPを再修正しています..."
            ):


                try:


                    current_html = st.session_state[
                        "improved_html"
                    ]


                    prompt = f"""
あなたは

LP制作・
Webデザイン・
コンバージョン改善

の専門家です。


以下のHTMLは
現在のLPです。


ユーザーの修正指示に従って、

HTML全体を
修正してください。



【修正指示】


{revision_instruction}



【重要】


・現在の良い部分は残す


・スマートフォン表示を重視する


・予約・問い合わせにつながる
  構成にする


・HTMLを途中で省略しない


・DOCTYPEから
  html終了タグまで
  完全なHTMLを出力する


・Markdownの
  ```html
  は付けない


・説明文は不要


・完成したHTMLコードだけを
  出力する
"""


                    revised_html = ask_ai(
                        prompt,
                        current_html
                    )


                    # Markdownコードブロック除去

                    revised_html = clean_html(
                        revised_html
                    )


                    # 最新版に更新

                    st.session_state[
                        "improved_html"
                    ] = revised_html


                    st.success(
                        "🎉 AIによる追加修正が完了しました！"
                    )


                    # ========================================
                    # 最新版プレビュー
                    # ========================================

                    st.subheader(
                        "👀 最新版LPプレビュー"
                    )


                    components.html(
                        revised_html,
                        height=800,
                        scrolling=True
                    )


                    # ========================================
                    # 最新版ダウンロード
                    # ========================================

                    st.download_button(
                        label="⬇️ 最新版HTMLをダウンロード",
                        data=revised_html,
                        file_name="ayumi_lp_latest.html",
                        mime="text/html",
                        use_container_width=True
                    )


                except Exception as e:


                    st.error(
                        f"追加修正中にエラーが発生しました: {e}"
                    )
