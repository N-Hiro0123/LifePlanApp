const getChatlogSmall = async (values) => {
  const body_msg = JSON.stringify(values);
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_ENDPOINT + `/chatlogsmall`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body_msg,
    }
  );
  const data = await res.json();

  if (!res.ok) {
    throw new Error("Failed to get chatlog");
  }
  return data;
};

export default getChatlogSmall;
