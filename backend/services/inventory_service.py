from repositories.inventory_repo import InventoryRepository


class InventoryService:

    @staticmethod
    def create_item(data):

        item = Item(
            code=data["code"],
            name=data["name"],
            quantity=data.get("quantity", 0),
            available=data.get("available", 0),
            status=data.get("status", "ACTIVE"),
            category_id=data["category_id"]
        )
        return InventoryRepository.create(item)

    @staticmethod
    def get_items():
        return InventoryRepository.get_all()