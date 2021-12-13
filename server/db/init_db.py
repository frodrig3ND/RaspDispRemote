from server.db import base  # noqa: F401
from server.db import session

# We copy the usual init_db, obviously if we weren't using
# sqlite we would use alembic, but since we are and its kind of a pain
# to set alembic to work with sqlite we are just going to go ahead
# and initialize, we really don't expect to perform a ton of migrations
# in this. However the whole application is setup to easlity switch
# to something like postgres


def init_db() -> None:
    base.Base.metadata.create_all(bind=session.engine)


if __name__ == "__main__":
    init_db()
