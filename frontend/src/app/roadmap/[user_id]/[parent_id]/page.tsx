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
    <div>
      <Link href={`/roadmap/${params.user_id}/${params.parent_id}/chat`}>
        <p>
          <strong>Chat**link**</strong>
        </p>
      </Link>
      <Link href={`/roadmap/${params.user_id}/${params.parent_id}/chatlog`}>
        <p>
          <strong>Chatlog**link**</strong>
        </p>
      </Link>
      <h1>Roadmap</h1>
      <ul>
        {roadmapInfo.map((log, index) => (
          <li key={index}>
            <Link
              href={`/roadmap/${params.user_id}/${params.parent_id}/${itemIdToNameMap[log.item_id]}`}
            >
              <p>
                <strong>
                  Item_id --link--: {itemMap[itemIdToNameMap[log.item_id]]}
                </strong>
              </p>
            </Link>
            <p>input_num: {log.item_input_num}</p>
            <p>State:{log.item_state}</p>
            <p>Update_At: {log.item_updated_at}</p>
            <br></br>
          </li>
        ))}
      </ul>
    </div>
  );
}
