"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";

import getServerTime from "./getServerTime";
import createChatPost from "./createChatPost";
import createChatRawData from "./createChatRawData";
import getChatlogSmall from "./getChatlogSmall";

export default function Chat() {
  const router = useRouter();
  const params = useParams();
  // console.log(params.user_id, params.parent_id);
  const [start_time, setStart_time] = useState<string>("");
  const [end_time, setEnd_time] = useState<string>("");
  const [chatlogInfo, setChatlogInfo] = useState([]);
  const [postComplete, setPostComplete] = useState(false); //投稿が完了したことを検出
  const [postCount, setPostCount] = useState<number>(0); //投稿階数　履歴を取得する

  const [isRecording, setIsRecording] = useState(false);
  const [text, setText] = useState<string>("");
  const [transcript, setTranscript] = useState<string>("");
  const [savetext, setSaveText] = useState<string>("");
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
      // 記録開始時間の取得
      const fetchAndSetStartTime = async () => {
        const server_time = await getServerTime();
        setStart_time(server_time);
      };
      fetchAndSetStartTime();
      // 録音開始
      recognition.start();
    } else {
      // true->falseの時の処理
      // 録音を停止
      recognition.stop();
      // 記録停止時間の取得

      // 発話が止まっている時に停止ボタンを押すとここで終了時間を記録
      if (savetext !== "") {
        const fetchAndSetEndTime = async () => {
          const server_time = await getServerTime();
          setEnd_time(server_time);
        };
        fetchAndSetEndTime();
      }
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
          setSaveText(results[i][0].transcript);
          setTranscript("");
        } else {
          setTranscript(results[i][0].transcript);
        }
      }
    };
  }, [recognition]);

  // 認識結果が確定した時(savetext)にその内容をバックエンドへ送る
  useEffect(() => {
    if (savetext == "") return;
    else {
      //結果をバックエンドへ送りたい
      const fetchChatRawDatas = async () => {
        const values = {
          parent_user_id: params.parent_id,
          child_user_id: params.user_id,
          content: savetext,
        };
        createChatRawData(values);
      };
      fetchChatRawDatas();
      console.log(text + "何が表示されているでしょうか");

      //発話中に終了ボタンを押したときはこちらの処理
      // 録音が終了した時にtext=""となっているので終了時間を取得する
      if (!isRecording) {
        const fetchAndSetEndTime = async () => {
          const server_time = await getServerTime();
          setEnd_time(server_time);
        };
        fetchAndSetEndTime();
        setText("");
      }
    }
  }, [savetext]);

  useEffect(() => {
    if (start_time < end_time) {
      // 録音内容をChatPostsへ保存
      const fetchChatPost = async () => {
        const values = {
          parent_user_id: params.parent_id,
          child_user_id: params.user_id,
          recording_start_datetime: start_time,
          recording_end_datetime: end_time,
        };
        // console.log(values);
        console.log(postCount + "投稿直前");
        const flag = await createChatPost(values);
        // setPostCount(postCount + 1); //投稿数をカウントアップ
        setPostComplete(flag); // 投稿完了を確認
        // console.log(postCount + "投稿直後");
      };
      fetchChatPost();
      setSaveText(""); //投稿する内容を初期化する
    }
  }, [end_time]);

  // 投稿が完了された時に、postCountを増やして、会話履歴を取得する
  useEffect(() => {
    if (postComplete) {
      setPostCount((prevCount) => prevCount + 1);
      console.log(postCount + "投稿時点");
      setPostComplete(false); // 投稿フラグを未完了に戻す
    } else {
      return;
    }
  }, [postComplete]);

  // 投稿が完了された時に、postCountを増やして、会話履歴を取得する
  useEffect(() => {
    if (postCount > 0) {
      const fetchGetChatlogSmall = async () => {
        // setPostCount((prevCount) => prevCount + 1);
        console.log(postCount + "投稿時点");
        const values = {
          parent_user_id: params.parent_id,
          child_user_id: params.user_id,
          count: postCount, //取得する最大履歴
        };
        const data = await getChatlogSmall(values);
        await setChatlogInfo(data);
      };
      fetchGetChatlogSmall();
    } else {
      return;
    }
  }, [postCount]);

  return (
    <main>
      <div>
        <h1>Chat Log</h1>
        <ul>
          {chatlogInfo.map((log, index) => (
            <li key={index}>
              <p>Posted by: {log.post_user}</p>
              <p>Created At: {log.chatpost_created_at}</p>
              <p>
                Content: <strong>{log.content}</strong>
              </p>
              <br></br>
            </li>
          ))}
        </ul>
      </div>
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
    </main>
  );
}
