const createChatRawData = async (values) => {
  const body_msg = JSON.stringify(values);

  const res = await fetch(
    process.env.NEXT_PUBLIC_API_ENDPOINT + `/chatrawdatas`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body_msg,
    }
  );
  if (!res.ok) {
    throw new Error("Failed to create chatrawdatas");
  }
};

export default createChatRawData;
