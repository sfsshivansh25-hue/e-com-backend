from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.repositories import user
from app.repositories.user import UserRepository
from app.core.security import hash_password, verify_password




class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)


    async def register_user(self, email: str, password: str) -> User:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        user = User(
            email=email,
            password_hash=hash_password(password),
            role="user",
        )


        await self.repo.create(user)
        await self.session.commit()
        return user


    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")


        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        return user