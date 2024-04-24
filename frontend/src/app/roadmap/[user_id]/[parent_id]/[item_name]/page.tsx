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
    </div>
  );
}
