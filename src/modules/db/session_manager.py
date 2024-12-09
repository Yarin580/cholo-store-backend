from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class SessionManager:
    def __init__(self, session_factory: async_sessionmaker, savepoint: bool = False):
        """
        Initializes the session manager with a session factory and optional savepoint support.
        """
        self.session_factory = session_factory
        self.savepoint = savepoint
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        """
        Async context manager entry point.
        Creates a new session and optionally begins a savepoint transaction.
        """
        self.session = self.session_factory()
        if self.savepoint:
            await self.session.begin_nested()  # Savepoint for nested transactions
        else:
            await self.session.begin()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Async context manager exit point.
        Commits the transaction if no exception occurred, otherwise rolls back.
        """
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()

        await self.session.close()
