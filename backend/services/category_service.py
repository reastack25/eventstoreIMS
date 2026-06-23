from models.category import Category
from repositories.category_repo import CategoryRepository


class CategoryService:

    @staticmethod
    def create_category(data):

        category = Category(
            name=data["name"],
            description=data.get("description")
        )

        return CategoryRepository.create(category)

    @staticmethod
    def get_categories():
        return CategoryRepository.get_all()

    @staticmethod
    def get_category(category_id):
        return CategoryRepository.get_by_id(category_id)