from django.shortcuts import render
from django.http import JsonResponse #this is for the baseic jsonresponse  
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import MyTokenPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework.exceptions import AuthenticationFailed
import requests
from django.core.files.storage import FileSystemStorage
from .utils.PredictLandmark import imglandmark
from ..models import Place
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class view:
    @api_view(['GET'])
    def getRoutes(request):
        routes=[
            'api/token',
            'api/token/refresh'
        ]
        #return JsonResponse(routes,safe=False)
        return Response(routes)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenPairSerializer

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        try:
            # Extract the token from the request
            token = request.data.get("token")
            # Validate the token
            UntypedToken(token)  # This raises an exception if the token is invalid
            return Response({"valid": True}, status=200)
        except AuthenticationFailed:
            return Response({"valid": False}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    import os
    if request.method == 'POST' and request.FILES['image']:
        image_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_file.name, image_file)
        # Get the full file path
        full_file_path = os.path.join(fs.location, filename)
        #image_path = fs.url(filename)
        place_name,details = recognize_place(full_file_path)
        print(f"The Place name is {place_name}")
        # print(f"888888888888888888888888888888{place_name}")
        # place_details = fetch_place_details(place_name)

        place = Place(
            name=details.get('title') if details else '',
            location=full_file_path,  # Update as needed
            image=image_file,
            construction_date=None,  # Update based on logic or API
            description=details.get('extract', '') if details else '',
            user=request.user  # Assuming you have user authentication
        )
        place.save()

        return render(request, 'imgrecognizer/result.html', {'place_name': place_name, 'place_details': details, 'place': place})

    return render(request, 'imgrecognizer/upload.html')

def recognize_place(image_path):
    # Dummy function for recognizing place; replace with actual logic
    print(f"the file image {image_path}")
    landmark=imglandmark(image_path)
    placedetails=landmark.predict_landmark()
    print(f"5555555555555555555{placedetails}")
    if(placedetails):
        mostSutableLandmark=placedetails[0][0]
        mostSutableLandmark=mostSutableLandmark.replace(' ','_')
        details=landmark.get_wikidata_details(mostSutableLandmark)
        #print(f"================={mostSutableLandmark} details=================\n{details}")
        print(f"\nPredictions for image: {image_path}")
        for landmarktxt, confidence in placedetails:
            print(f"{landmarktxt}: {confidence:.2f}")
        #landmark.plot_predictions()
        
    
    
    return placedetails,details