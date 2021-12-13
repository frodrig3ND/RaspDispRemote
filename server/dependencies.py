from .db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except: # noqa
        db.rollback()
        raise
    finally:
        db.close()
