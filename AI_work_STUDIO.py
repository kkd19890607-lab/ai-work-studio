import os
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

st.set_page_config(
    page_title="AI WORK STUDIO",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI WORK STUDIO")
st.caption("OpenAI連携・LP分析＆改善アシスタント")

# APIキー確認
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI APIキーが設定されていません。")
    st.stop()

client = OpenAI(api_key=api_key)

st.subheader("LPのHTMLを貼り付け")

html = st.text_area(
    "分析・改善したいLPのHTMLを貼り付けてください",
    height=400,
    placeholder="ここに <!DOCTYPE html> から </html> まで貼り付けます"
)

col1, col2 = st.columns(2)

with col1:
    analyze = st.button(
        "🔍 LPをAI分析",
        use_container_width=True
    )

with col2:
    improve = st.button(
        "✨ 改善版HTMLを作る",
        use_container_width=True
    )

if analyze:

    if not html.strip():
        st.warning("LPのHTMLを貼り付けてください。")

    else:
        with st.spinner("AIがLPを分析しています..."):

            prompt = f"""
あなたはLP改善・Webマーケティング・コピーライティングの専門家です。

以下のLPを分析してください。

特に次の項目を評価してください。

1. ファーストビュー
2. ターゲットへの訴求力
3. 信頼性
4. LINE予約への導線
5. CTAの強さ
6. 料金表示
7. スマートフォンでの読みやすさ
8. SEO
9. コンバージョン率改善
10. 医療・美容系LPとして誤解を招きやすい表現

100点満点で採点してください。

その後、

【最優先で直すところ】
【改善すると予約率が上がりそうなところ】
【良いところ】
【具体的な修正文】

の順番で、日本語で分かりやすく回答してください。

LP HTML:

{html}
"""

            try:
                response = client.responses.create(
                    model="gpt-5.6-luna",
                    input=prompt
                )

                st.success("分析完了！")
                st.markdown(response.output_text)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")


if improve:

    if not html.strip():
        st.warning("LPのHTMLを貼り付けてください。")

    else:
        with st.spinner("改善版LPを作成しています..."):

            prompt = f"""
あなたはプロのWebマーケター兼フロントエンドエンジニアです。

以下のLPを改善してください。

目的は問い合わせ・LINE予約率を高めることです。

条件：

・元のデザインの良い部分は残す
・スマートフォン最優先
・ファーストビューを強化
・LINE予約導線を改善
・信頼性を高める
・読みやすくする
・過度な効果保証や断定表現を避ける
・存在が確認できない口コミ、資格、経歴、実績を新しく作らない
・HTML全体を完成形で出力する
・説明文は不要
・最初から最後までHTMLだけを出力する

元のHTML:

{html}
"""

            try:
                response = client.responses.create(
                    model="gpt-5.6-luna",
                    input=prompt
                )

                improved_html = response.output_text
                st.session_state["improved_html"] = improved_html

                # Markdownコードブロックが付いた場合に除去
                improved_html = improved_html.replace(
                    "```html", ""
                ).replace(
                    "```", ""
                ).strip()

                st.success("改善版HTMLが完成しました！")

                st.download_button(
                    "💾 改善版HTMLを保存",
                    data=improved_html,
                    file_name="improved_lp.html",
                    mime="text/html",
                    use_container_width=True
                )

                with st.expander("改善版HTMLを見る"):
                    st.code(improved_html, language="html")

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

st.divider()
st.subheader("👀 改善版LPをプレビュー")

if "improved_html" in st.session_state:
    components.html(
        st.session_state["improved_html"],
        height=800,
        scrolling=True
    )
else:
    st.info("「✨ 改善版HTMLを作る」を押すと、ここにLPが表示されます。")


# ==================================================
# 広告効果分析
# ==================================================

st.divider()
st.header("📊 広告効果分析")

st.write("毎月の広告データを入力すると、広告効果を自動計算します。")

ad_cost = st.number_input(
    "広告費（円）",
    min_value=0,
    value=30000,
    step=1000
)

lp_views = st.number_input(
    "LP閲覧数",
    min_value=0,
    value=0,
    step=1
)

line_clicks = st.number_input(
    "LINEクリック数",
    min_value=0,
    value=0,
    step=1
)

inquiries = st.number_input(
    "問い合わせ数",
    min_value=0,
    value=0,
    step=1
)

reservations = st.number_input(
    "新規予約数",
    min_value=0,
    value=0,
    step=1
)

sales = st.number_input(
    "広告経由の売上（円）",
    min_value=0,
    value=0,
    step=1000
)

if st.button("📈 広告効果を計算"):

    st.subheader("分析結果")

    if reservations > 0:
        cpa = ad_cost / reservations
        st.metric("1予約あたり広告費（CPA）", f"{cpa:,.0f}円")
    else:
        st.metric("1予約あたり広告費（CPA）", "予約なし")

    if lp_views > 0:
        line_rate = line_clicks / lp_views * 100
        st.metric("LP → LINEクリック率", f"{line_rate:.1f}%")

    if inquiries > 0:
        reservation_rate = reservations / inquiries * 100
        st.metric("問い合わせ → 予約率", f"{reservation_rate:.1f}%")

    if ad_cost > 0:
        roas = sales / ad_cost * 100
        st.metric("ROAS（広告費に対する売上）", f"{roas:.0f}%")

        if roas >= 300:
            st.success("🟢 広告効率はかなり良好です。広告費増額を検討できます。")
        elif roas >= 200:
            st.success("🟢 広告は良い状態です。継続しながら改善しましょう。")
        elif roas >= 100:
            st.warning("🟡 売上は広告費を上回っていますが、改善余地があります。")
        else:
            st.error("🔴 広告費が売上を上回っています。LP・広告・予約導線を見直しましょう。")
