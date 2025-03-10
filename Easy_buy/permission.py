
from rest_framework.permissions import BasePermission,SAFE_METHODS
from core.models import User

class ViewOnly(BasePermission):
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        else:
            if request.user.role == "admin":
                return True
            
            elif request.user.role == "customer":
                if request.method in SAFE_METHODS:
                    return True
                else:
                    return False
            
            elif request.user.role == "supplier":
                if request.method in SAFE_METHODS or request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                    return True
                else:
                    return False
    
    def has_object_permission(self, request, view,obj):
            
        if request.user.role == "admin":
            return True
            
        if request.user.role == "supplier":
            return obj.created_by == request.user
        
        else:
            return False