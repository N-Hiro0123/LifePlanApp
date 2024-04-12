export default function createItemIdToNameMap(itemInfo) {
  const map = itemInfo.reduce((acc, item) => {
    acc[item.item_id] = item.item_name;
    return acc;
  }, {});

  return map;
}
