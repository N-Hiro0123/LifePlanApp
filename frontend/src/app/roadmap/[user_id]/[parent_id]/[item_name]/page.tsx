"use client";
import { useParams, useRouter } from "next/navigation";
import fetchRoadmapDtails from "./fetchRoadmapDtails";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function RoadmapDatails() {
  const router = useRouter();
  const params = useParams();
  // console.log(params.user_id, params.parent_id, params.item_name);
  const [detailDatas, setdetailDatas] = useState([]);
  const [roadmapInfo, setRoadmapInfo] = useState([]);
  const [chatSummariesInfo, setChatSummariesInfo] = useState([]);
  const [manualSummariesInfo, setManualSummariesInfo] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

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
      setIsLoading(false);
    };
    fetchAndSetDatas();
  }, []);

  useEffect(() => {
    if (!isLoading) {
      console.log(roadmapInfo, chatSummariesInfo, manualSummariesInfo);
    }
  }, [isLoading, roadmapInfo, chatSummariesInfo, manualSummariesInfo]);

  return (
    <div>
      <Link href={`/roadmap/${params.user_id}/${params.parent_id}`}>
        <p>
          <strong>Roadmap**link**</strong>
        </p>
      </Link>
      <br></br>
      <h1>{params.item_name}</h1>
      <h1>Roadmap</h1>
      <p>input_num: {roadmapInfo[0]["item_input_num"]}</p>
      <p>state: {roadmapInfo[0]["item_state"]}</p>

      <br></br>
      <h1>Manual Summaries</h1>
      <p>
        manual_summary_id（編集する時に使う）:
        {manualSummariesInfo[0]["manual_summary_id"]}
      </p>
      <p>input_num: {manualSummariesInfo[0]["content"]}</p>
      <p>update_at: {manualSummariesInfo[0]["updated_at"]}</p>

      <br></br>
      <ul>
        {chatSummariesInfo.map((log, index) => (
          <li key={index}>
            <p>chat_summary_id（編集する時に使う）: {log["chat_summary_id"]}</p>
            <p>content:{log["content"]}</p>
            <p>created_at:{log["created_at"]}</p>
            <br></br>
          </li>
        ))}
      </ul>
    </div>
  );

  //   return (
  //     <div>
  //       <Link href={`/roadmap/${params.user_id}/${params.parent_id}`}>
  //         <p>
  //           <strong>Roadmap**link**</strong>
  //         </p>
  //       </Link>
  //       <h1>{params.item_name}</h1>
  //       <p>input_num: {roadmapInfo.item_input_num.0}</p>
  //       <p>State:{roadmapInfo.item_state.0}</p>
  //       <h1>Mnual Summaries</h1>
  //       <p>content: {manualSummariesInfo.content.0}</p>
  //       <p>update_at: {manualSummariesInfo.updated_at.0}</p>
  //       <p>manual_summary_id（編集する時に使う）: {manualSummariesInfo.summary_id.0}</p>
  //       <ul>
  //         {chatSummariesInfo.map((log, index) => (
  //           <li key={index}>
  //             <p>chat_summary_id（編集する時に使う）: {log.chat_summary_id}</p>
  //             <p>content:{log.content}</p>
  //             <p>created_at:{log.created_at}</p>
  //             <br></br>
  //           </li>
  //         ))}
  //       </ul>
  //     </div>
  //   );
}
