import time

class SessionManager:
    def __init__(self, expiry_seconds:int):
        self.expiry_seconds = expiry_seconds
        self.sessions = {}
        
    def create_session(self, session_id:str):
        
        self.sessions[session_id] = time.time()
        return f"Session {session_id} created."
    
    def is_session_active(self, session_id:str) -> bool:
        if session_id  not in self.sessions:
            return False
        else:
            del self.sessions[session_id]
            return False
        
    def delete_session(self, session_id:str):
        if session_id in self.sessions:
            del self.sessions[session_id]
            return "Deleted"
        return "Session not found."
    
    # ------------Test Run----------------#
if __name__ == "__main__":
    manager = SessionManager(expiry_seconds=3)
    
    print(manager.create_session("driver_101"))
    print("Is active?", manager.is_session_active("driver_101"))
    
    time.sleep(4)
    print("Is active after 4 seconds?", manager.is_session_active("driver_101"))
    
    print(manager.delete_session("driver_101"))
    
    print(manager.create_session("rider_202"))
    print(manager.delete_session("rider_202"))
    
    print("Test run completed successfully")