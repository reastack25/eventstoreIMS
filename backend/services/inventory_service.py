from repositories.inventory_repo import InventoryRepository


class InventoryService:

    @staticmethod
    def get_items():
        return InventoryRepository.get_all()