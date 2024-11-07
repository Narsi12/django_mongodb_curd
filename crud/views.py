import logging
import pymongo
from .models import Employee
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import emp
from rest_framework import status
from bson import ObjectId

# Set up logging
logger = logging.getLogger(__name__)


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Employee_info"]
employees = mydb['crud_employee']

@api_view(['POST'])
def create_employee(request):
    logger.info('create endpoint hit with data: %s', request.data)
    serializer = emp(data = request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info('New employee created: %s', serializer.data)
        return Response(serializer.data,status = status.HTTP_200_OK)
    else:
        logger.error('Error in create: %s', serializer.errors)
        return Response(serializer.data,status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_users(request):
    logger.info('Retrieving all users')

    try:
        breakpoint()
        # Retrieve all employee records using PyMongo
        users = employees.find()
        
        # Convert the cursor to a list of dictionaries
        employee_list = []
        for user in users:
            # Ensure you convert ObjectId to string for JSON serialization
            user['_id'] = str(user['_id'])
            employee_list.append(user)

        return Response(employee_list, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f'Error retrieving users: {e}')
        return Response({'error': 'An error occurred while retrieving users'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PUT'])
def update_employee(request, pk):
    logger.info(f'Updating employee with ID: {pk}')
    try:
        employee_id = ObjectId(pk)
        updated_data = request.data
        result = employees.find_one_and_update(
            {'_id': employee_id},   
            {'$set': updated_data},   
            return_document=pymongo.ReturnDocument.AFTER  # Return the updated document
        )
        if result is not None:
            # Convert ObjectId to string for JSON serialization
            result['_id'] = str(result['_id'])
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'Error updating employee: {e}')
        return Response({'error': 'An error occurred while updating the employee'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      

@api_view(['DELETE'])
def delete_user(request, pk):
    logger.info(f'Deleting employee with ID: {pk}')

    try:
        # Convert the primary key (pk) to an ObjectId
        employee_id = ObjectId(pk)

        # Delete the employee document using delete_one
        result = employees.delete_one({'_id': employee_id})

        if result.deleted_count > 0:
            return Response({'message': 'Employee deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'Error deleting employee: {e}')
        return Response({'error': 'An error occurred while deleting the employee'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)