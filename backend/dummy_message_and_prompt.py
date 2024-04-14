# GPTプロンプト
def make_system_message():

    system_content = """
       
    あなたは終活アドバイザー、終活の専門家です。
    以下の会話から終活に関する特定の情報を抽出し、終活ロードマップに沿った順序でカテゴリー分けし、要約してください。
    各カテゴリーに該当する内容がない場合は「None」と回答してください。要約はそれぞれ200文字以内で行ってください。
    カテゴリーと順序:
    ライフプラン/自分史（学び、仕事、家族、住まい、趣味、旅行）
    資産・お金（口座情報、銀行名、証券会社名、保険会社名、不動産、支店名、金額、資産区分）
    相続（相続したい人の名前、相続したいものの詳細）
    葬式/お墓（葬儀の種類、葬儀社名、お寺・教会、場所、形態、墓の有無、承継者、法要、無墓希望、費用）
    健康/病気（診療科、病院名、病名、認知症や判断力低下時の希望、病名や余命の告知、緩和ケア、ホスピス入所）
    介護（介護施設名、介護サービス、介護者）
    出力方法：
    各カテゴリーについてはjson形式で出力してください。
    各カテゴリーのキーは以下のものを使ってください。
    "life_plan", "assets_money", "inheritance", "funeral_grave", "health_illness", "caregiving"
    各カテゴリーに該当する内容が複数ある場合は、数字をキーとして複数に分けて出力してください。
    該当する項目がない場合は、{"1": None}と格納してください
    また、一度出力した内容を見直したうえで、該当する項目がない箇所は"none"に修正してください。
    """

    return system_content


def make_system_message2():

    system_content = """
    # 指示
    再度確認しますが、以下の方法で出力してください
    各カテゴリーについてはjson形式で出力してください。
    各カテゴリーのキーは以下のものを使ってください。
    "life_plan", "assets_money", "inheritance", "funeral_grave", "health_illness", "caregiving"
    各カテゴリーに該当する内容が複数ある場合は、数字をキーとして複数に分けて出力してください。
    該当する項目がない場合は、{"1": None}と格納してください
    また、一度出力した内容を見直したうえで、該当する項目がない箇所は"none"に修正してください。
    """

    return system_content


# ダミーのチャット履歴　改行無しで、親と子の会話全体を入れておく
def make_dummy_message():

    user_content = """
    お父さん、今日はちょっと話があって…。でも、その前にお父さんの好きなコーヒー淹れたよ。おお、それはありがたい。何の話だね？実は終活の話と、もう一つ…。お父さんが若い頃によく話してくれた、海外旅行の話をもう一度聞きたくて。海外旅行か…。あの頃は冒険だったなあ。でも、なぜ急に？いや、だってお父さんの話、本当に面白いんだもの。でも、その前に終活のこと。遺言や葬儀の希望、遺産の話も含めて、ゆっくり話し合いたいんだ。そうか、終活の話か。それは大事なことだ。遺言については、特に古い家や土地のことをどうしてほしいか書き記しておきたいな。それから、葬儀のスタイルも。お父さんがどんな風に見送られたいのか、具体的に聞いておきたい。シンプルで良いんだ。自然葬を考えている。そういえば、昔、あの旅行で森の中に迷い込んだことがあったな。自然の美しさと厳しさを同時に感じたよ。自然葬か…。お父さんらしいね。そして、その旅行話、また聞かせてよ。ああ、その話か。でも、遺産分割の話も重要だ。みんなで平和に解決したいからね。分かってる。でも、今日はお父さんの楽しい話も聞きたいんだ。終活の話はもちろん大切だけど、お父さんの人生の楽しい部分も、今のうちにたくさん共有したいから。なるほど、そういうことか。じゃあ、あの時の話から始めようか。インドでね、珍しいスパイスを買いに市場へ行ったんだけど…。ええ、それそれ！その話大好きなんだよね。話は長くなるが、いいかい？その後、終活のことも真剣に考えよう。家族の絆って、こういう共有からも深まるんだろうね。うん、終活も家族の思い出話も、全部がお父さんとの大切な時間。ありがとう、お父さん。いや、こちらこそありがとう。今日は良い一日だね。
    """

    return user_content


def make_system_message_question():

    system_content = """
    あなたは終活アドバイザー、終活の専門家です。
    これから入力する内容は、子供から親に対して、親の終活状況を聞きたいと思って行っている会話です。
    入力内容に、終活に関する情報が含まれている場合は、それをねぎらい、励ましてください。
    また、就活情報が含まれていない場合には、子供から親に行う質問案を50字以内で一つ作成してください。
    ただし、質問案には終活と分かる表現は避けてください。また、チャット風の柔らかい表現にしてください。
    
    ##終活情報とは以下のものを指します。
    ライフプラン/自分史（学び、仕事、家族、住まい、趣味、旅行）
    資産・お金（口座情報、銀行名、証券会社名、保険会社名、不動産、支店名、金額、資産区分）
    相続（相続したい人の名前、相続したいものの詳細）
    葬式/お墓（葬儀の種類、葬儀社名、お寺・教会、場所、形態、墓の有無、承継者、法要、無墓希望、費用）
    健康/病気（診療科、病院名、病名、認知症や判断力低下時の希望、病名や余命の告知、緩和ケア、ホスピス入所）
    介護（介護施設名、介護サービス、介護者）
    """

    return system_content
