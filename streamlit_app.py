# streamlit_app.py
import streamlit as st
import requests
import time

st.title('WaveScript!')

prompt = st.text_area("企画の種を入れてください！")



if st.button('WaveScript your idea!'):
    if prompt:
        # prompt = '# 指示内容\n以下で与えられるキーワードをもとにラジオの台本を作成してください。\n\n# キーワード' + prompt
        prompt = "# 指示内容\n以下で与えられるキーワードをもとにラジオの台本を作成してください。\n\n# 出力フォーマット\n台本は【OP】【本編】の2つのセクションに分けてください。それぞれが始まる前にわかりやすいように【OP】【本編】をつけてください。それぞれのセクションは以下で与えられる説明に従ってください。\n\n# 【OP】の説明\n【OP】セクションは全体の一番最初に配置してください。\n​「​おはようございます！\n東大放研がお送りする「東大もっとラジオ暮らし」のお時間です！\n本日のお相手は{出演者の名前}です。よろしくお願いします」\nから始まるようにしてください。\n\n# 【本編】の説明\nこのラジオ番組の本編部分です。企画内容がわかるように具体的に、1000字程度記述してください。この番組のエンディングに相当するものは別で書き加えるので記述する必要はありません。\n\n# キーワード\n" + prompt + '\n\n# パラメータ\nfrequency_penalty:-2.0, n:1, presence_penalty:-2.0, temperature:0.1'
        response = requests.post('http://127.0.0.1:8000/generate_script', json={'prompt': prompt})
        with st.spinner('WaveScripting...'):
            time.sleep(3)
        # response_json = response.json()
        if response.status_code == 200:
            script = response.json().get('script', 'No script generated')
            script = script[4:]
            script = script.split('【本編】')
            st.write("#### 【OP】")
            st.write(script[0])
            st.write("#### 【本編】")
            st.write(script[1])
            st.write("#### 【ED】")
            st.write('名残惜しいですがお別れのお時間です。\n（感想をふったりフリートークしたりしても）\n\n最後にお知らせです。\n今回の放送は次の月曜日から1週間、番組HPからお聞きいただけます。\n一部の放送回は、公式YouTubeチャンネルにて配信しております。\nさらに詳しい情報はX、旧ツイッターアカウント@toudaihouken(ｱｯﾄﾏｰｸ ﾄｳﾀﾞｲﾎｳｹﾝ)全て小文字のローマ字で@tou dai hou ken(ｱｯﾄﾏｰｸ ﾃｨｰｵｰﾕｰ ﾃﾞｨｰｴｰｱｲ ｴｲﾁｵｰﾕｰ ｹｰｲｰｴﾇ)で随時更新しておりますので是非ご確認ください。\n\n本日のお相手は〜でした。\nそれではまた来週同じ時間にお会いしましょう！\nありがとうございました！')
        else:
            st.write('生成に失敗しました エラーコード:', response.status_code)
            st.write('詳細エラーメッセージ:', response.text)
    else:
        st.write("企画を入力してください")