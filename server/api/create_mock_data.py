### EDIT OR DELETE THIS FILE AS NEEDED ###

# import asyncio
# import random
# import logging

# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.orm import sessionmaker

# from database import get_session
# from models import Item, Category, Supplier, Base
# from config import NUM_ITEMS, NUM_CATEGORIES, NUM_SUPPLIERS

# from faker import Faker

# router = APIRouter()
# faker = Faker()

# async def create_mock_categories(num_categories: int, session: AsyncSession = Depends(get_session)):
#     categories = [Category(name=faker.word()) for _ in range(num_categories)]
#     session.add_all(categories)
#     await session.commit()
#     return categories

# async def create_mock_suppliers(num_suppliers: int, session: AsyncSession = Depends(get_session)):
#     suppliers = [
#         Supplier(name=faker.company(), contact_info=faker.phone_number())
#         for _ in range(num_suppliers)
#     ]
#     session.add_all(suppliers)
#     await session.commit()
#     return suppliers

# async def create_mock_items(num_items: int, categories, suppliers, session: AsyncSession = Depends(get_session)):
#     items = []
#     for item in range(num_items):
#         item = Item(
#             name=faker.word(),
#             description=faker.sentence(),
#             stock=random.randint(0, 100),
#             category_id=random.choice(categories).id,
#             supplier_id=random.choice(suppliers).id,
#         )
#         items.append(item)
#     session.add_all(items)
#     await session.commit()

# async def generate_mock_data(num_categories: int, num_suppliers: int, num_items: int, session: AsyncSession):
#     print("Generating mock data")
#     # async with get_session() as session:
#     categories = await create_mock_categories(num_categories, session)
#     suppliers = await create_mock_suppliers(num_suppliers, session)
#     await create_mock_items(num_items, categories, suppliers, session)

# @router.post("/generate-mock-data/")
# async def generate_mock_data_endpoint(
#     num_categories: int=NUM_CATEGORIES, num_suppliers: int=NUM_SUPPLIERS, num_items: int=NUM_ITEMS, session: AsyncSession = Depends(get_session)
# ):
#     try:
#         await generate_mock_data(num_categories, num_suppliers, num_items, session)
#         return {"message": "Mock data generated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
