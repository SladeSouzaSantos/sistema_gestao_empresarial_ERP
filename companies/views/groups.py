from companies.views.base import Base
from companies.utils.exceptions import RequiredField
from companies.utils.permissions import GroupsPermission
from companies.serializers import GroupsSerializer

from accounts.models import Group, GroupPermission

from rest_framework.views import Response
from rest_framework.exceptions import APIException

from django.contrib.auth.models import Permission

class Groups(Base):
    permission_classes = [GroupsPermission]
    
    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        groups = Group.objects.filter(enterprise_id=enterprise_id).all()

        serializer = GroupsSerializer(groups, many=True)

        return Response({"groups": serializer.data})
    
    def post(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        name = request.data.get("name")
        permissions = request.data.get("permissions")

        if not name:
            raise RequiredField
        
        created_group = Group.objects.create(
            name=name,
            enterprise_id=enterprise_id
        )

        if permissions:
            permissions = permissions.split(",")
            
            try:
                permissions = [int(p) for p in permissions]
                for id_permission in permissions:
                    permission = Permission.objects.filter(id=id_permission).exists()

                    if not permission:
                        created_group.delete()
                        raise APIException("A permissão {p} não existe.".format(p= id_permission))
                    
                    if not GroupPermission.objects.filter(
                        group_id=created_group.id,
                        permission_id=id_permission
                    ).exists():
                        GroupPermission.objects.create(
                            group_id=created_group.id,
                            permission_id=id_permission
                        )
            
            except ValueError:
                created_group.delete()
                raise APIException("Envie as permissões no padrão correto.")
            
        return Response({"success": True})
    
class GroupDetail(Base):
    permission_classes = [GroupsPermission]
    
    def get(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        self.get_group(group_id, enterprise_id)
        group = Group.objects.filter(id=group_id).first()

        serializer = GroupsSerializer(group)

        return Response({"group": serializer.data})
    
    def put(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        self.get_group(group_id, enterprise_id)

        name = request.data.get("name")
        permissions = request.data.get("permissions")

        if name:
            Group.objects.filter(id=group_id).update(name=name)
        
        if permissions:
            permissions = permissions.split(",")
            
            try:
                permissions = [int(p) for p in permissions]
                GroupPermission.objects.filter(group_id=group_id).delete()
                for id_permission in permissions:
                    permission = Permission.objects.filter(id=id_permission).exists()

                    if not permission:                        
                        raise APIException("A permissão {p} não existe.".format(p= id_permission))
                    
                    if not GroupPermission.objects.filter(
                        group_id=group_id,
                        permission_id=id_permission
                    ).exists():
                        GroupPermission.objects.create(
                            group_id=group_id,
                            permission_id=id_permission
                        )
            
            except ValueError:
                raise APIException("Envie as permissões no padrão correto.")
            
        return Response({"success": True})
    
    def delete(self, request, group_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        Group.objects.filter(id=group_id, enterprise_id=enterprise_id).delete()

        return Response({"success": True})