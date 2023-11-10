import requests
from enum import Enum
from typing import List
from typing_extensions import Annotated
from fastapi import FastAPI, Path
from pydantic import BaseModel
from random import randint


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', summary='Root', operation_id='root__get')
def root() -> str:
    ''' Return interesting fact about random number fron 1 to 1000 '''
    return requests.get("http://numbersapi.com/{}".format(randint(1, 1000))).text

@app.get('/dog', summary='Get dogs', operation_id='get_dogs_dog_get')
def get_dog(kind: DogType) -> List[Dog]:
    ''' Return the list of dogs with such DogType from dog_db '''
    tmp = []
    for k, v in dog_db.items():
        if v.kind == kind:
            tmp.append(dog_db[k])
    return tmp

@app.get('/dog/{pk}', summary='Get Dog By Pk', operation_id='get_dog_by_pk_dog__pk__get')
def get_dog_pk(pk: Annotated[int, Path(ge=0, le=len(dogs_db)-1)) -> Dog:
    ''' Return Dog from dogs_db with given pk + (added Pk bounds check)'''
    for k, v in dogs_db.items():
        if v.pk == pk:
            return dogs_db[k]
