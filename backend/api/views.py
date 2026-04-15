from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from .models import Service, BlogPost, GalerieCategorie, GalerieImage, Contact, InfoSite, Statistique, MembreEquipe, Campagne, Partenaire
from .serializers import (
    ServiceSerializer, BlogPostListSerializer, BlogPostDetailSerializer,
    GalerieCategorieSerializer, GalerieImageSerializer,
    ContactSerializer, ContactAdminSerializer, InfoSiteSerializer,
    BlogPostAdminSerializer, GalerieImageAdminSerializer, StatistiqueSerializer,
    MembreEquipeSerializer, CampagneSerializer, PartenaireSerializer, PartenaireAdminSerializer,
)


# --- Public views ---

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(actif=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(publie=True)
    serializer_class = BlogPostListSerializer
    permission_classes = [AllowAny]


class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(publie=True)
    serializer_class = BlogPostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class GalerieCategorieListView(generics.ListAPIView):
    queryset = GalerieCategorie.objects.all()
    serializer_class = GalerieCategorieSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class GalerieImageListView(generics.ListAPIView):
    serializer_class = GalerieImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = GalerieImage.objects.filter(publie=True)
        categorie = self.request.query_params.get('categorie')
        if categorie:
            queryset = queryset.filter(categorie_id=categorie)
        return queryset


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]


class InfoSiteView(generics.GenericAPIView):
    serializer_class = InfoSiteSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        info = InfoSite.objects.first()
        if info:
            serializer = self.get_serializer(info)
            return Response(serializer.data)
        return Response({}, status=status.HTTP_200_OK)


class EquipeListView(generics.ListAPIView):
    queryset = MembreEquipe.objects.filter(actif=True)
    serializer_class = MembreEquipeSerializer
    permission_classes = [AllowAny]
    pagination_class = None


# Partenaires public
class PartenaireListView(generics.ListAPIView):
    queryset = Partenaire.objects.filter(actif=True)
    serializer_class = PartenaireSerializer
    permission_classes = [AllowAny]
    pagination_class = None


# --- Auth views ---

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
            })
        return Response(
            {'detail': 'Identifiants invalides ou accès non autorisé.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Déconnecté.'})


class MeView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        })


class CSRFView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'csrfToken': get_token(request)})


# --- Admin CRUD views ---

class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            'services': Service.objects.count(),
            'blog_posts': BlogPost.objects.count(),
            'blog_published': BlogPost.objects.filter(publie=True).count(),
            'galerie_images': GalerieImage.objects.count(),
            'galerie_categories': GalerieCategorie.objects.count(),
            'contacts': Contact.objects.count(),
            'contacts_non_lus': Contact.objects.filter(lu=False).count(),
            'statistiques': Statistique.objects.count(),
        })


# Services admin
class AdminServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None


class AdminServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminUser]


# Blog admin
class AdminBlogListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostAdminSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class AdminBlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostAdminSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


# Galerie admin
class AdminCategorieListCreateView(generics.ListCreateAPIView):
    queryset = GalerieCategorie.objects.all()
    serializer_class = GalerieCategorieSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None


class AdminCategorieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalerieCategorie.objects.all()
    serializer_class = GalerieCategorieSerializer
    permission_classes = [IsAdminUser]


class AdminGalerieListCreateView(generics.ListCreateAPIView):
    queryset = GalerieImage.objects.all()
    serializer_class = GalerieImageAdminSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class AdminGalerieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GalerieImage.objects.all()
    serializer_class = GalerieImageAdminSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


# Contact admin
class AdminContactListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactAdminSerializer
    permission_classes = [IsAdminUser]


class AdminContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactAdminSerializer
    permission_classes = [IsAdminUser]


# Statistiques public
class StatistiqueListView(generics.ListAPIView):
    queryset = Statistique.objects.filter(actif=True)
    serializer_class = StatistiqueSerializer
    permission_classes = [AllowAny]
    pagination_class = None


# Équipe admin
class AdminEquipeListCreateView(generics.ListCreateAPIView):
    queryset = MembreEquipe.objects.all()
    serializer_class = MembreEquipeSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None


class AdminEquipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MembreEquipe.objects.all()
    serializer_class = MembreEquipeSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


# Campagnes public
class CampagneListView(generics.ListAPIView):
    serializer_class = CampagneSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = Campagne.objects.all()
        produit = self.request.query_params.get('produit')
        session = self.request.query_params.get('session')
        if produit:
            qs = qs.filter(produit=produit)
        if session:
            qs = qs.filter(session=session)
        return qs


# Campagnes admin
class AdminCampagneListCreateView(generics.ListCreateAPIView):
    serializer_class = CampagneSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None

    def get_queryset(self):
        qs = Campagne.objects.all()
        produit = self.request.query_params.get('produit')
        session = self.request.query_params.get('session')
        if produit:
            qs = qs.filter(produit=produit)
        if session:
            qs = qs.filter(session=session)
        return qs


class AdminCampagneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Campagne.objects.all()
    serializer_class = CampagneSerializer
    permission_classes = [IsAdminUser]


# Statistiques admin
class AdminStatistiqueListCreateView(generics.ListCreateAPIView):
    queryset = Statistique.objects.all()
    serializer_class = StatistiqueSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None


class AdminStatistiqueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Statistique.objects.all()
    serializer_class = StatistiqueSerializer
    permission_classes = [IsAdminUser]


# Partenaires admin
class AdminPartenaireListCreateView(generics.ListCreateAPIView):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireAdminSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = None


class AdminPartenaireDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partenaire.objects.all()
    serializer_class = PartenaireAdminSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


# InfoSite admin
class AdminInfoSiteView(APIView):
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        info = InfoSite.objects.first()
        if info:
            serializer = InfoSiteSerializer(info)
            return Response(serializer.data)
        return Response({})

    def put(self, request):
        info, _ = InfoSite.objects.get_or_create(pk=1)
        serializer = InfoSiteSerializer(info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def _serialize_user(u):
    return {
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'is_staff': u.is_staff,
        'is_superuser': u.is_superuser,
        'is_active': u.is_active,
        'date_joined': u.date_joined,
        'last_login': u.last_login,
    }


class AdminUserListCreateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        return Response([_serialize_user(u) for u in users])

    def post(self, request):
        username = request.data.get('username', '').strip()
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '')
        is_staff = bool(request.data.get('is_staff', True))

        if not username or not password:
            return Response({'detail': "Nom d'utilisateur et mot de passe requis."}, status=400)
        if len(password) < 8:
            return Response({'detail': 'Le mot de passe doit contenir au moins 8 caractères.'}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({'detail': "Ce nom d'utilisateur est déjà utilisé."}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff,
        )
        return Response(_serialize_user(user), status=201)


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def _get(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def patch(self, request, pk):
        user = self._get(pk)
        if not user:
            return Response({'detail': 'Utilisateur non trouvé.'}, status=404)
        if 'username' in request.data:
            new_username = request.data['username'].strip()
            if User.objects.filter(username=new_username).exclude(pk=pk).exists():
                return Response({'detail': "Ce nom d'utilisateur est déjà utilisé."}, status=400)
            user.username = new_username
        if 'email' in request.data:
            user.email = request.data['email'].strip()
        if 'is_staff' in request.data:
            user.is_staff = bool(request.data['is_staff'])
        if 'is_active' in request.data:
            user.is_active = bool(request.data['is_active'])
        user.save()
        return Response(_serialize_user(user))

    def delete(self, request, pk):
        user = self._get(pk)
        if not user:
            return Response({'detail': 'Utilisateur non trouvé.'}, status=404)
        if user.pk == request.user.pk:
            return Response({'detail': 'Vous ne pouvez pas supprimer votre propre compte.'}, status=400)
        user.delete()
        return Response(status=204)


class AdminUserChangePasswordView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'Utilisateur non trouvé.'}, status=404)
        new_password = request.data.get('new_password', '')
        if len(new_password) < 8:
            return Response({'detail': 'Le mot de passe doit contenir au moins 8 caractères.'}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Mot de passe modifié avec succès.'})
