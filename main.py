import requests
from enum import Enum
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from random import randint
from time import time


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
    for k, v in dogs_db.items():
        if v.kind == kind:
            tmp.append(dogs_db[k])
    return tmp

@app.get('/dog/{pk}', summary='Get Dog By Pk', operation_id='get_dog_by_pk_dog__pk__get')
def get_dog_pk(pk: Annotated[int, Path(ge=0, le=len(dogs_db)-1)]) -> Dog:
    ''' Return Dog from dogs_db with given pk '''
    for k, v in dogs_db.items():
        if v.pk == pk:
            return dogs_db[k]

@app.post('/dog', response_model=Dog, summary='Create Dog', operation_id='create_dog_dog_post')
def post_dog(dog: Dog) -> Dog:
    ''' Add Dog to dogs_db. Return added Dog '''
    dogs_db[len(dogs_db)] = dog
    return dog

@app.post('/post', response_model=Timestamp, summary='Get Post', operation_id='get_post_post_post')
def post() -> Timestamp:
    ''' Add Timestamp to post_db. Return added Timestamp '''
    post_db.append(Timestamp(id=len(post_db), timestamp=time()))
    return post_db[-1]

@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog', operation_id='update_dog_dog__pk__patch')
def patch(pk: int, dog: Dog) -> Dog:
    ''' Update dog info. Return updated dog '''
    for k, v in dogs_db.items():
        if v.pk == pk:
            dogs_db[k] = dog
            return dog
