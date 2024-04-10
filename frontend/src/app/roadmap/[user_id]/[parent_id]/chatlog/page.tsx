"use client";

import getChatlog from "./getChatlog";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

export default function Chatlog() {
  const router = useRouter();
  const params = useParams();
  //   console.log(params.user_id, params.parent_id);
  const [chatlogInfo, setChatlogInfo] = useState([]);

  useEffect(() => {
    const fetchGetChatlog = async () => {
      const values = {
        parent_user_id: params.parent_id,
        child_user_id: params.user_id,
      };
      const data = await getChatlog(values);
      setChatlogInfo(data);
    };
    fetchGetChatlog();
  }, []);

  return (
    <div>
      <h1>Chat Log</h1>
      <ul>
        {chatlogInfo.map((log, index) => (
          <li key={index}>
            <p>Posted by: {log.role}</p>
            <p>Created At: {log.chatpost_created_at}</p>
            <p>
              Content: <strong>{log.content}</strong>
            </p>
            <br></br>
          </li>
        ))}
      </ul>
    </div>
  );
}
