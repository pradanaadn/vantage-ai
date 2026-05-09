from typing import List, Dict

class ItemsService:
    def __init__(self):
        # Initial mock data
        self._items = [
            {"id": 1, "name": "Global Server A1"},
            {"id": 2, "name": "Storage Cluster 04"},
            {"id": 3, "name": "AI Processing Unit"},
            {"id": 4, "name": "Edge Gateway Pro"},
            {"id": 5, "name": "Network Bridge V2"},
            {"id": 6, "name": "Security Vault X"},
        ]

    async def get_all_items(self) -> List[Dict]:
        """
        Fetch all items. This can be easily updated to use 
        any database (SQL, NoSQL, etc.) in the future.
        """
        return self._items

    async def create_item(self, name: str) -> Dict:
        new_item = {"id": len(self._items) + 1, "name": name}
        self._items.append(new_item)
        return new_item

# Dependency Injection instance
items_service = ItemsService()
