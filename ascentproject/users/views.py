from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User,Entities
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json



# View for creating a new user
@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            user = User.objects.create(
                user_id=data.get('user_id'),
                name=data.get('name'),
                email=data.get('email'),
                password=data.get('password'),
                user_type=data.get('user_type'),
                assigned_entities=data.get('assigned_entities', ''),
                phone_number=data.get('phone_number')
            )
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)


def get_user(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    user_data = {
        'user_id': user.user_id,
        'name': user.name,
        'email': user.email,
        'user_type': user.user_type,
        'assigned_entities': user.assigned_entities
    }
    return JsonResponse(user_data)



@csrf_exempt
def update_user(request, user_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)

            # Retrieve the user object, raise 404 if not found
            user = get_object_or_404(User, pk=user_id)

            # Update fields with data from the request, only if the data exists
            if 'name' in data:
                user.name = data['name']
            if 'email' in data:
                user.email = data['email']
            if 'password' in data:
                user.password = data['password']  # Save password as plain text
            if 'user_type' in data:
                user.user_type = data['user_type']
            if 'assigned_entities' in data:
                user.assigned_entities = data['assigned_entities']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']

            user.save()  # Save the updated user object to the database

            return JsonResponse({'message': 'User updated successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def delete_user(request, user_id):
    if request.method == "DELETE":
        try:
            # Retrieve the user object, raise 404 if not found
            user = get_object_or_404(User, pk=user_id)

            # Delete the user
            user.delete()

            return JsonResponse({'message': 'User deleted successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)



def authenticate_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required'}, status=400)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

            if user.password == password:  # Check password directly for now
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)


def assign_entities_to_user(request, user_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            entity_ids = data.get('assigned_entities', [])

            if not entity_ids:
                return JsonResponse({'error': 'No entities provided'}, status=400)

            # Ensure the entity_ids are in the correct format
            if isinstance(entity_ids, str):
                entity_ids = [int(id.strip()) for id in entity_ids.split(',')]  # Convert comma-separated string to list of ints

            # Fetch the entities based on the IDs provided
            entities = Entities.objects.filter(entity_id__in=entity_ids)
            if len(entities) != len(entity_ids):
                return JsonResponse({'error': 'One or more entities not found'}, status=404)

            # Get the user object
            user = get_object_or_404(User, user_id=user_id)

            # Assign the entities to the user
            user.assigned_entities.set(entities)  # This will assign the selected entities to the user
            user.save()

            return JsonResponse({'message': 'Entities assigned successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)


def reset_password(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            email = data.get('email')
            current_password = data.get('password')  # Current password
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')

            # Check if all fields are provided
            if not email or not current_password or not new_password or not confirm_password:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Check if new password and confirm password match
            if new_password != confirm_password:
                return JsonResponse({'error': 'New password and confirm password do not match'}, status=400)

            # Get the user by email
            user = User.objects.get(email=email)

            # Check if the current password matches the password stored in the database
            if user.password != current_password:
                return JsonResponse({'error': 'Invalid current password'}, status=400)

            # Update the password with the new password (saving it as plain text)
            user.password = new_password  # Save the new password as plain text
            user.save()

            return JsonResponse({'message': 'Password updated successfully'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=400)

    return JsonResponse({'message': 'Invalid HTTP method'}, status=405)