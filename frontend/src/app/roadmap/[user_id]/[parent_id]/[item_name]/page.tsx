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

  useEffect(() => {
    const fetchAndSetDatas = async () => {
      const Data = await fetchRoadmapDtails(
        params.parent_id,
        params.user_id,
        params.item_name
      );
      setdetailDatas(Data);
    };
    fetchAndSetDatas();
  }, []);

  useEffect(() => {
    const roadmapdata = detailDatas[roadmap];
    setRoadmapInfo(roadmapdata);
    const chatdata = detailDatas[chatsummaries];
    setChatSummariesInfo(chatdata);
    const manualdata = detailDatas[manualsummaries];
    setManualSummariesInfo(manualdata);
  }, [detailDatas]);

  return (
    <div>
      <Link href={`/roadmap/${params.user_id}/${params.parent_id}`}>
        <p>
          <strong>Roadmap**link**</strong>
        </p>
      </Link>

      <h1>{params.item_name}</h1>
      <p>{roadmapInfo[item_input_num]}</p>
      {/* <p>input_num: {roadmapInfo.item_input_num}</p>
      <p>State:{roadmapInfo.item_state}</p> */}

      {/* <ul>
        {roadmapInfo.map((log, index) => (
          <li key={index}>
            <Link
              href={`/roadmap/${params.user_id}/${params.parent_id}/${itemIdToNameMap[log.item_id]}`}
            >
              <p>
                <strong>
                  Item_id --link--: {itemIdToNameMap[log.item_id]}
                </strong>
              </p>
            </Link>
            <p>input_num: {log.item_input_num}</p>
            <p>State:{log.item_state}</p>
            <p>Update_At: {log.item_updated_at}</p>
            <br></br>
          </li>
        ))}
      </ul> */}
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
