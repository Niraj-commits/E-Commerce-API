from rest_framework.permissions import BasePermission,SAFE_METHODS


class RegisterUser(BasePermission):
    
    def has_permission(self, request, view):
        
        if not request.user.is_authenticated and request.method == "POST":
            return True
        
        if request.user.is_authenticated and request.user.role == "admin":
            return True
        
        if request.user.is_authenticated and request.user.role !="admin":
            if request.method =="POST":
                return True
            
            else:
                return False
        
        else:
            return False