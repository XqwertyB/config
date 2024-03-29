from .models import (
    Announcement,
    Category,
    Costumer,
    TopWishList

)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .filter import PriceModelFilter
from .serializers import AnnouncementSerializer, RegistrationSerializer, LoginSerializer, CategorySeralizer
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from django_filters.rest_framework import DjangoFilterBackend


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class AnnouncementView(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sub_category_id', 'price', 'organization_id']
    filterset_class = PriceModelFilter
    permission_classes = [permissions.AllowAny]


class AnnouncementViewCreate(generics.CreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySeralizer
    permission_classes = [permissions.AllowAny]

def get_favorite_vacancies(request):
    customer_id = request.GET.get('customer_id')
    favorite_vacancies = TopWishList.objects.filter(costumer_id=customer_id).values_list('announcement_id', flat=True)
    return JsonResponse({'favorite_vacancies': list(favorite_vacancies)})



@csrf_exempt
def manage_favorite_vacancy(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        announcement_id = request.POST.get('announcement_id')

        try:

            favorite_vacancy = TopWishList.objects.get(customer_id=customer_id, announcement_id=announcement_id)
            favorite_vacancy.delete()
            return JsonResponse({'message': 'Vacancy removed from favorites'})
        except TopWishList.DoesNotExist:

            favorite_vacancy = TopWishList(customer_id=customer_id, announcement_id=announcement_id)
            favorite_vacancy.save()
            return JsonResponse({'message': 'Vacancy added to favorites'})
