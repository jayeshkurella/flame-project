from rest_framework import viewsets
from rest_framework.response import Response
from searchbar.models import data
from .serializer import SourceDataSerializer
from shapely.geometry import Polygon, mapping
from datetime import datetime
import os
from pystac import Catalog
from django.http import JsonResponse
from rest_framework.decorators import action
import rasterio
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
import pystac
import json
from rest_framework.pagination import PageNumberPagination
import os
import pytz
import datetime as dt
from rest_framework.viewsets import ViewSet
from django.db import connection
from django.http import JsonResponse
from rest_framework.decorators import api_view
from Logger import logger
from django.http import HttpResponseNotFound
from Logger import logger
from rest_framework.views import APIView

class StacViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        # = Catalog.from_file("./example-catalog/catalog.json")
        catalog = Catalog.from_file("./flames/stac-catalog")
        return Response(f"Stac App: {catalog.title}")

    def retrieve(self, request, *args, **kwargs):
        catalog = Catalog(
            id="tutorial-catalog",
            description="This catalog is a basic demonstration catalog utilizing a scene from SpaceNet 5.",
        )
        catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
        return Response(f"Stac Created: {catalog.title}")

def extract_state_from_url(img_download_url):
    try:
        # Split the URL by "/"
        url_parts = img_download_url.split("/")

        # Find the index of the first non-empty path component after the drive
        state_index = next((i for i, part in enumerate(url_parts[1:], start=2) if part), None)

        if state_index is not None and state_index < len(url_parts):
            # Extract the first non-empty path component as the state
            state = url_parts[state_index]
            print("------------state-*-*--",state)
            return state
        else:
            return None
    except Exception as e:
        print(f"An error occurred during state extraction from URL: {str(e)}")
        return None





# Function to add stac item in catalog added item is added in stac_catalog folder
@api_view(['POST'])
def add_item_to_stac(request):
        logging_data = dict(request.data)
        logger.debug(f"[API Call] {request.__class__.__name__} create Data: {logging_data}")
        # Assume that in request.data we got the request
        data = request.data
        print("**********", data)
      #  logging_data = dict(request.data)
       # logging_data['photo'] = 'DEBUG'
      #  logger.debug(f"[API Call] {request.__class__.__name__} create Data: {logging_data}")

        img_download_url = request.data.get("img_download_url", "")

        # Extract state and city from the request data or adjust this based on your data structure
        state = extract_state_from_url(img_download_url)
        print("---------------state------------",state)
        city = request.data.get("place_city", "")

        # Define the root directory for the STAC catalog
        catalog_root = "./stac-catalog"

        # Create sub-directories for state and city if they don't exist
        state_dir = os.path.join(catalog_root, state)
        state_dir=state_dir.replace("\\", "/")
        print("//////////////////state_dir////////",state_dir)
        city_dir = os.path.join(state_dir, city)
        city_dir=city_dir.replace("\\", "/")
        print("//////////////////city_dir////////",city_dir)
        os.makedirs(city_dir, exist_ok=True)

        

        image_name = os.path.split(img_download_url)[-1]
        item_id = f"{image_name}-item"
        
        # Extracting values from the request data
        properties = {
            "id": data.get("id", None),
            "major": data.get("major", ""),
            "submajor": data.get("submajor", ""),
            "minor": data.get("minor", ""),
            "subminor": data.get("subminor", ""),
            "grade": data.get("grade", ""),
            "file_formats": data.get("file_formats", ""),
            "type": data.get("type", ""),
            "source_description": data.get("source_description", ""),
            "place_city": data.get("place_city", ""),
            "year": data.get("year", ""),
            "publisher": data.get("publisher", ""),
            "path": data.get("path", ""),
            "collection": data.get("collection", ""),
            "collection_type": data.get("collection_type", ""),
            "soi_toposheet_no": data.get("soi_toposheet_no", ""),
            "grade1": data.get("grade1", ""),
            "data_resolution": data.get("data_resolution", ""),
            "ownership": data.get("ownership", ""),
            "is_processed": data.get("is_processed", ""),
            "short_descr": data.get("short_descr", ""),
            "descr":data.get("descr", ""),
            "img_service":data.get("img_service", ""),
            "img_dw": data.get("img_dw", ""),
            "map_service":data.get("map_service", ""),
            "map_dw": data.get("map_dw", ""),
            "publish_on": data.get("publish_on", ""),
            "thumbnail": data.get("thumbnail", ""),
            "source": data.get("source", ""),
            "created_id": data.get("created_id", ""),
            "created_date":data.get("created_date", ""),
            "modified_id": data.get("modified_id", ""),
            "modified_date": data.get("modified_date", ""),
            "deleted_id":data.get("deleted_id", ""),
            "deleted_date": data.get("deleted_date", ""),
            "img_download_url":data.get("img_download_url",""),
            "img_vis_url":data.get("img_vis_url",""),
            "shp_file_url":data.get("shp_file_url",""),
            "sub_collection":data.get("sub_collection",""),
            "urlalias":data.get("urlalias","")
            # Add other fields accordingly
        }

        # Path to the catalog file within the city directory
        catalog_path = "./stac-catalog/catalog.json"
        catalog_path=catalog_path.replace("\\", "/")
        print("catalog pstg is ----",catalog_path)

      
        catalog = pystac.Catalog.from_file(catalog_path)
        
        catalog = pystac.Catalog(id=f"{state}_{city}_stac-catalog", description=f"STAC Catalog for {state}, {city}")

        bbox, footprint = get_bbox_and_footprint(img_download_url)
        
        
        
        item = pystac.Item(
            id=item_id,
            geometry=footprint,
            bbox=bbox,
            datetime=datetime.now(),
            properties=properties,
        )

        catalog.add_item(item)
        item.add_asset(
            key="image",
            asset=pystac.Asset(
                href=img_download_url, media_type=pystac.MediaType.GEOTIFF
            ),
        )

        catalog.normalize_hrefs(city_dir)
        catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

        return Response({"status": "success", "message": "Item Added To STAC Catalog", "data": properties})
        
