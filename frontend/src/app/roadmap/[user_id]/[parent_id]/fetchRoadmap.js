export default async function fetchRoadmap(parent_user_id) {
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_ENDPOINT +
      `/roadmaps?parent_user_id=${parent_user_id}`,
    { cache: "no-cache" }
  );
  if (!res.ok) {
    throw new Error("Failed to fetch roadmap");
  }
  return res.json();
}
