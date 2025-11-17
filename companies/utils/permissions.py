from rest_framework import permissions
from accounts.models import UserGroup, GroupPermission
from django.contrib.auth.models import Permission

def check_permission(user, method, permission_to):
    if not user.is_authenticated:
        return False
    
    if user.is_owner:
        return True
    
    #method == "GET"
    requested_permission = "view_" + permission_to
    
    if method == "POST":
        requested_permission = "add_" + permission_to    
    elif method == "PUT":
        requested_permission = "change_" + permission_to
    elif method == "DELETE":
        requested_permission = "delete_" + permission_to
    
    groups = UserGroup.objects.values('group_id').filter(user_id=user.id).all()

    for group in groups:
        permissions = GroupPermission.objects.values('permission_id').filter(group_id=group['group_id']).all()
        
        for permission in permissions:
            if Permission.objects.filter(id=permission['permission_id'], codename=requested_permission).exists():
                return True

class EmployeesPermission(permissions.BasePermission):
    message = "Funcionário não possui permissão para gerenciar funcionários."

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to="employee")
    
class GroupsPermission(permissions.BasePermission):
    message = "O funcionário não possui permissão para gerenciar grupos."

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to="group")

class GroupsPermissionsPermission(permissions.BasePermission):
    message = "O funcionário não possui permissão para gerenciar permissões."

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to="permission")
    
class TaskPermission(permissions.BasePermission):
    message = "O funcionário não possui permissão para gerenciar tarefas de todos os funcionários."

    def has_permission(self, request, _view):
        return check_permission(request.user, request.method, permission_to="task")