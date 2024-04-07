const createChatPost = async (values) => {
  //   const creating_customer_name = formData.get("customer_name");
  //   const creating_customer_id = formData.get("customer_id");
  //   const creating_age = formData.get("age");
  //   const creating_gender = formData.get("gender");
  console.log(values);
  const body_msg = JSON.stringify(values);

  const res = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + `/chatposts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body_msg,
  });
  if (!res.ok) {
    throw new Error("Failed to create chatposts");
  }
};

export default createChatPost;
