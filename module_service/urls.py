from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import TagView, TagModuleView, ModuleView


router = SimpleRouter()
router.register('tag', TagView, basename='tags')
router.register('tag-module', TagModuleView, basename='tag-modules')
router.register('module', ModuleView, basename='modules')

urlpatterns = router.urls + [

]
