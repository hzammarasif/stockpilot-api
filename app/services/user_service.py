



class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        session: AsyncSession,
    ):
        self.user_repository = user_repository
        self.session = session

