# =============PYDANTIC==============

# base model
from practice.pydantic1 import (
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
    ValidationError,
    conint,
    constr,
    Field,
)

from typing import List

PositiveInt = conint(gt=0)


class UserProfile(BaseModel):
    model_config = ConfigDict(strict=True)
    name: str
    age: int
    email: str

    @field_validator("age")
    @classmethod
    def check_age(cls, age):
        if age < 18:
            return ValueError("must be atleast 18")
        return age


user = UserProfile(name="abdurrehman", age=17, email="abdurrehman@gmail.com")
print(user)

data = '{"name": "abdurrehman", "age": 22, "email": "abdurrehman@gmail.com"}'
user = UserProfile.model_validate_json(data)
print(user)
json_data = UserProfile.model_dump_json(user)
print(json_data)


class User(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    @classmethod
    def match_passwords(cls, model):
        if model.password != model.confirm_password:
            raise ValueError("Passwords do not match")
        return model


try:
    user1 = User(password="a", confirm_password="b")
    print(user1)
except ValidationError as e:
    print(e)


class Product(BaseModel):
    name: str = Field(min_length=1)
    price: int = Field(gt=0)
    tags: List[str] = []


from fastapi import FastAPI, HTTPException, status
from practice.pydantic1 import BaseModel, Field, EmailStr, ConfigDict, model_validator
from datetime import datetime

fake_db = []

app = FastAPI()


class userShared(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr


class UserRequest(userShared):
    password: str = Field(min_length=8, description="password atleast 8 characters")
    confirm_password: str = Field(min_length=8, description="should match password")

    @model_validator(mode="after")
    def match_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("passwords dont match")
        return self


class UserResponse(userShared):
    id: int = Field(gt=0)
    created_at: datetime = Field(default=datetime.now())
    isActive: bool = False
    model_config = ConfigDict(from_attributes=True)


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserRequest):

    for user in fake_db:
        if user["email"] == user_in.email:
            raise HTTPException(status_code=400, detail="email alr registered")

    user_data = user_in.model_dump()
    user_data.pop("confirm_password")
    user_data["password"] = "random hashed password dummy for now"
    user_data.update(
        {"id": len(fake_db) + 1, "created_at": datetime.now(), "isActive": True}
    )

    fake_db.append(user_data)
    return user_data


@app.get("/users", response_model=list[UserResponse])
def get_users():
    return fake_db
