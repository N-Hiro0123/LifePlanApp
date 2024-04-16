"use client";
import { useParams, useRouter } from "next/navigation";
import fetchRoadmapDtails from "./fetchRoadmapDtails";
import itemMap from "../itemMap";

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
      const Data = await fetchRoadmapDtails(
        params.parent_id,
        params.user_id,
        params.item_name
      );
      setRoadmapInfo(Data["roadmap"]);
      setChatSummariesInfo(Data["chatsummaries"]);
      setManualSummariesInfo(Data["manualsummaries"]);
    };
    fetchAndSetDatas();
  }, []);

  return (
    <div>
      <Link href={`/roadmap/${params.user_id}/${params.parent_id}`}>
        <p>
          <strong>Roadmap**link**</strong>
        </p>
      </Link>
      <br></br>
      <h1>{itemMap[params.item_name]}</h1>
      <h1>Roadmap</h1>
      <p>input_num: {roadmapInfo[0]?.["item_input_num"]}</p>
      <p>state: {roadmapInfo[0]?.["item_state"]}</p>

      <br></br>
      <h1>Manual Summaries</h1>
      {/* <p>
        manual_summary_id（編集する時に使う）:
        {manualSummariesInfo[0]?.["manual_summary_id"]}
      </p> */}
      <p>input_num: {manualSummariesInfo[0]?.["content"]}</p>
      <p>update_at: {manualSummariesInfo[0]?.["updated_at"]}</p>

      <br></br>
      <br></br>
      <ul>
        {chatSummariesInfo.map((log, index) => (
          <li key={index}>
            {/* <p>chat_summary_id（編集する時に使う）: {log["chat_summary_id"]}</p> */}
            <p>content:{log["content"]}</p>
            <p>created_at:{log["created_at"]}</p>
            <br></br>
          </li>
        ))}
      </ul>
    </div>
  );
}
