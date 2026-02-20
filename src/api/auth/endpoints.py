import logging
from fastapi import APIRouter, Body, status 
from fastapi.responses import JSONResponse
from src.api.auth.dependencies import AuthServiceDependency, CurrentUserDependency
from src.api.auth.schemas import LoginResponse, LoginRequest, RegisterRequest, UserResponseSchema
from src.api.general_schemas import ErrorResponse, SuccessResponse


router = APIRouter(prefix="/auth", tags=["authorization"])


@router.post("/login", response_model=LoginResponse)
async def login(service: AuthServiceDependency, data: LoginRequest = Body()) -> JSONResponse:
    user = await service.login(data.username, data.password)
    if not user:
        return JSONResponse(
            content=ErrorResponse(message="Пароль неверный или пользователь не существует").model_dump(),
            status_code=status.HTTP_400_BAD_REQUEST    
        )
    return LoginResponse.from_dto(user)


@router.post("/register")
async def register(
    service: AuthServiceDependency,
    data: RegisterRequest = Body()
) -> JSONResponse:
    try:
        user = await service.register(
            name=data.name,
            username=data.username,
            password=data.password,
            email=data.email
        )
        return JSONResponse(
            content=SuccessResponse(message=f"Пользователь {user.name} успешно создан").model_dump(),
            status_code=status.HTTP_201_CREATED
        )
    except ValueError as e:
        error_msg = str(e)

        if "уже существует" in error_msg or "username" in error_msg.lower() or "email" in error_msg.lower():
            return JSONResponse(
                content=ErrorResponse(message=error_msg).model_dump(),
                status_code=status.HTTP_409_CONFLICT
            )

        else:
            logging.error(f"Registration error: {error_msg}")
            return JSONResponse(
                content=ErrorResponse(message="Внутренняя ошибка сервера").model_dump(),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@router.get("/me", response_model=UserResponseSchema)
async def get_me(user: CurrentUserDependency) -> JSONResponse:
    if not user:
        return JSONResponse(content=ErrorResponse(message="Пользователь не существует").model_dump(), status_code = status.HTTP_401_UNAUTHORIZED)
    return JSONResponse(content=UserResponseSchema.from_dto(user).model_dump(), status_code=status.HTTP_200_OK)


