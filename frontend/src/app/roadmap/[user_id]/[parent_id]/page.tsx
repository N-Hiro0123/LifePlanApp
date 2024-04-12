"use client";
import { useParams, useRouter } from "next/navigation";
import fetchRoadmap from "./fetchRoadmap";
import { useEffect, useState } from "react";

export default function Roadmap() {
  const router = useRouter();
  const params = useParams();
  // console.log(params.user_id, params.parent_id);

  const [roadmapInfo, setRoadmapInfo] = useState([]);

  useEffect(() => {
    const fetchAndSetCustomer = async () => {
      const roadmapData = await fetchRoadmap(params.parent_id);
      setRoadmapInfo(roadmapData);
    };
    fetchAndSetCustomer();
  }, []);

  return (
    <div>
      <h1>Roadmap</h1>
      <ul>
        {roadmapInfo.map((log, index) => (
          <li key={index}>
            <p>Item_id: {log.item_id}</p>
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
