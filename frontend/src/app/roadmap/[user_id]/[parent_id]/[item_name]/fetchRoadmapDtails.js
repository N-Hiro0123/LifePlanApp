export default async function fetchRoadmapDtails(
  parent_user_id,
  child_user_id,
  item_name
) {
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_ENDPOINT +
      `/roadmapdetails?parent_user_id=${parent_user_id}&child_user_id=${child_user_id}&item_name=${item_name}`,
    { cache: "no-cache" }
  );
  if (!res.ok) {
    throw new Error("Failed to fetch roadmap");
  }
  return res.json();
}