def get_bbox_and_footprint(img_download_url):
    with rasterio.open(img_download_url) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon(
            [
                [bounds.left, bounds.bottom],
                [bounds.left, bounds.top],
                [bounds.right, bounds.top],
                [bounds.right, bounds.bottom],
            ]
        )
    return bbox, mapping(footprint)



class SourceDataViewSet(viewsets.ModelViewSet):
    queryset=data.objects.all()
    serializer_class=SourceDataSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

#### Function to get all catalog data all files data from stac-catalog folder
@api_view(['GET'])
def search_catalog_common_metadata_api(request, **kwargs):
    logger.debug(f"[API Call] {request.__class__.__name__} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # Get limit and offset from the request query parameters
        limit = int(request.query_params.get('limit', 10))  # Default to 10 items per page
        offset = int(request.query_params.get('offset', 0))

        # List to store items
        items = []
        excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_path):
            main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is either a JSON file or a GeoTIFF file
                                    if file_name.endswith('-item.json') or file_name.endswith('.tiff'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        # Example: Read the content of JSON file
                                        if file_name.endswith('-item.json'):
                                            with open(file_path, 'r') as json_file:
                                                item_data = json.load(json_file)
                                                # Extract relevant information from properties dictionary
                                                properties = item_data.get('properties', {})
                                                response_data = {
                                                    "Major": properties.get("major", ""),
                                                    "Submajor": properties.get("submajor", ""),
                                                    "Minor": properties.get("minor", ""),
                                                    "SubMinor": properties.get("subminor", ""),
                                                    "Grade": properties.get("grade", ""),
                                                    "File_formats": properties.get("file_formats", ""),
                                                    "Type": properties.get("type", ""),
                                                    "Source_Description": properties.get("source_description", ""),
                                                    "place_city": properties.get("place_city", ""),
                                                    "year": properties.get("year", ""),
                                                    "publisher": properties.get("publisher", ""),
                                                    "Path": properties.get("path", ""),
                                                    "Collection": properties.get("collection", ""),
                                                    "Collection_type": properties.get("collection_type", ""),
                                                    "SOI_toposheet_no": properties.get("soi_toposheet_no", ""),
                                                    "Data_Resolution": properties.get("data_resolution", ""),
                                                    "Ownership": properties.get("ownership", ""),
                                                    "is_processed": properties.get("is_processed", ""),
                                                    "short_descr": properties.get("short_descr", ""),
                                                    "descr": properties.get("descr", ""),
                                                    "img_service": properties.get("img_service", ""),
                                                    "img_dw": properties.get("img_dw", ""),
                                                    "map_service": properties.get("map_service", ""),
                                                    "map_dw": properties.get("map_dw", ""),
                                                    "publish_on": properties.get("publish_on", ""),
                                                    "thumbnail": properties.get("thumbnail", ""),
                                                    "source": properties.get("source", ""),
                                                    "created_date": properties.get("created_date", ""),
                                                    "img_vis_url":properties.get("img_vis_url", ""),
                                                    "img_download_url":properties.get("img_download_url", ""),
                                                    "shp_file_url":properties.get("shp_file_url", ""),
                                                }

                                                items.append(response_data)

        # Return the list of items
        paginated_items = items[offset: offset + limit]

        # Return the paginated response
        response_data = {"data": paginated_items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   # except Exception as e:
      #  return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


 #   except Exception as e:
        # Handle exceptions and return an error response
    #    error_message = str(e)
    #    return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def search_catalog_metadata_by_key_api(request, key_to_search, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                

                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)
              
                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                  

                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)
                       

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)
                            print("-----------------",item_data)
                            # Check if the specified key is present in the properties section
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                properties_values = item_data['properties'].values()
                                if any(str(key_to_search).lower() in str(value).lower() for value in properties_values):
                                    print("File path:", file_path)
                                    items.append(item_data)



        # Return the list of items
        paginator = CustomPageNumberPagination()
        paginated_items = paginator.paginate_queryset(items, request)
        return paginator.get_paginated_response({'data': paginated_items})

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
    
