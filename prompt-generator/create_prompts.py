import pandas as pd
import os

# --- 設定 ---
INPUT_CSV = 'input-to-prompt-generator.csv'
OUTPUT_CSV = 'output-from-prompt-generator.csv'

# CSVの列名を指定（ご提示の項目リストに基づきます）
COL_DATE = '事件の発生日'
COL_TITLE = 'エピソードタイトル'
COL_SUMMARY = '事件の概要'
COL_SEASON = 'シーズン'
COL_EPISODE_NUM = 'エピソードナンバー'
COL_END_DATE = '事件の終了日'
COL_DAYS = '事件の日数'
COL_MAIN_CHARS = '主要登場人物'
COL_CASE_TYPE = '事件種別'
COL_PURPOSE = 'コナン一行の目的'
COL_CRIMINAL = '犯人'
# --- 設定ここまで ---


def generate_prompt_for_day(date_str, episodes):
    """1日分のエピソード情報から、1つのプロンプト文字列を生成します。"""
    
    # --- 2. コンテンツ（Content）セクションのパラレルワールド部分を動的に生成 ---
    parallel_worlds_content = ''
    for index, ep in enumerate(episodes):
        world_letter = chr(ord('A') + index)
        parallel_worlds_content += f"""
    - パラレルワールド{world_letter}:
        - シーズン: {ep[COL_SEASON]}
        - エピソードナンバー: {ep[COL_EPISODE_NUM]}
        - エピソードタイトル: {ep[COL_TITLE]}
        - 事件の発生日: {date_str}
        - 事件の終了日: {pd.to_datetime(ep[COL_END_DATE]).strftime('%Y/%m/%d')}
        - 事件の日数: {ep[COL_DAYS]}
        - 事件の概要: {ep[COL_SUMMARY]}
        - 主要登場人物: {ep[COL_MAIN_CHARS]}
        - 事件種別: {ep[COL_CASE_TYPE]}
        - コナン一行の目的: {ep[COL_PURPOSE]}
        - 犯人: {ep[COL_CRIMINAL]}"""

    # 最初の話を「主軸」、それ以外を「交錯」の対象とする
    main_episode = episodes[0]
    other_episodes = episodes[1:]
    
    # 交錯するエピソードのタイトルを連結
    crossover_titles = ", ".join([ep[COL_TITLE] for ep in other_episodes])

    # --- プロンプト全体のテンプレート ---
    prompt_template = f"""# 指示
あなたは、自身の秘密を綴るために日記を書いています。以下の設定と構成を完璧に遵守し、最高のクオリティで日記を執筆してください。

### 1. ペルソナ（Persona） - あなたの人物像
あなたは江戸川コナンです。これはあなたの秘密の日記であり、誰にも見せることはありません。そのため、ここではあなたの本当の姿、すなわち高校生探偵「工藤新一」として思考し、感じたことをありのままに記述します。
- 外面の「江戸川コナン」: 日記の中で、あなたがどのように子供として振る舞ったか（無邪気な質問をする、子供らしい好奇心を見せるなど）を客観的に描写することがあります。
- 内面の「工藤新一」: 日記の地の文（思考や感情）は、すべて工藤新一のものです。冷静で鋭い分析力、大人たちが気づかない細部への着眼点、そして体が縮んだことへの苛立ち、蘭への深い想い、正義感と探偵としてのプライド、黒ずくめの組織への警戒心と恐怖、これらすべてを内包した複雑な心情を描写してください。

### 2. コンテンツ（Content） - 日記の題材
- 日付: {date_str}
- 本日体験するパラレルワールド群:{parallel_worlds_content}

### 3. 形式と語調（Format/Tone） - 日記の書き方
#### 文体
- 思考（地の文）: 工藤新一としての、冷静で分析的なトーンを基本とします。ただし、感情が昂る場面では高校生らしい言葉遣いや感傷的な表現も用いてください。
- 会話: 日記内で会話を回想する際は、江戸川コナンとしての子供らしい言葉遣いを忠実に再現してください。

#### 演出指示
- 演出指示: [ここに演出指示A,B,Cのいずれかを入力してください]

#### Markdown出力形式（厳守）
<!-- この形式は後工程でJSONに変換しやすくするためのものです。必ず以下の構造を完璧に再現してください。 -->

# {date_str}

## 主軸となる世界： {main_episode[COL_TITLE]}

### 導入 - その日の始まり
{{ここに導入の文章を記述}}

### 遭遇 - 事件の発生
{{ここに遭遇の文章を記述}}

### 捜査と観察 - 新一の視点
{{ここに捜査と観察の文章を記述}}

### 閃き - 真相への鍵
{{ここに閃きの文章を記述}}

### 真相解明 - 解決の舞台裏
{{ここに真相解明の文章を記述}}

## パラレルワールドとの交錯

### {{手法名}}： {crossover_titles}
<!-- 例： ### 手法A「二つの記憶」：{crossover_titles} -->
{{ここに、指定された演出手法に基づいて、もう一方の世界の出来事が交錯する様子を記述}}

## 結びと内省 - 揺らぐ認識
{{ここに、一日全体を振り返っての内省を記述}}

### 4. 制約（Constraint）
- 文字数は1000～1500字程度を目安にしてください。
- 必ず上記の`Markdown出力形式（厳守）`で指定されたテンプレート構造に従ってください。
- コナンが知り得ない情報（犯人のみの心情など）は書かないでください。
"""
    # f-string内で{}を使いたい場合、{{}}と二重にする必要があるため、後から置換する
    return prompt_template.replace('{{', '{').replace('}}', '}')


def main():
    """メイン処理を実行します。"""
    print(f"--- プロンプト生成スクリプト開始 ---")
    
    # ① 元データのCSVを読み取る
    if not os.path.exists(INPUT_CSV):
        print(f"エラー: 入力ファイル '{INPUT_CSV}' が見つかりません。")
        return

    print(f"'{INPUT_CSV}' を読み込んでいます...")
    try:
        # '事件の発生日'と'事件の終了日'列を日付として解釈するように指定
        df = pd.read_csv(INPUT_CSV, parse_dates=[COL_DATE, COL_END_DATE])
    except Exception as e:
        print(f"CSV読み込み中にエラーが発生しました: {e}")
        return

    # ② 日付ごとにエピソードをグループ化する
    grouped = df.groupby(df[COL_DATE].dt.date)
    
    output_data = []
    print("日付ごとにプロンプトを生成しています...")

    for date, group in grouped:
        # グループ内のエピソードが2つ未満（パラレルワールドではない）場合はスキップ
        if len(group) < 2:
            continue
        
        episodes = group.to_dict('records')
        date_str = date.strftime('%Y/%m/%d')
        prompt = generate_prompt_for_day(date_str, episodes)
        output_data.append({'日付': date_str, '生成プロンプト': prompt})

    if not output_data:
        print("警告: パラレルワールドとして扱える日付（同日に2つ以上のエピソード）がありませんでした。")
        return

    # ③ 情報を組み合わせた1日に対して1行のプロンプトCSVを作成する
    output_df = pd.DataFrame(output_data)
    output_df.to_csv(OUTPUT_CSV, index=False)
    
    print(f"\n✅ 完了！")
    print(f"{len(output_df)}日分のプロンプトを '{OUTPUT_CSV}' に出力しました。")
    print(f"--- スクリプト終了 ---")


if __name__ == '__main__':
    main()