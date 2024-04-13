export default async function fetchItems() {
  const res = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + `/items`, {
    cache: "no-cache",
  });
  if (!res.ok) {
    throw new Error("Failed to fetch items");
  }
  return res.json();
}
