from rest_framework.viewsets import ModelViewSet
from backend.custom_methods import IsAuthenticatedCustom
from .serializers import (Answers, AnswerSerializer, Question, QuestionsSerializer, )
from django.db.models import Q
import re

# Perform select and prefetch 

class QuestionView(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = (IsAuthenticatedCustom, )


    def get_queryset(self):
        if self.request.method.lower() != "get":
            return self.queryset

        data = self.request.query_params.dict()
        data.pop("page", None)
        keyword = data.pop("keyword", None)

        if keyword:
            search_fields = (
                "user__user__username", 
                "question_text", 
                "question_category__name",
            )

            query = self.get_query(keyword, search_fields)

            try:
                return self.queryset.filter(query).filter(**data).distinct().order_by("user__created_at")
            except Exception as e:
                raise Exception(e)

        return self.queryset.filter(**data).distinct().order_by("user__created_at")

    @staticmethod
    def get_query(query_string, search_fields):
        ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.

        '''
        query = None  # Query to search for every search term
        terms = QuestionView.normalize_query(query_string)
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



class AnswerView(ModelViewSet):
    queryset = Answers.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticatedCustom, )



# Get the the list of people that reacted to a question 
# Get the the list of people that reacted to a answer
# To check if a user has liked a question
# To check if a user has liked a answer
# Follow a user