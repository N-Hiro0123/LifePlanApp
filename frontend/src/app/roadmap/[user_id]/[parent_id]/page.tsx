"use client";
import { useParams, useRouter } from "next/navigation";
import fetchRoadmap from "./fetchRoadmap";
import fetchItems from "./fetchItems";
import createItemIdToNameMap from "./createItemIdToNameMap";
import itemMap from "./itemMap";
import getStateClass from "./getStepClass";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function Roadmap() {
  const router = useRouter();
  const params = useParams();
  // console.log(params.user_id, params.parent_id);
  const [itemInfo, setItemInfo] = useState([]);
  const [roadmapInfo, setRoadmapInfo] = useState([]);
  const [itemIdToNameMap, setItemIdToNameMap] = useState({});

  useEffect(() => {
    const fetchAndSetItems = async () => {
      const itemData = await fetchItems();
      setItemInfo(itemData);
    };
    fetchAndSetItems();
  }, []);

  useEffect(() => {
    const fetchAndSetRoadmap = async () => {
      const roadmapData = await fetchRoadmap(params.parent_id);
      setRoadmapInfo(roadmapData);
    };
    fetchAndSetRoadmap();
    // item_idをitem_nameへ変換するmapを作成
    const map = createItemIdToNameMap(itemInfo);
    setItemIdToNameMap(map);
    // console.log(map);
  }, [itemInfo]);

  return (
    <div className="container">
      <div className="flex flex-col justify-center items-center min-h-screen bg-base-100">
        <div className="w-full max-w-md p-4 bg-white rounded-lg shadow text-center">
          {" "}
          {/* Added text-center */}
          <div className="flex justify-between items-center mb-6">
            <a href="/menu" className="btn btn-square btn-ghost" style={{ width: "50px", height: "50px" }}>
              <img src="/Menu.svg" alt="メニュー" style={{ width: "100%", height: "100%" }} />
            </a>
            <h1 className="text-xl font-bold text-neutral">親子でらくらく！大人の未来計画</h1>
          </div>
          <ul className="steps steps-vertical mx-auto">
            {" "}
            {/* Added mx-auto */}
            {roadmapInfo.map((item, index) => (
              <li key={index} data-content={item.item_input_num} className={getStateClass(item.item_state)}>
                <Link href={`/roadmap/${params.user_id}/${params.parent_id}/${itemIdToNameMap[item.item_id]}`}>
                  <p>
                    <strong> {itemMap[itemIdToNameMap[item.item_id]]}</strong>
                  </p>
                </Link>
              </li>
            ))}
          </ul>
          <div className="flex justify-center items-center mt-4">
            <a href={`/roadmap/${params.user_id}/${params.parent_id}/chat`}>
              <img src="/PlusButton.svg" alt="+ボタン" style={{ width: "80%", height: "80%" }} />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
