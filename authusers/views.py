from dj_rest_auth.views import UserDetailsView
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import LoginView

class CustomUserDetailsView(UserDetailsView):
    def get(self, request, *args, **kwargs):
        user = request.user
        roles = list(user.groups.values_list("name", flat=True))  # Obtiene los nombres de los roles (grupos)

        data = {
            "id": user.id,
            "email": user.email,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "roles": roles,  
        }
        return Response(data, status=status.HTTP_200_OK)


class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()  # Obtiene la respuesta original de dj-rest-auth
        user = self.user  # Usuario autenticado
        
        # Obtiene los nombres de los roles (grupos)
        roles = list(user.groups.values_list("name", flat=True))

        # Modifica la respuesta para incluir los roles
        response.data["roles"] = roles
        return response