const createChatPostGPT = async (values) => {
  const body_msg = JSON.stringify(values);
  console.log(values);
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_ENDPOINT + `/chatpostgpt`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body_msg,
    }
  );
  if (!res.ok) {
    throw new Error("Failed to create chatpostgpt");
  }
  return true;
};

export default createChatPostGPT;
