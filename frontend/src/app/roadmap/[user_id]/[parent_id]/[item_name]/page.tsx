"use client";
import { useParams, useRouter } from "next/navigation";
import fetchRoadmapDtails from "./fetchRoadmapDtails";
import itemMap from "../itemMap";
import stateMap from "./stateMap";

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
    <div className="max-w-4xl mx-auto">
      <div className="w-full max-w-xl p-4 bg-white rounded-lg shadow-md">
        <div className="flex flex-col items-start p-4">
          {" "}
          {/* Changed this line */}
          <Link href={`/roadmap/${params.user_id}/${params.parent_id}`} legacyBehavior>
            <a className="self-start mb-4">
              <img src="/Close.svg" alt="Close" style={{ width: "100px", height: "100px" }} />
            </a>
          </Link>
          <div className="grid grid-cols-5 gap-4 mb-4 w-full">
            <div className="col-span-1">
              <p className="text-gray-600 font-bold">{stateMap[roadmapInfo[0]?.["item_state"]]}</p>
            </div>
            <div className="col-span-1">
              <p className="text-gray-600 font-bold">{roadmapInfo[0]?.["item_input_num"]}</p>
            </div>
            <div className="col-span-3">
              <h1 className="text-xl font-bold whitespace-nowrap">{itemMap[params.item_name]}</h1>
            </div>
          </div>
          {/* Manual Summaries */}
          <br></br>
          <div className="w-full max-w-xl space-y-4 text-left">
            <h2 className="text-lg font-semibold">手動要約</h2>
            <div className="bg-white shadow overflow-hidden sm:rounded-lg">
              <div className="px-8 py-5 text-left">
                <p className="mt-1 text-sm text-gray-500">Content: {manualSummariesInfo[0]?.["content"]}</p>
                <p className="mt-1 text-sm text-gray-500">Updated At: {manualSummariesInfo[0]?.["updated_at"]}</p>
              </div>
            </div>
          </div>
          {/* AI Summariesの内容 */}
          <br></br>
          <ul className="w-full max-w-xl space-y-4 text-left">
            <h3 className="text-lg font-semibold">AI要約</h3>
            {chatSummariesInfo.map((log, index) => (
              <li key={index} className="bg-gray-100 p-3 rounded-lg text-left">
                <p className="text-gray-800">Content: {log["content"]}</p>
                <p className="text-gray-500">Created At: {log["created_at"]}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
