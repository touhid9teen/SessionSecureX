from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from .serializers import TodoSerializer, RegistationSerializer
from .models import TodoModels
from django.middleware.csrf import get_token
from django.http import JsonResponse


class TodoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Assign the todo to the logged-in user
        request.data['user'] = request.user.id
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Fetch todos for the logged-in user
        todos = TodoModels.objects.filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)


class TodoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Fetch todo for the logged-in user
            todo = TodoModels.objects.get(id=pk, user=request.user)
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TodoModels.DoesNotExist:
            return Response({"error": "Item does not exist"}, status=status.HTTP_404_NOT_FOUND)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Get CSRF token for the session
            csrf_token = get_token(request)
            response = JsonResponse({'message': 'Login successful'})
            # CSRF token and sessionid are managed by Django's middleware automatically
            response.set_cookie('csrftoken', csrf_token)
            return response
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout Successful"}, status=status.HTTP_200_OK)
