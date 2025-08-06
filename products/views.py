from rest_framework.decorators omport api_view
from rest_framework.response import Response

@api_view(['GET'])
def menu_list(request):
    menu = [
        {
            "name" : "Panner Butter Masala",
            "description" : "Soft panner cubs in creamy toamto gravy",
            "price" : "180.00"
        },

        {
            "name" : "Veg Biryni",
            "description" : "Aromatic rice with mixed vegetables and spices",
            "price" : "150.00"
        },

        {
            "name" : "Masala Dosa",
            "description" : "Crispy dosa stoffed with spicy mashed patatoes",
            "price" : 70.00
        }

    ]
    return Response(menu)