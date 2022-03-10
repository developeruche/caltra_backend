#  @developeruche

# Import useful libs
import jwt
from .models import Jwt, CustomUser
from datetime import datetime, timedelta
from django.conf import settings
import random
import string
from rest_framework.views import APIView
from .serializers import (
    LoginSerializer, RegisterSerializer, RefreshSerializer,
     UserProfileSerializer, UserProfile
)
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .authentication import Authentication
from backend.custom_methods import IsAuthenticatedCustom, IsAuthenticatedOrReadCustom
from rest_framework.viewsets import ModelViewSet
import re
from django.db.models import Q
from django.core.signing import TimestampSigner


# Some util functions
def get_random(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_access_token(payload):
    return jwt.encode(
        {"exp": (datetime.now() + timedelta(minutes=50)).timestamp(), **payload},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def get_refresh_token():
    return jwt.encode(
        {"exp": (datetime.now() + timedelta(days=30)).timestamp(), "data": get_random(10)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )


def decodeJWT(bearer):
    if not bearer:
        return None

    token = bearer[7:]
    # decoded = jwt.decode(token, key=settings.SECRET_KEY)
    decoded = Authentication.verify_token(token)
    
    if decoded:
        try:
            return CustomUser.objects.get(id=decoded["user_id"])
        except Exception:
            return None




class LoginView(APIView):
    """ 
        When a user login they would receive an access token 
        and a refresh token which would be use later    
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'])

        if not user:
            return Response({"error": "Invalid username or password"}, status="400")

        # Deleting the first tokens from the storage
        Jwt.objects.filter(user_id=user.id).delete()

        # Insert new tokens to the storage
        access = get_access_token({"user_id": user.id})
        refresh = get_refresh_token()

        Jwt.objects.create(
            user_id=user.id, access=access.decode(), refresh=refresh.decode()
        )

        return Response({"access": access, "refresh": refresh})



class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        CustomUser.objects._create_user(**serializer.validated_data)

        
        # Create the time signed string
        application_name = "caltra"
        to_sign_data = f"{application_name}__{serializer.validated_data['email']}"
        signer = TimestampSigner(salt=settings.APP_SALT)
        signed_data = signer.sign(to_sign_data)

        # Send the email for verification


        return Response({"success": "User created.", "test": signed_data}, status=201)



class RefreshView(APIView):
    """ 
        The logic here is this, the access token last for just 5 min
        and when the access token is bad or expiry the use cannot 
        perform authenticated task again so the user sends the refresh
        token which expires in a 30 days, and the user would be given a
        new access token and the cycle would go on and on.
    """
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt = Jwt.objects.get(
                refresh=serializer.validated_data["refresh"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")

        if not Authentication.verify_token(serializer.validated_data["refresh"]):
            return Response({"error": "Token is invalid or has expired"})

        access = get_access_token({"user_id": active_jwt.user.id})
        refresh = get_refresh_token()

        active_jwt.access = access.decode()
        active_jwt.refresh = refresh.decode()
        active_jwt.save()

        return Response({"access": access, "refresh": refresh})


# Big work still to be done on this
class UserProfileView(ModelViewSet):
    queryset = UserProfile.objects.all() 
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticatedCustom, )




    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        if keyword:
            search_fields = (
                "user__username", "first_name", "last_name", 
                "user__email", "campus__name", "tel_number",
                "caption", "about"
            )

            query = self.get_query(keyword, search_fields)

            print(query)
            try:
                return self.queryset.filter(query).filter(**data).exclude(
                    Q(user__is_superuser=True)).distinct().order_by("user__created_at")
            except Exception as e:
                raise Exception(e)

        return self.queryset.filter(**data).exclude(
            Q(user__is_superuser=True)).distinct().order_by("user__created_at")

    @staticmethod
    def get_query(query_string, search_fields):
        ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.

        '''
        query = None  # Query to search for every search term
        terms = UserProfileView.normalize_query(query_string)
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query

        return query

    @staticmethod
    def normalize_query(query_string, findterms=re.compile(r'"([^"]+)"|(\S+)').findall, normspace=re.compile(r'\s{2,}').sub):
        ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
            and grouping quoted words together.
            Example:

            >>> normalize_query('  some random  words "with   quotes  " and   spaces')
            ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

        '''

        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]





class MeView(APIView):
    """ 
        This router would return the user ID of the current user
    """
    permission_classes = (IsAuthenticatedCustom, )
    serializer_class = UserProfileSerializer

    def get(self, request):
        data = {}
        try:
            data = self.serializer_class(request.user.user_profile).data #This would be returned if the user profile has been created
        except Exception:
            data = {
                "user": {
                    "id": request.user.id
                }
            }
        return Response(data, status=200)


class LogoutView(APIView): 
    """ 
        When some loggout and the access token is not deleted from the frontend the user can still do any modification the user wants till the access token expires when is going to be less than 5 mins
    """
    permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        user_id = request.user.id

        Jwt.objects.filter(user_id=user_id).delete()

        return Response("logged out successfully", status=200)


class HasCreatedProfile(APIView):
    permission_classes = (IsAuthenticatedCustom, )

    def get(self, request):
        user_id = request.user.id
        
        try:
            UserProfile.objects.get(user_id=user_id)
            return Response({"success": "Profile do exist"}, status=200) 
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not created"}, status=200) 


class PreVerEmail(APIView):
    def get(self, request, email):        
        # Create the time signed string
        application_name = "caltra"
        to_sign_data = f"{application_name}__{email}"
        signer = TimestampSigner(salt=settings.APP_SALT)
        signed_data = signer.sign(to_sign_data)
        
        # send the the email
        

        return Response({"success": signed_data}, status=200)



class VerifyEmail(APIView):
    """ 
        This would set the state of the user to active because they have chosen the email is there's
        (This would mail the user a time signed link which onclick of this link the account would be activate)
    """
    
    def post(self, request, auth):
        # Ver the auth string 
        signer = TimestampSigner(salt=settings.APP_SALT)

        try: 
            signer.unsign(auth, max_age=5180)
        except:
            raise Exception("Token is Expired or invalid.")

        # activate the account
        user_id = request.user.id
        CustomUser.objects.filter(id=user_id).update(is_active=True)

        return Response({'success': "Email verification done"}, status=200)



class PreResetPassword(APIView):
    """ 
        This is the route the user would hit first before the main reset password route it would create the signed token and
        send the email to the user email
    """
    def post(self, request):
        """ This function would receive the email from the request data  as json """
        email = request.data['email']
        # Creating the signed token
        application_name = 'caltra'
        to_sign_data = f"{application_name}__{email}_PASSWORD_RESET"
        print(to_sign_data)
        signer = TimestampSigner(salt=settings.APP_SALT)
        signed_data = signer.sign(to_sign_data)

        # sending the email

        return Response({"success": "email sent.", 'data': signed_data})



class ResetPassword(APIView):
    """ 
        This is where the main work is done the (This token string is verified and) (The password is then changed) 
    """
    def post(self, request, auth):
        """ 1. Password string would be passed from the url
            2. Email would be passed from the request body as JSON
        """
        email = request.data['email']
        password = request.data['password']

        

        CustomUser.objects.get(email=email)
        # Comfirm for the user that have this email
        try:
            CustomUser.objects.get(email=email)
        except:
            return Response({"error": "Email not found."})
        
        

        # Verifing the token string
        signer = TimestampSigner(salt=settings.APP_SALT)

        
        try: 
            signer.unsign(auth, max_age=600)
        except:
            raise Exception("Token is Expired or invalid.")
        
        
        # Changing the password
        try:
            CustomUser.objects.update_password(email=email, password=password)
        except:
            return Response({"error": "An error occurred while trying tot change the password."})

        # send an email telling the user that the password have been changed successfully

        return Response({"success": "Password has been changed successfully."})


""" How the get the type of device and ip address of the device trying the change the password. """