from django.shortcuts import render
from rest_framework import views,response,status
import json

# Create your views here.



class ReccomendView(views.APIView):

    def get(self,request,p_user_id,format=None):

        l_file_path = 'static/users.json'

        l_user_data = None

        with open(l_file_path, 'r') as file:
            l_user_data = json.load(file)

        l_users_list = l_user_data["users"]

        l_current_user = l_users_list[p_user_id - 1]

        l_current_user_interest = l_current_user["interests"]

        l_recommendation_list = []

        l_interest_multiplier = {}

        for interest, value in l_current_user_interest.items():
            l_interest_multiplier[interest] = value/100

        for person in l_users_list:

            score = 0

            l_interest_dict = person["interests"]

            for a in l_interest_dict:

                if a in l_interest_multiplier:
                    score += l_interest_dict[a]*l_interest_multiplier[a]
                    score -= abs(l_current_user['age'] - person['age'])/2

            l_recommendation_list.append({"id": person["id"], "score" : score})

        l_recommendation_list = sorted(l_recommendation_list, key=lambda x: x["score"], reverse=True)

        l_result = []

        for user in l_recommendation_list:
            l_result.append(l_users_list[user["id"] - 1])

        return response.Response(l_result[0:5], status=status.HTTP_200_OK)






        