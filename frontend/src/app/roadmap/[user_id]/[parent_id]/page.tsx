"use client";
import { useParams, useRouter } from "next/navigation";
import fetchRoadmap from "./fetchRoadmap";
import fetchItems from "./fetchItems";
import createItemIdToNameMap from "./createItemIdToNameMap";
import itemMap from "./itemMap";

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
        <div className="w-full max-w-md p-4 bg-white rounded-lg shadow">
          <div className="flex justify-between items-center mb-6">
            <a
              href="/menu"
              className="btn btn-square btn-ghost"
              style={{ width: "50px", height: "50px" }}
            >
              <img
                src="/Menu.svg"
                alt="メニュー"
                style={{ width: "25%", height: "25%" }}
              />
            </a>
            <h1 className="text-xl font-bold text-primary">
              親子でらくらく！大人の未来計画
            </h1>
          </div>
          <ul className="steps steps-vertical mx-auto">
            {roadmapInfo.map((item, index) => (
              <li
                key={index}
                className={`step ${
                  item.isComplete ? "bg-accent" : "bg-base-300"
                } ${
                  item.isComplete ? "text-primary-content" : "text-base-content"
                }`}
              >
                {item.title}
                {item.isComplete && (
                  <span className="label label-primary">済</span>
                )}
                <span className="step-secondary">
                  {item.timesCompleted} 回目
                </span>
              </li>
            ))}
          </ul>
          <div className="text-center mt-6">
            <a
              href={`/roadmap/${params.user_id}/${params.parent_id}/chat`}
              className="btn btn-circle btn-primary btn-sm"
              style={{ width: "50px", height: "50px" }}
            >
              <img
                src="/PlusButton.svg"
                alt="+ボタン"
                style={{ width: "15%", height: "15%" }}
              />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
