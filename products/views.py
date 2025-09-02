from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Special

@api_view(['GET'])
def menu_api(request):
    menu = [
        {
            "name" : "Panner Butter Masala",
            "description" : "Soft panner cubs in creamy tomato gravy",
            "price" : "180.00"
        },

        {
            "name" : "Veg Biryani",
            "description" : "Aromatic rice with mixed vegetables and spices",
            "price" : "150.00"
        },

        {
            "name" : "Masala Dosa",
            "description" : "Crispy dosa stuffed with spicy mashed potatoes",
            "price" : 70.00
        }

    ]
    # Get page number from request ( default = 1 )
    page_number = request.GET.get('page',1)
    paginator = Paginator(menu, 2 )

    try:
        page_obj = paginator.page(page_number)
    except:
        page_obj = paginator.page(1)

    data = {
        "count": paginator.count,
        "total_pages": page_obj.number,
        "current_page": page_obj.number,
        "results": list(page_obj.object_list),
    }
    return Response(data)

def todays_specials(request):
    specials = Special.objects.filter(date=date.today())

    return render(request,'products/specials.html',{'specials':specials})

def about_chefs(request):
    from .models import Chef
    chefs = Chef.objects.all()
    return render(request,'products/chefs.html',{'chefs':chefs})
