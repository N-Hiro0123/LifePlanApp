"use client";
import { useParams, useRouter } from "next/navigation";
import fetchRoadmap from "./fetchRoadmap";
import fetchItems from "./fetchItems";
import createItemIdToNameMap from "./createItemIdToNameMap";
import { useEffect, useState } from "react";

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
    const map = createItemIdToNameMap(itemInfo);
    setItemIdToNameMap(map);
    console.log(map);
  }, [itemInfo]);

  return (
    <div>
      <h1>Roadmap</h1>
      <ul>
        {/* {itemInfo.map((log, index) => (
          <li key={index}>
            <p>Item_id: {log.item_id}</p>
            <p>input_num: {log.item_name}</p>
            <br></br>
          </li>
        ))} */}
        {roadmapInfo.map((log, index) => (
          <li key={index}>
            <p>Item_id: {itemIdToNameMap[log.item_id]}</p>
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
