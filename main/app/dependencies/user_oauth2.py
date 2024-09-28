# from ..database.config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
import jwt
from json import dumps
from datetime import timezone, timedelta, datetime, date
from fastapi import HTTPException,status,Depends
# from jwt.api_jwt import encode,

ALGORITHM = "HS256"
SECRET_KEY = "32c746fa44e4f23f19ae95b309affc9a7fcffc9511b42d080e4497a7face4d8e"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# This is the authentication function you will pass in the user routes
# as a dependency for authentication
# After passing it as a dependency you can store the current user id as a
# variable and use it to get user data in the user routes
def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verify the jwt token and return the current(login) user id
    for further authentication in the routes"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)

# This function handles serialization of obj into a
# format that can be converted into JSON.
# it is use in the create_access_token function
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(
        obj, (datetime, date)
    ):  # check if the object is in datetime or date format
        return obj.isoformat()  # convert it to a JSon serialization format
    raise TypeError("Type %s not serializable" % type(obj))


# create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()  # copying the data

    # if the expire_delta time is provided
    if expires_delta:
        # set the expire time to the current time
        # plus expire time(168hours = 1week)
        # Converts the result to a JSON-serializable format
        expire = dumps(
            datetime.now(timezone.utc) + expires_delta, default=json_serial
            )

    else:
        # if the expire time is not provided, the current expire time will be
        # current time plus 70hrs
        # Converts the result to a JSON-serializable format
        expire = dumps(
            datetime.now(timezone.utc) + timedelta(hours=70),
            default=json_serial
        )
    to_encode.update(
        {"expire": str(expire)}
    )  # updating the data to have the expire keyword and expire time
    # encode the data(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithms=ALGORITHM)
    return encoded_jwt

# verify the token
def verify_token(token: str, credentials_exceptions):
    try:
        print(ALGORITHM)
        # decode the data using the token, secret key and the algorithm
        payload = jwt.decode(token, SECRET_KEY,algorithms=["HS256"])
        print(payload)
        email = payload.get("sub")  # extracts the username from the payload
        user_id = payload.get("id")  # extracts the user id
        if not email:
            raise credentials_exceptions
        # returns the user id so that you can use it to fetch
        # the current(login) user data for update and delete operations
        return user_id
    except Exception as e:
        raise e
