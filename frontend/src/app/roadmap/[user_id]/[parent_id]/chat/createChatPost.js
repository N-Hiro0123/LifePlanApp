const createChatPost = async (values) => {
  const body_msg = JSON.stringify(values);

  const res = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + `/chatposts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body_msg,
  });
  if (!res.ok) {
    throw new Error("Failed to create chatposts");
  }
  return true;
};

export default createChatPost;
