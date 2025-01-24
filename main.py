from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

data = {}  # Assuming this to be the a DB


class Item(BaseModel):
    name: str
    price: int
    description: Optional[str] = ""


# Now we can create API endpoints.


@app.get("/get-data/{data_id}")
def get_data(data_id: str = Path(description="Id of the data to get.")):
    """
    In this we are taking the path parameter and processing on the basis of it.
    Path function helps to make the endpoint a little more descriptive by providing
    more information like default value and description, title, etc.
    """
    return data.get(data_id, None)


@app.get("/query-data")
def query_data(name: str = Query(None, description="Name of the data to get.")):
    """
    In this we are taking a query parameter and processing based on it.
    Query function helps to make the endpoint more descriptive by providing
    more information like default value, description, title, etc.

    Example usecase: http://localhost/query-data?name=examplename&price=400

    """
    for data_id, data_value in data.items():
        if data_value.name == name:
            return data[data_id]
    return HTTPException(404, "Data not found!")


@app.post("/add-data")
def add_data(data_id: str, data_item: Item):
    """
    Using BaseModel from pydantic we define a structure of the function header.
    """
    if data_item.name and data_item.price:
        data[data_id] = data_item
        return data
    return HTTPException(422, "Provide all function headers.")


@app.put("/update/{data_id}")
def update_data(
    data_id: str,
    name: Optional[str] = None,
    price: Optional[int] = None,
    description: Optional[str] = None,
):
    if data_id not in data:
        return HTTPException(404, "Data is not present!")

    if name:
        data[data_id].name = name
    if price:
        data[data_id].price = price
    if description:
        data[data_id].description = description

    return data[data_id]


@app.delete("/delete/{data_id}")
def delete(data_id: str):
    if data_id not in data:
        return HTTPException(404, "Data not present!")
    temp = data[data_id]
    del data[data_id]
    return temp
