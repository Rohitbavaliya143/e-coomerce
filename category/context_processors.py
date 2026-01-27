from .models import category
def menu_categories(request):
    return{
        'menu_categories':category.objects.all()
    }