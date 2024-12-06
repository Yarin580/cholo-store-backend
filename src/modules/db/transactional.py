from functools import wraps
from .session_manager import SessionManager

def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with SessionManager() as session:  # SessionManager handles session creation
            try:
                kwargs['session'] = session  # Pass the session to the service method
                result = func(*args, **kwargs)  # Call the original function with session
                session.commit()  # Commit after successful function execution
                return result
            except Exception as e:
                session.rollback()  # Rollback in case of an error
                raise e
            finally:
                session.close()  # Ensure session is closed
    return wrapper
