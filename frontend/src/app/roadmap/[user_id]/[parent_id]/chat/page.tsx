"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";

import getServerTime from "./getServerTime";
import createChatPost from "./createChatPost";
import createChatRawData from "./createChatRawData";

export default function Chat() {
  const router = useRouter();
  const params = useParams();
  console.log(params.user_id, params.parent_id);
  const [start_time, setStart_time] = useState<string>("");
  const [end_time, setEnd_time] = useState<string>("");

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
      const fetchAndSetEndTime = async () => {
        const server_time = await getServerTime();
        setEnd_time(server_time);
      };
      fetchAndSetEndTime();

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
    }
  }, [savetext]);

  return (
    <main>
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