# function for the search of side bar minor  data
@api_view(['GET'])
def sb_minor(request, **kwargs):
    logger.debug(f"[API Call] {request.__class__.__name__} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []
        # Folders to exclude from search
        excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Get limit and offset from query parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_path):
            main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is a JSON file
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        # Example: Read the content of JSON file
                                        with open(file_path, 'r') as json_file:
                                            item_data = json.load(json_file)

                                            # Check if the 'properties' key is present and is a dictionary
                                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                                # Check if any of the selectedItems is present in the 'properties' values
                                                properties_values = item_data['properties'].values()
                                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                                    formatted_item = format_item_data(item_data)
                                                    items.append(formatted_item)

        # Apply limit and offset
        paginated_items = items[offset:offset + limit]

        # Return the paginated response
        response_data = {"data": paginated_items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# function for the search of side bar sub_minor  data
@api_view(['GET'])
def sb_subminor(request, **kwargs):
    logger.debug(f"[API Call] {request.__class__.__name__} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []
        # Folders to exclude from search
        excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Get limit and offset from query parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_path):
            main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is a JSON file
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        # Example: Read the content of JSON file
                                        with open(file_path, 'r') as json_file:
                                            item_data = json.load(json_file)

                                            # Check if the 'properties' key is present and is a dictionary
                                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                                # Check if any of the selectedItems is present in the 'properties' values
                                                properties_values = item_data['properties'].values()
                                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                                    formatted_item = format_item_data(item_data)
                                                    items.append(formatted_item)

        # Apply limit and offset
        paginated_items = items[offset:offset + limit]

        # Return the paginated response
        response_data = {"data": paginated_items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# function for the search of side bar grade  data
@api_view(['GET'])
def sb_grade(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)

                            # Check if the 'properties' key is present and is a dictionary
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                # Check if any of the selectedItems is present in the 'properties' values
                                properties_values = item_data['properties'].values()
                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                    formatted_item = format_item_data(item_data)
                                    items.append(formatted_item)

        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# function for the search of side bar publisher  data
@api_view(['GET'])
def sb_publisher(request, **kwargs):
    logger.debug(f"[API Call] {request} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []
        # Folders to exclude from search
        excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Get the year from query parameters
        selected_year = request.GET.get('publisher', None)
        if selected_year is not None:
            try:
                selected_year = selected_year
            except ValueError:
                # If selected_year is not a valid integer, return an empty response
                return Response({"data": [], "count": 0}, status=status.HTTP_200_OK)
        
        # Get limit and offset from query parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_path):
            main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is a JSON file
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        # Example: Read the content of JSON file
                                        with open(file_path, 'r') as json_file:
                                            item_data = json.load(json_file)

                                            # Check if the 'properties' key is present and is a dictionary
                                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                                # Check if any of the selectedItems is present in the 'properties' values
                                                properties_values = item_data['properties'].values()
                                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                                    # Check if the year matches the selected year
                                                    if selected_year is None:
                                                        formatted_item = format_item_data(item_data)
                                                        items.append(formatted_item)
                                                    elif 'publisher' in item_data['properties']:
                                                        item_year = item_data['properties']['publisher']
                                                        try:
                                                            item_year = item_year
                                                            if item_year == selected_year:
                                                                formatted_item = format_item_data(item_data)
                                                                items.append(formatted_item)
                                                        except ValueError:
                                                            pass


        # Apply limit and offset
        paginated_items = items[offset:offset + limit]

        # Return the paginated response
        response_data = {"data": paginated_items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# function for the search of side bar place  data
@api_view(['GET'])
def sb_place(request, **kwargs):
    logger.debug(f"[API Call] {request} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []
        # Folders to exclude from search
        excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Get the year from query parameters
        selected_year = request.GET.get('place_city', None)
        if selected_year is not None:
            try:
                selected_year = selected_year
            except ValueError:
                # If selected_year is not a valid integer, return an empty response
                return Response({"data": [], "count": 0,"message":"No data Found"}, status=status.HTTP_200_OK)
        # Get limit and offset from query parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_path):
            main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is a JSON file
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        # Example: Read the content of JSON file
                                        with open(file_path, 'r') as json_file:
                                            item_data = json.load(json_file)

                                            # Check if the 'properties' key is present and is a dictionary
                                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                                # Check if any of the selectedItems is present in the 'properties' values
                                                properties_values = item_data['properties'].values()
                                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                                    if selected_year is None:
                                                        formatted_item = format_item_data(item_data)
                                                        items.append(formatted_item)
                                                    elif 'year' in item_data['properties']:
                                                        item_year = item_data['properties']['place_city']
                                                        try:
                                                            item_year = int(item_year)
                                                            if item_year == selected_year:
                                                                formatted_item = format_item_data(item_data)
                                                                items.append(formatted_item)
                                                        except ValueError:
                                                            pass

        # Apply limit and offset
        paginated_items = items[offset:offset + limit]

        # Return the paginated response
        response_data = {"data": paginated_items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# function for the search of side bar year  data
@api_view(['GET'])
def sb_year(request, **kwargs):
    logger.debug(f"[API Call] {request} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []
        # Folders to exclude from search
        excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Get the year from query parameters
        selected_year = request.GET.get('year', None)
        if selected_year is not None:
            try:
                selected_year = int(selected_year)
            except ValueError:
                # If selected_year is not a valid integer, return an empty response
                return Response({"data": [], "count": 0}, status=status.HTTP_200_OK)

        # Get limit and offset from query parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_path):
            main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is a JSON file
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        # Example: Read the content of JSON file
                                        with open(file_path, 'r') as json_file:
                                            item_data = json.load(json_file)

                                            # Check if the 'properties' key is present and is a dictionary
                                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                                # Check if any of the selectedItems is present in the 'properties' values
                                                properties_values = item_data['properties'].values()
                                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                                    # Check if the year matches the selected year
                                                    if selected_year is None:
                                                        formatted_item = format_item_data(item_data)
                                                        items.append(formatted_item)
                                                    elif 'year' in item_data['properties']:
                                                        item_year = item_data['properties']['year']
                                                        try:
                                                            item_year = int(item_year)
                                                            if item_year == selected_year:
                                                                formatted_item = format_item_data(item_data)
                                                                items.append(formatted_item)
                                                        except ValueError:
                                                            pass

        # Apply limit and offset
        paginated_items = items[offset:offset + limit]

        # Return the paginated response
        response_data = {"data": paginated_items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def sb_collection(request, **kwargs):
        logger.debug(f"[API Call] {request.__class__.__name__} [data fetched successfully] ")
    
        # Path to the STAC catalog
        catalog_root = "./stac-catalog"

        # List to store items
        items = []
        # Folders to exclude from search
        excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Get limit and offset from query parameters
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_root):
            main_subfolder_path = os.path.join(catalog_root, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)
                    subfolder_path=subfolder_path.replace("\\","/")
                    print("*******subfolder_path*****",subfolder_path)
                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            print("************",item_folder_name)
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is a JSON file ending with '-item.json'
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        with open(file_path, 'r') as json_file:
                                            item_data = json.load(json_file)

                                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                                properties_values = item_data['properties'].values()
                                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                                    formatted_item = format_item_data(item_data)
                                                    items.append(formatted_item)

        # Apply limit and offset
        paginated_items = items[offset:offset + limit]

        # Return the paginated response
        response_data = {"data": paginated_items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)


  #  except Exception as e:
        # Handle exceptions and return an error response
      #  error_message = str(e)
      #  return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# function for the search of sode bar collection data
@api_view(['GET'])
def sb_subcollection(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                    with open(file_path, 'r') as json_file:
                        item_data = json.load(json_file)

                        if 'properties' in item_data and isinstance(item_data['properties'], dict):
                            properties_values = item_data['properties'].values()
                            if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                formatted_item = format_item_data(item_data)
                                items.append(formatted_item)
                                    
        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# To manipulate the response that coming in properties for all side search we are use this function
def format_item_data(item_data):
    """
    Function to format an individual item based on the specified structure.
    """
    formatted_item = {
        "id": item_data['id'],
        "Major": item_data['properties'].get('major', ''),
        "Submajor": item_data['properties'].get('submajor', ''),
        "Minor": item_data['properties'].get('minor', ''),
        "SubMinor": item_data['properties'].get('subminor', ''),
        "Grade": item_data['properties'].get('grade', ''),
        "File_formats": item_data['properties'].get('file_formats', ''),
        "Type": item_data['properties'].get('type', ''),
        "source_description": item_data['properties'].get('source_description', ''),
        "place_city": item_data['properties'].get('place_city', ''),
        "year": item_data['properties'].get('year', ''),
        "publisher": item_data['properties'].get('publisher', ''),
        "path": item_data['properties'].get('path', ''),
        "collection": item_data['properties'].get('collection', ''),
        "collection_type": item_data['properties'].get('collection_type', ''),
        "soi_toposheet_no": item_data['properties'].get('soi_toposheet_no', ''),
        "data_resolution": item_data['properties'].get('data_resolution', ''),
        "ownership": item_data['properties'].get('ownership', ''),
        "is_processed": item_data['properties'].get('is_processed', ''),
        "short_descr": item_data['properties'].get('short_descr', ''),
        "descr": item_data['properties'].get('descr', ''),
        "img_service": item_data['properties'].get('img_service', ''),
        "img_dw": item_data['properties'].get('img_dw', ''),
        "map_service": item_data['properties'].get('map_service', ''),
        "map_dw": item_data['properties'].get('map_dw', ''),
        "publish_on": item_data['properties'].get('publish_on', ''),
        "thumbnail": item_data['properties'].get('thumbnail', ''),
        "source": item_data['properties'].get('source', ''),
        "created_date": item_data['properties'].get('created_date', ''),
        "img_vis_url": item_data['properties'].get('img_vis_url', ''),
        "img_download_url": item_data['properties'].get('img_download_url', ''),
        "shp_file_url": item_data['properties'].get('shp_file_url', ''),
        "urlalias": item_data['properties'].get('urlalias', ''),
    }
    return formatted_item


from django.http import JsonResponse

# Assuming your function looks something like this
def search_side_bar(request):
    logger.debug(f"[API Call] {request.__class__.__name__} [data fetched successfully] ")
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Folders to exclude from search
        excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']

        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_path):
            main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is a JSON file
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        # Example: Read the content of JSON file
                                        with open(file_path, 'r') as json_file:
                                            item_data = json.load(json_file)
                                            # Check if the specified key is present in the properties section
                                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                                items.append(item_data)

        # Initialize a dictionary to organize items based on properties
        data = {
            'major': [],
            'submajor': [],
            'minor': [],
            'subminor': [],
            'grade': [],
            'publisher': [],
            'place_city': [],
            'year': [],
            # Add more categories as needed
        }

        # Iterate through each item in your response
        for item in items:
            for key in data.keys():
                if key in item['properties']:
                    subhead_value = item['properties'][key]
                    # Check if a dictionary with the same subhead already exists in the list
                    subhead_dict = next((d for d in data[key] if d['subhead'] == subhead_value), None)
                    if subhead_dict:
                        # Increment the count if the subhead exists
                        subhead_dict['count'] += 1
                    else:
                        # Add a new dictionary if the subhead doesn't exist
                        data[key].append({'subhead': subhead_value, 'count': 1})
            # Add more conditions for other properties

        # Return the organized data as JSON response
        return JsonResponse(data)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return JsonResponse({"error": error_message}, status=500)
    


def search_catalog_metadata_for_combined_response(request, query, **kwargs):
    # Path to the STAC catalog
    catalog_path = "./stac-catalog"

    # List to store items
    items = []
    excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
    # Iterate through each main subfolder (state, city, etc.) in the catalog
    for main_subfolder_name in os.listdir(catalog_path):
        main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

        # Check if the path is a directory and not in excluded folders list
        if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
            # Iterate through each subfolder within the main subfolder
            for subfolder_name in os.listdir(main_subfolder_path):
                subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                # Check if the path is a directory
                if os.path.isdir(subfolder_path):
                    # Iterate through each item folder in the sub-subfolder
                    for item_folder_name in os.listdir(subfolder_path):
                        # Check if the folder name is in the expected format
                        if item_folder_name.endswith('-item'):
                            # Construct the full path to the item folder
                            item_folder_path = os.path.join(subfolder_path, item_folder_name)

                            # Access files within the item folder
                            for file_name in os.listdir(item_folder_path):
                                # Check if the file is a JSON file
                                if file_name.endswith('-item.json'):
                                    file_path = os.path.join(item_folder_path, file_name)

                                    # Example: Read the content of JSON file
                                    with open(file_path, 'r') as json_file:
                                        item_data = json.load(json_file)

                                        # Check if the specified key is present in the properties section
                                        if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                            properties = item_data['properties']

                                            # Check if any value in properties matches the query
                                            # Check if any key-value pair in properties matches any key-value pair in query
                                            # Check if query is a string and matches any value in properties
                                            if isinstance(query, str) and any(
                                                str(query).lower() in str(value).lower() for value in properties.values()
                                            ):
                                                response_data = {
                                                    "major": properties.get("major", ""),
                                                    "Submajor": properties.get("submajor", ""),
                                                    "Minor": properties.get("minor", ""),
                                                    "SubMinor": properties.get("subminor", ""),
                                                    "Grade": properties.get("grade", ""),
                                                    "File_formats": properties.get("file_formats", ""),
                                                    "Type": properties.get("type", ""),
                                                    "Source_Description": properties.get("source_description", ""),
                                                    "place_city": properties.get("place_city", ""),
                                                    "year": properties.get("year", ""),
                                                    "publisher": properties.get("publisher", ""),
                                                    "Path": properties.get("path", ""),
                                                    "Collection": properties.get("collection", ""),
                                                    "Collection_type": properties.get("collection_type", ""),
                                                    "SOI_toposheet_no": properties.get("soi_toposheet_no", ""),
                                                    "Data_Resolution": properties.get("data_resolution", ""),
                                                    "Ownership": properties.get("ownership", ""),
                                                    "is_processed": properties.get("is_processed", ""),
                                                    "short_descr": properties.get("short_descr", ""),
                                                    "descr": properties.get("descr", ""),
                                                    "img_service": properties.get("img_service", ""),
                                                    "img_dw": properties.get("img_dw", ""),
                                                    "map_service": properties.get("map_service", ""),
                                                    "map_dw": properties.get("map_dw", ""),
                                                    "publish_on": properties.get("publish_on", ""),
                                                    "thumbnail": properties.get("thumbnail", ""),
                                                    "source": properties.get("source", ""),
                                                    "created_date": properties.get("created_date", ""),
                                                    "img_vis_url":properties.get("img_vis_url", ""),
                                                    "img_download_url":properties.get("img_download_url", ""),
                                                    "shp_file_url":properties.get("shp_file_url", ""),
                                                }
                                                items.append(response_data)

    # Check if there are no items found
    if not items:
        return HttpResponseNotFound("No items found matching the specified key.")

    # Return the list of items matching the specified key as JsonResponse
    return JsonResponse(items, safe=False)




def search_sidebar_for_combined_response(request, query, **kwargs):
    # Path to the STAC catalog
    catalog_path = "./stac-catalog"

    # List to store items
    items = []
    excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
    # Iterate through each main subfolder in the catalog
    for main_subfolder_name in os.listdir(catalog_path):
        main_subfolder_path = os.path.join(catalog_path, main_subfolder_name)

        # Check if the path is a directory and not in excluded folders list
        if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
            # Iterate through each subfolder within the main subfolder
            for subfolder_name in os.listdir(main_subfolder_path):
                subfolder_path = os.path.join(main_subfolder_path, subfolder_name)

                # Check if the path is a directory
                if os.path.isdir(subfolder_path):
                    # Iterate through each item folder in the sub-subfolder
                    for item_folder_name in os.listdir(subfolder_path):
                        # Check if the folder name is in the expected format
                        if item_folder_name.endswith('-item'):
                            # Construct the full path to the item folder
                            item_folder_path = os.path.join(subfolder_path, item_folder_name)

                            # Access files within the item folder
                            for file_name in os.listdir(item_folder_path):
                                # Check if the file is a JSON file
                                if file_name.endswith('-item.json'):
                                    file_path = os.path.join(item_folder_path, file_name)

                                    # Example: Read the content of JSON file
                                    with open(file_path, 'r') as json_file:
                                        item_data = json.load(json_file)

                                        # Check if the specified key is present in the properties section
                                        if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                            properties = item_data['properties']

                                            # Check if any value in properties matches the query
                                            # Check if any key-value pair in properties matches any key-value pair in query
                                            # Check if query is a string and matches any value in properties
                                            if isinstance(query, str) and any(
                                                str(query).lower() in str(value).lower() for value in properties.values()
                                            ):
                                                items.append(item_data)  # Add item only if it matches the query

    # Initialize a dictionary to organize items based on properties
    data = {
        'major': [],
        'submajor': [],
        'minor': [],
        'subminor': [],
        'grade': [],
        'publisher': [],
        'place_city': [],
        'year': [],
        # Add more categories as needed
    }

    # Iterate through each item in your response
    for item in items:
        for key in data.keys():
            if key in item['properties']:
                subhead_value = item['properties'][key]
                # Check if a dictionary with the same subhead already exists in the list
                subhead_dict = next((d for d in data[key] if d['subhead'] == subhead_value), None)
                if subhead_dict:
                    # Increment the count if the subhead exists
                    subhead_dict['count'] += 1
                else:
                    # Add a new dictionary if the subhead doesn't exist
                    data[key].append({'subhead': subhead_value, 'count': 1})
        # Add more conditions for other properties

    # Return the organized data as JSON response
    return JsonResponse(data)




###### In this function for main page we combine the two function 
## to give response in combined format
@api_view(['GET'])
def combined_response(request, query):
    logging_data = dict(request.data)
    logger.debug(f"[API Call] {request.__class__.__name__} create Data: {logging_data}")
    try:
        # Call the first function to get the search results
        search_results = search_catalog_metadata_for_combined_response(request, query)

        # Call the second function to get the sidebar data
        sidebar_data = search_sidebar_for_combined_response(request, query)

        # Initialize search results and sidebar data as empty dictionaries
        search_results_dict = {}
        sidebar_data_dict = {}

        # Try to load JSON from the responses
        try:
            search_results_dict = json.loads(search_results.content)
            sidebar_data_dict = json.loads(sidebar_data.content)
        except json.JSONDecodeError:
            pass

        # Check if both search results and sidebar data are empty
        if not search_results_dict and not sidebar_data_dict:
            return JsonResponse({"message": "No data available for the specified query."})

        # Return the responses separately
        return JsonResponse({
            'ms_data': search_results_dict,
            'sb_data': sidebar_data_dict
        })

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return JsonResponse({"error": error_message}, status=500)


    
from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from psycopg2.extensions import AsIs   
    
    
from psycopg2.extensions import AsIs

from django.db import connection
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from psycopg2.extensions import AsIs   
    
# api to get data by using lat long within query
# the shape file name coming will be in dynamically and multiple.    
class AttributeViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def get_within_point(self, request):
        latitude = request.query_params.get('lat')
        longitude = request.query_params.get('long')
        shape_file_names = request.query_params.getlist('shape_file_name')
        radius_in_meters = request.query_params.get('radius_in_centimeters', 100)  # Default to 1000 centimeters if not provided


        print("********************************", latitude, longitude, shape_file_names,radius_in_meters)

        if latitude is None or longitude is None:
            return Response(status=400, data={'error': 'Latitude and longitude parameters are required.'})

        if not shape_file_names:
            return Response(status=400, data={'error': 'Shape file names are not present.'})
            
        # Convert centimeters to degrees (approximate conversion factor)
        radius_in_degrees = float(radius_in_meters) / 111000


        results = []

        for shape_file_name in shape_file_names:
            # Modify this section to remove extra quotes around the table name
            query = '''
                SELECT *
                FROM {}
                WHERE ST_DWithin(geom, ST_SetSRID('POINT(%s %s)'::geometry, 4326), %s);
            '''.format(AsIs(shape_file_name))

            with connection.cursor() as cursor:
                cursor.execute(query, [float(longitude), float(latitude), float(radius_in_degrees)])
                result = cursor.fetchall()
                print("++++++++++++++++++++++++++++++++", result)
                if not result:
                    msg = f"No data within the specified radius from {latitude}, {longitude} in {shape_file_name}."
                    results.append({'Layer_Name': shape_file_name, 'message': msg})
                else:
                    for row in result:
                        # Convert the row to a dictionary for easy serialization
                        row_dict = dict(zip([desc[0] for desc in cursor.description], row))
                        
                        # Check if 'geom' field exists in the row_dict
                        if 'geom' in row_dict:
                            print("-------------geom is present---")
                            del row_dict['geom']  # Remove the 'geom' field from the dictionary
                            
                        # Check if 'gid' field exists in the row_dict
                        if 'gid' in row_dict:
                            del row_dict['gid']
                        
                        if 'id' in row_dict:
                            del row_dict['id']
                        results.append({'Layer_Name': shape_file_name, 'result': row_dict})

        return Response(results)


class All_AttributeViewSet(APIView):
    def get(self, request):
        logging_data = dict(request.data)
       # logging.debug(f"[API Call] {request} ")
        shape_file_name = request.query_params.get('shape_file_name')

        if not shape_file_name:
            return Response(status=400, data={'error': 'Shape file name is not present.'})

        results = []

        query = '''
    SELECT *
    FROM "{}"
    '''.format(shape_file_name)

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                msg = f"No Data Found for {shape_file_name}."
                results.append({'Layer_Name': shape_file_name, 'message': msg})
            else:
                for row in result:
                    row_dict = dict(zip([desc[0] for desc in cursor.description], row))
                    
                    # Check if 'geom', 'gid', 'id' fields exist in the row_dict and exclude them
                    if 'geom' in row_dict:
                        del row_dict['geom']
                    if 'gid' in row_dict:
                        del row_dict['gid']
                    if 'id' in row_dict:
                        del row_dict['id']
                    
                    results.append({'Layer_Name': shape_file_name, 'result': row_dict})

        return Response(results)

from django.http import QueryDict

@api_view(['GET'])
def sb_collection1(request, **kwargs):
    logger.debug(f"[API Call] {request.__class__.__name__} [data fetched successfully] ")
    
    # Path to the STAC catalog
    catalog_root = "./stac-catalog"

    # List to store items
    items = []
    # Folders to exclude from search
    excluded_folders = ['Projects', 'Resources_and_Publication', 'Shape_File_Data']
    # Get the list of selectedItems from query parameters
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]

    # Get limit and offset from query parameters
    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))

    try:
        # Iterate through each main subfolder (state, city, etc.) in the catalog
        for main_subfolder_name in os.listdir(catalog_root):
            main_subfolder_path = os.path.join(catalog_root, main_subfolder_name)

            # Check if the path is a directory and not in excluded folders list
            if os.path.isdir(main_subfolder_path) and main_subfolder_name not in excluded_folders:
                # Iterate through each subfolder within the main subfolder
                for subfolder_name in os.listdir(main_subfolder_path):
                    subfolder_path = os.path.join(main_subfolder_path, subfolder_name)
                    subfolder_path = subfolder_path.replace("\\", "/")
                    print("*******subfolder_path*****", subfolder_path)
                    # Check if the path is a directory
                    if os.path.isdir(subfolder_path):
                        # Iterate through each item folder in the sub-subfolder
                        for item_folder_name in os.listdir(subfolder_path):
                            print("************", item_folder_name)
                            # Check if the folder name is in the expected format
                            if item_folder_name.endswith('-item'):
                                # Construct the full path to the item folder
                                item_folder_path = os.path.join(subfolder_path, item_folder_name)

                                # Access files within the item folder
                                for file_name in os.listdir(item_folder_path):
                                    # Check if the file is a JSON file ending with '-item.json'
                                    if file_name.endswith('-item.json'):
                                        file_path = os.path.join(item_folder_path, file_name)

                                        with open(file_path, 'r') as json_file:
                                            item_data = json.load(json_file)

                                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                                properties_values = item_data['properties'].values()
                                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                                    formatted_item = format_item_data(item_data)
                                                    items.append(formatted_item)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Apply limit and offset
    paginated_items = items[offset:offset + limit]

    # Build pagination links with original query parameters preserved
    base_url = 'https://products.coderize.in/api/flame/stac/sb_collection1/'
    query_params_dict = QueryDict(request.GET.urlencode(), mutable=True)
    query_params_dict['limit'] = limit
    query_params_dict['offset'] = offset + limit if len(paginated_items) == limit else None  # Calculate next offset
    next_url = base_url + '?' + query_params_dict.urlencode() if query_params_dict['offset'] is not None else None
    query_params_dict['offset'] = offset - limit if offset - limit >= 0 else None  # Calculate previous offset
    previous_url = base_url + '?' + query_params_dict.urlencode() if query_params_dict['offset'] is not None else None

    response_data = {
        "next": next_url,
        "previous": previous_url,
        "count": len(items),
        "results": paginated_items
    }

    return Response(response_data, status=status.HTTP_200_OK)






