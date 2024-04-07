export default async function fetchChatPosts() {
  const res = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + "/chatposts", {
    cache: "no-cache",
  });
  if (!res.ok) {
    throw new Error("Failed to fetch chatposts");
  }
  // resを呼び出せるのは一度まで。awaitを使わないとPromiseオブジェクトが格納されてしまう
  const data = await res.json();

  return data["created_at"];
}
