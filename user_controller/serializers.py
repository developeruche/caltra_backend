from rest_framework import serializers
from .models import (CustomUser, CategoryOfInterest, 
                ProfileImage, UserProfile, 
                Campus, )


# UTIL serializers
class ProfileImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileImage
        fields = "__all__"

class CategoryOfInterestSerializer(serializers.ModelSerializer): #The function of this serializer is just displaying the category of interest when the user visit the profile page.
    
    class Meta:
        model = CategoryOfInterest
        fields = "__all__"

class CampusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = "__all__"




# Input Action Serializers
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer): #this would serializer the refresh token so access can be renewed
    refresh = serializers.CharField()



# Model Serializers
class CustomUserSerializer(serializers.ModelSerializer): #this serializer would be used to render the save users in the database

    class Meta:
        model = CustomUser
        exclude = ("password", )


class UserProfileSerializer(serializers.ModelSerializer): #this serializer would be used to update and render the UsersProfile
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    profile_picture = ProfileImageSerializer(read_only=True)
    profile_picture_id = serializers.IntegerField(
        write_only=True, required=False)
    interest = CategoryOfInterestSerializer(many=True)
    campus = CampusSerializer(read_only=True)
    campus_id = serializers.IntegerField(write_only=True)  
    followers = serializers.SerializerMethodField("get_followers_count")

    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_followers_count(self, obj):
        return obj.followers.count()

    def create(self, validated_data):
        # Removing the intrest list from the validated data
        interest_list = validated_data.pop('interest')
        inr = []

        # Saving the validated data
        u_profile = UserProfile.objects.create(**validated_data)

        # Looping through the array
        for i in interest_list:
            try: 
                p = CategoryOfInterest.objects.get(**i)
                inr.append(p)
            except Exception as e:
                raise Exception(e)
            
        u_profile.interest.set(inr)

        return u_profile
    
    def update(self, instance, validated_data):
        to_set_data = validated_data.pop('interest', instance.interest) 
        inr = []

        for i in to_set_data:
            try: 
                p = CategoryOfInterest.objects.get(**i)
                inr.append(p)
            except Exception as e:
                raise Exception(e)
        
        instance.interest.set(inr)
        return super().update(instance, validated_data)