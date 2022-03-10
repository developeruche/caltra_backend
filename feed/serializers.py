from rest_framework import serializers
from .models import FeedAnswersImage, FeedQuestionImage, Answers, Question, FeedQuestionVideo, FeedAnswerVideo
from user_controller.serializers import UserProfileSerializer, CategoryOfInterest, CategoryOfInterestSerializer, UserProfile


class FeedAnswersImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FeedAnswersImage
        fields = "__all__"


class FeedQuestionImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FeedQuestionImage
        fields = "__all__"


class FeedQuestionVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedQuestionVideo
        fields = "__all__"


class FeedAnswerVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedAnswerVideo
        fields = "__all__"



class QuestionsSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    question_image = FeedQuestionImageSerializer(read_only=True, many=True)
    question_image_ids = serializers.ListField(write_only=True)
    question_category = CategoryOfInterestSerializer(many=True)
    reaction = serializers.SerializerMethodField("get_reaction_count")
    question_video = FeedQuestionVideoSerializer(read_only=True)
    question_video_id = serializers.IntegerField(write_only=True, required=False)


    def get_reaction_count(self, obj):
        return obj.reaction.count()
    
    class Meta:
        model = Question
        fields = "__all__"

    def create(self, validated_data):
        # removing the (question_image_ids, question_category)
        q_category_list = validated_data.pop('question_category')
        q_image_ids_list = validated_data.pop('question_image_ids') #this is an array


        qcl = []
        qil = []

        # Saving the validated data
        v_question = Question.objects.create(**validated_data)
        
        # Looping through the array(Working on the category)
        for i in q_category_list:
            try: 
                p = CategoryOfInterest.objects.get(**i)
                qcl.append(p)
            except:
                raise Exception("Oops, Something went wrong.")
        
        # Looping through the array(Working on the images)
        for i in q_image_ids_list:
            try: 
                p = FeedQuestionImage.objects.get(id=i)
                qil.append(p)
            except:
                raise Exception("Oops, Something went wrong.")
        
        v_question.question_category.set(qcl)
        v_question.question_image.set(qil)

        return v_question

    def update(self, instance, validated_data):
        to_set_data = validated_data.pop('question_category')
        to_set_data_two = validated_data.pop('question_image_ids')

        qlc = []
        qil = []


        for i in to_set_data:
            try: 
                p = CategoryOfInterest.objects.get(**i)
                qlc.append(p)
            except Exception as e:
                raise Exception(e)

        for i in to_set_data_two:
            try: 
                p = FeedQuestionImage.objects.get(id=i)
                qil.append(p)
            except Exception as e:
                raise Exception(e)

        
        instance.question_category.set(qlc)
        instance.question_image.set(qil)

        return super().update(instance, validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    answer_image = FeedAnswersImageSerializer(read_only=True, many=True)
    answer_image_ids = serializers.ListField(write_only=True, )
    answer_video = FeedAnswerVideoSerializer(read_only=True)
    answer_video_id = serializers.IntegerField(write_only=True, required=False)
    question = QuestionsSerializer(read_only=True)
    question_id = serializers.IntegerField(write_only=True)
    reaction = serializers.SerializerMethodField("get_reaction_count")
    

    class Meta:
        model = Answers
        fields = "__all__"


    def get_reaction_count(self, obj):
        return obj.reaction.count()

    def create(self, validated_data):
        # removing the image ids
        a_image_ids_list = validated_data.pop("answer_image_ids")

        if a_image_ids_list:
            aiil = []


            # Saving the first stage validated data
            a_answer = Answers.objects.create(**validated_data)

            # Looping through the array
            for i in a_image_ids_list:
                try: 
                    p = FeedAnswersImage.objects.get(id=i)
                    aiil.append(p)
                except Exception as e:
                    raise Exception(e)

            a_answer.answer_image.set(aiil)

            return a_answer



    def update(self, instance, validated_data):
        to_set_data = validated_data.pop('answer_image_ids')


        if to_set_data:
            aii = []

            for i in to_set_data:
                try:
                    p = FeedAnswersImage.objects.get(id=i)
                    aii.append(p)
                except Exception as e:
                    raise Exception(e)

            instance.answer_image.set(aii)
            
            return super().update(instance, validated_data)










    