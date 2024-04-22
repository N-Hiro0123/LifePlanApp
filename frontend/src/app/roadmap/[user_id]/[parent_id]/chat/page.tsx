"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";

import getServerTime from "./getServerTime";
import createChatPost from "./createChatPost";
import createChatText from "./createChatText"; //テキストの投稿はこれだけを使う
import createChatPostGPT from "./createChatPostGPT";
import createChatRawData from "./createChatRawData";
import createGPTSummary from "./createGPTSummary";
import getChatlogSmall from "./getChatlogSmall";
import Link from "next/link";

export default function Chat() {
  const router = useRouter();
  const params = useParams();
  // console.log(params.user_id, params.parent_id);
  const [chatlogInfo, setChatlogInfo] = useState([]);
  const [postComplete, setPostComplete] = useState(false); //投稿が完了したことを検出
  const [postGPTComplete, setPostGPTComplete] = useState(false); //GPTの投稿が完了したことを検出
  const [postCount, setPostCount] = useState<number>(0); //投稿階数　履歴を取得する
  const [summaryInfo, setSummaryInfo] = useState([]); //要約結果を保存

  const [isRecording, setIsRecording] = useState(false);
  const [text, setText] = useState<string>("");
  const [transcript, setTranscript] = useState<string>("");
  const [savetext, setSaveText] = useState<string>(""); //投稿するテキスト
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(
    null
  );

  useEffect(() => {
    if (typeof window !== "undefined") {
      // このブロックのコードは、windowオブジェクトが存在する（つまりブラウザ環境で実行されている）場合にのみ実行されます
      const recognition = new webkitSpeechRecognition();
      recognition.lang = "ja-JP";
      recognition.continuous = true;
      recognition.interimResults = true;
      setRecognition(recognition);
    }
  }, []);

  useEffect(() => {
    if (!recognition) return;
    if (isRecording) {
      // false->tureの時の処理
      // 録音開始
      recognition.start();
    } else {
      // true->falseの時の処理
      // 録音を停止
      recognition.stop();
      // text内容を保存する場所に渡す
      setSaveText(text);
      // textを初期化
      setText("");
    }
  }, [isRecording]);

  useEffect(() => {
    if (!recognition) return;
    recognition.onresult = (event) => {
      const results = event.results;
      for (let i = event.resultIndex; i < results.length; i++) {
        if (results[i].isFinal) {
          setText((prevText) => prevText + results[i][0].transcript);
          setTranscript("");
        } else {
          setTranscript(results[i][0].transcript);
        }
      }
    };
  }, [recognition]);

  // 送信ボタンを押したときに投稿＆GPTから返答もらう
  const handleSubmit_post = async (event) => {
    event.preventDefault();

    const fetchChatText = async () => {
      const values = {
        parent_user_id: params.parent_id,
        child_user_id: params.user_id,
        content: savetext,
      };
      const res = await createChatText(values);
      setPostComplete(res);
    };

    fetchChatText(); //テキストの投稿
    setSaveText(""); //初期化
    setPostCount((prevCount) => prevCount + 1); // 投稿階数を＋１
  };

  // 投稿が完了された時に、GPT応答を生成しつつpostCountを増やす
  useEffect(() => {
    if (postComplete) {
      const fetchPostGPT = async () => {
        const values = {
          parent_user_id: params.parent_id,
          child_user_id: params.user_id,
          count: postCount, //取得する最大履歴
        };
        const res = await createChatPostGPT(values);
        setPostGPTComplete(res);
      };
      fetchPostGPT();
      setPostCount((prevCount) => prevCount + 1); //GPT分のカウントを増やす
    } else {
      return;
    }
  }, [postComplete]);

  // 投稿もしくはGPT投稿が完了された時に会話履歴を取得する
  useEffect(() => {
    if (postComplete || postGPTComplete) {
      const fetchGetChatlogSmall = async () => {
        const values = {
          parent_user_id: params.parent_id,
          child_user_id: params.user_id,
          count: postCount, //取得する最大履歴
        };
        const data = await getChatlogSmall(values);
        await setChatlogInfo(data);
      };
      fetchGetChatlogSmall();
      setPostComplete(false);
      setPostGPTComplete(false);
    } else {
      return;
    }
  }, [postComplete, postGPTComplete]);

  // 要約ボタンを押したときに要約するとともに画面遷移する
  const handleSubmit_summary = async (event) => {
    event.preventDefault();

    const fetchGPTSuumary = async () => {
      const values = {
        parent_user_id: params.parent_id,
        child_user_id: params.user_id,
        count: postCount,
      };
      const data = await createGPTSummary(values);
      setSummaryInfo(data); // 一応、要約結果を格納しておく　確認画面を作成する場合はこれを使う
    };
    await fetchGPTSuumary(); //要約の実施
    router.push(`./`); //ロードマップの画面に戻る
  };

  return (
    <main>
      {/* 以下、会話履歴表示部 */}
      <div>
        <Link href={`/roadmap/${params.user_id}/${params.parent_id}`}>
          <p>
            <strong>ロードマップ画面へ</strong>
          </p>
        </Link>
        <h1>履歴</h1>
        <ul>
          {chatlogInfo.map((log, index) => (
            <li key={index}>
              <p>Posted by: {log.role}</p>
              <p>Created At: {log.chatpost_created_at}</p>
              <p>
                Content: <strong>{log.content}</strong>
              </p>
              <br></br>
            </li>
          ))}
        </ul>
      </div>
      {/* 以下、音声認識ボタン */}
      <button
        onClick={() => {
          setIsRecording((prev) => !prev);
        }}
      >
        {isRecording ? "停止" : "録音開始"}
      </button>
      <div>
        <p>途中経過：{transcript}</p>
        <p>解析：{text}</p>
      </div>
      {/* 以下、メッセージ投稿ボタン */}
      <div>
        <h1>メッセージ送信フォーム</h1>
        <form onSubmit={handleSubmit_post}>
          <textarea
            value={savetext}
            onChange={(e) => setSaveText(e.target.value)}
            placeholder="メッセージを入力してください"
            rows="4" // 行数を指定
            style={{ width: "100%", height: "150px", overflowY: "auto" }} // スタイル直書き
          />
          <button type="submit">送信</button>
        </form>
      </div>
      <div>
        <button onClick={handleSubmit_summary}>要約</button>
      </div>
    </main>
  );
}
