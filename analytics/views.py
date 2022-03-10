from django.shortcuts import render
from rest_framework.views import APIView
from backend.custom_methods import IsAuthenticatedCustom
from .models import ActiveUser


class AddActiveUser(APIView):
    permission_classes = (IsAuthenticatedCustom, )

    def post(self, request):
        """ This route would add a user to the list of user for the day """
        # Getting the user that is logged
        user = request.user

        user_list  = ActiveUser.objects.get()

        if user_list:
            ActiveUser.objects.update()



