"use client";
import { useParams, useRouter } from "next/navigation";
import fetchRoadmapDtails from "./fetchRoadmapDtails";
import itemMap from "../itemMap";
import stateMap from "../stateMap";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function RoadmapDatails() {
  const router = useRouter();
  const params = useParams();
  // console.log(params.user_id, params.parent_id, params.item_name);
  const [roadmapInfo, setRoadmapInfo] = useState([]);
  const [chatSummariesInfo, setChatSummariesInfo] = useState([]);
  const [manualSummariesInfo, setManualSummariesInfo] = useState([]);

  useEffect(() => {
    const fetchAndSetDatas = async () => {
      const Data = await fetchRoadmapDtails(params.parent_id, params.user_id, params.item_name);
      setRoadmapInfo(Data["roadmap"]);
      setChatSummariesInfo(Data["chatsummaries"]);
      setManualSummariesInfo(Data["manualsummaries"]);
    };
    fetchAndSetDatas();
  }, []);

  return (
<<<<<<< HEAD
    <div>
      <Link href={`/roadmap/${params.user_id}/${params.parent_id}`} legacyBehavior>
        <a className="text-blue-600 hover:underline">
          <img src="/Close.svg" alt="Close" style={{ width: "100px", height: "100px" }} />
        </a>
      </Link>
      <br></br>
      <h1>
        <strong>{itemMap[params.item_name]}</strong>
      </h1>
      <p>入力数: {roadmapInfo[0]?.["item_input_num"]}</p>
      <p>状態: {stateMap[roadmapInfo[0]?.["item_state"]]}</p>

      <br></br>
      <h1>手動要約</h1>
      {/* <p>
        manual_summary_id（編集する時に使う）:
        {manualSummariesInfo[0]?.["manual_summary_id"]}
      </p> */}
      <p>{manualSummariesInfo[0]?.["content"]}</p>
      <p>日時:　 {manualSummariesInfo[0]?.["updated_at"]}</p>

      <br></br>
      <br></br>
      <ul>
        {chatSummariesInfo.map((log, index) => (
          <li key={index}>
            {/* <p>chat_summary_id（編集する時に使う）: {log["chat_summary_id"]}</p> */}
            <p>内容:　{log["content"]}</p>
            <p>日時:　{log["created_at"]}</p>
            <br></br>
          </li>
        ))}
      </ul>
=======
    <div className="max-w-4xl mx-auto">
      <div className="w-full max-w-xl p-4 bg-white rounded-lg shadow-md">
        <div className="flex flex-col items-center p-4">
          {" "}
          {/* Changed this line */}
          <Link href={`/roadmap/${params.user_id}/${params.parent_id}`} legacyBehavior>
            <a className="self-start mb-4">
              <img src="/Close.svg" alt="Close" style={{ width: "100px", height: "100px" }} />
            </a>
          </Link>
          <h1 className="text-xl font-bold mb-4">{itemMap[params.item_name]}</h1>
          <p className="text-gray-600">Input Number: {roadmapInfo[0]?.["item_input_num"]}</p>
          <p className="text-gray-600 mb-4">State: {roadmapInfo[0]?.["item_state"]}</p>
          {/* Manual Summaries */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold">Manual Summaries</h2>
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-8 py-5">
                <p className="mt-1 text-sm text-gray-500">Content: {manualSummariesInfo[0]?.["content"]}</p>
                <p className="mt-1 text-sm text-gray-500">Updated At: {manualSummariesInfo[0]?.["updated_at"]}</p>
              </div>
            </div>
          </div>
          {/* AI Summariesの内容 */}
          <ul className="space-y-4">
            <h3 className="text-lg font-semibold">AI Summaries</h3>
            {chatSummariesInfo.map((log, index) => (
              <li key={index} className="bg-gray-100 p-3 rounded-lg">
                <p className="text-gray-800">Content: {log["content"]}</p>
                <p className="text-gray-500">Created At: {log["created_at"]}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
>>>>>>> origin/feature/nishioka/kuroda-test2
    </div>
  );
}
