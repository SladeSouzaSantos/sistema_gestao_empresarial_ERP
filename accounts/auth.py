from rest_framework.exceptions import AuthenticationFailed, APIException

from django.contrib.auth.hashers import check_password, make_password

from accounts.models import User
from companies.models import Enterprise, Employee

class Authentication:
    
    def sign_in(self, email=None, password=None):
        exception_auth = AuthenticationFailed("E-mail e/ou senha incorreto(s)")
        
        user_exists = User.objects.filter(email=email).exists()            
        if not user_exists:
            raise exception_auth
        
        user = User.objects.filter(email=email).first()
        if not check_password(password, user.password):
            raise exception_auth
        
        return user
        
    def sign_up(self, name=None, email=None, password=None, type_account="owner", company_id=False):
        if not name or name == "":
            raise APIException("O nome é obrigatório")
        
        if not email or email == "":
            raise APIException("O e-mail é obrigatório")
        
        if not password or password == "":
            raise APIException("A senha é obrigatória")
        
        if type_account == "employee" and not company_id:
            raise APIException("O ID da empresa é obrigatório para cadastro de funcionários")
        
        user = User
        if user.objects.filter(email=email).exists():
            raise APIException("Já existe um usuário cadastrado com esse e-mail")
        
        password_hashed = make_password(password)
        created_user = user.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=0 if type_account == "employee" else 1,
        )

        if type_account == "owner":            
            created_enterprise = Enterprise.objects.create(
                name="Nome da Empresa",
                user_id=created_user.id
            )

        if type_account == "employee":
            Employee.objects.create(
                enterprise_id=company_id or created_enterprise.id,
                user_id=created_user.id
            )

        return created_user