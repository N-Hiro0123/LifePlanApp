const createGPTSummary = async (values) => {
  const body_msg = JSON.stringify(values);
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_ENDPOINT + `/chatsummary`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body_msg,
    }
  );
  const data = await res.json();

  if (!res.ok) {
    throw new Error("Failed to get GptSummary");
  }
  return data;
};

export default createGPTSummary;
