from rest_framework.exceptions import APIException

class NotFoundEmployee(APIException):
    status_code = 404
    default_detail = "Funcionário não encontrado."
    default_code = "not_found_employee"

class NotFoundGroup(APIException):
    status_code = 404
    default_detail = "Grupo de usuário não encontrado."
    default_code = "not_found_group"

class RequiredField(APIException):
    status_code = 400
    default_detail = "Campo obrigatório não foi preenchido corretamente."
    default_code = "error_required_field"

class NotFoundTaskStatus(APIException):
    status_code = 404
    default_detail = "Status de tarefa não encontrado."
    default_code = "not_found_task_status"

class NotFoundTask(APIException):
    status_code = 404
    default_detail = "Tarefa não encontrada."
    default_code = "not_found_task"