from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render
from rest_framework.parsers import JSONParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import os
from django.conf import settings # STATIC_ROOT
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets, status
from .models import Eval
from .models import Team
from .models import CustomUser
from .serializers import EvalSerializer
from djoser.views import UserViewSet
from .serializers import CustomUserCreateSerializer
from .serializers import TeamSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authentication import BasicAuthentication

import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.stats.meta_analysis import (
    effectsize_smd,
    effectsize_2proportions,
    combine_effects,
    _fit_tau_iterative,
    _fit_tau_mm,
    _fit_tau_iter_mm,
)
import json

User = get_user_model()


class CustomUserCreateView(UserViewSet):
    """
    Class which manages API calls on the users table
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserCreateSerializer

    @action(detail=False, methods=['get'], url_path='userslist')
    def userslist(self, request):
        """
        Returns the list of users
        """
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='bulk-delete')
    def bulk_delete(self, request):
        """
        Retrieve the user id to delete it from the database
        """
        user_ids = request.data.get('ids', [])
        if not user_ids:
            return Response({"error": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.filter(id__in=user_ids).delete()
        return Response({"message": "Users deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['put'], url_path='')
    def update_user(self, request, pk=None):
        """
        Retrieves user information to update in the database
        """
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        print("data", request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EvalViewSet(viewsets.ModelViewSet):
    """
    Class which manages API calls on the eval table
    """
    queryset = Eval.objects.all()
    serializer_class = EvalSerializer

    def create(self, request):
        """
        Retrieves eval information to create in the database
        """
        data = request.data  # Données envoyées depuis le frontend
        for eval_data in data:
            System_id = eval_data.get('System_id')
            Round = eval_data.get('Round')
            Query = eval_data.get('Query')
            Metric = eval_data.get('Metric')
            defaults = {
                'Value': eval_data.get('Value'),
                'System_collection': eval_data.get('System_collection'),
                'Team_id': eval_data.get('Team')
            }

            # Utiliser update_or_create pour mettre à jour ou créer l'enregistrement
            obj, created = Eval.objects.update_or_create(
                System_id=System_id,
                Round=Round,
                Query=Query,
                Metric=Metric,
                defaults=defaults
            )

        return Response({"message": "Les données ont été ajoutées/mises à jour avec succès."},
                        status=status.HTTP_201_CREATED)

    def delete(self, request):
        """
        Retrieve the eval id to delete it from the database, if there is no id received, it deletes everything in the table
        """
        eval_ids = request.data.get('ids', [])
        if not eval_ids:
            Eval.objects.all().delete()
            return Response({"message": "All Evaluations deleted."}, status=status.HTTP_200_OK)

        Eval.objects.filter(id__in=eval_ids).delete()
        return Response({"message": "Evaluations on this system deleted successfully."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='average-values')
    def average_values(self, request):
        """
        Filters the table based on query, system, round(s), and metric to calculate the mean, standard deviation, median, max, and min.
        """
        queries = request.query_params.getlist('query')
        rounds = request.query_params.getlist('round')
        metric = request.query_params.get('metric')
        system = request.query_params.get('system')

        print(f"Queries: {queries}, Rounds: {rounds}, Metric: {metric}, System: {system}")

        queryset = Eval.objects.all()
        print(f"Filtered before queryset count: {queryset.count()}")
        if queries:
            queryset = queryset.filter(Query__in=queries)
            print(f"Filtered queries queryset count: {queryset.count()}")
        if rounds:
            print(
                f"Available Rounds after filtering by queries: {queryset.values_list('Round', flat=True).distinct()}")
            queryset = queryset.filter(Round__in=rounds)
            print(f"Filtered queries rounds queryset count: {queryset.count()}")
        if metric:
            # Debugging: Print distinct metrics available after filtering by rounds and queries
            print(
                f"Available Metrics after filtering by rounds and queries: {queryset.values_list('Metric', flat=True).distinct()}")

            queryset = queryset.filter(Metric=metric)
            print(metric)
            print(f"Filtered queries rounds metric queryset count: {queryset.count()}")
        if system:
            queryset = queryset.filter(System_id=system)
            print(f"Filtered all queryset count: {queryset.count()}")

        print(f"Filtered queryset count: {queryset.count()}")
        print({queryset})

        values = queryset.values_list('Value', flat=True)
        # Convert values to float, ignoring non-numeric values
        numeric_values = []
        for value in values:
            try:
                numeric_values.append(float(value))
            except ValueError:
                continue

        if not numeric_values:
            return Response({"error": "No numeric data found for the specified filters."},
                            status=status.HTTP_404_NOT_FOUND)

        average_value = round(sum(numeric_values) / len(numeric_values), 4)
        median_value = round(np.median(numeric_values), 4)
        std_deviation = round(np.std(numeric_values), 4)
        max_value = round(max(numeric_values), 4)
        min_value = round(min(numeric_values), 4)

        return Response({
            "average_value": average_value,
            "median_value": median_value,
            "std_deviation": std_deviation,
            "max_value": max_value,
            "min_value": min_value
        }, status=status.HTTP_200_OK)


class TeamViewSet(viewsets.ModelViewSet):
    """
    Class which manages API calls on the team table
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

