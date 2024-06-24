from flask import request, make_response, jsonify, current_app as app
from app  import db
from app.models import db, User, Task, Review

@app.route('/users', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        users_to_dict = []
        for user in User.query.order_by('created_at').all():
            to_dict = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_name': user.username,
                'email': user.email,
                'phone': user.phone
            }
            users_to_dict.append(to_dict)
        response = make_response(
            jsonify(users_to_dict),
            200,
        )
    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('user_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            password=data.get('password')
        )
        db.session.add(new_user)
        db.session.commit()
        response = make_response(
            jsonify({
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'user_name': new_user.username,
                'email': new_user.email,
                'phone': new_user.phone
            }),
            201,
        )
    else:
        response = make_response(
            jsonify({"error": "Method not allowed"}),
            405,
        )
    return response
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        response = make_response(
            jsonify({"message": "User deleted successfully"}),
            200,
        )
    else:
        response = make_response(
            jsonify({"error": "User not found"}),
            404,
        )
    return response

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks_to_dict = []
        for task in Task.query.order_by('created_at').all():
            to_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'tart_date': task.start_date,
                'end_date': task.end_date,
                'tatus': task.status,
                'user_id': task.owner_id
            }
            tasks_to_dict.append(to_dict)
        response = make_response(
            jsonify(tasks_to_dict),
            200,
        )
    elif request.method == 'POST':
        data = request.get_json()
        new_task = Task(
            title=data.get('title'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            status=data.get('status', 'incomplete'),
            owner_id=data.get('user_id')
        )
        db.session.add(new_task)
        db.session.commit()
        response = make_response(
            jsonify({
                'id': new_task.id,
                'title': new_task.title,
                'description': new_task.description,
                'tart_date': new_task.start_date,
                'end_date': new_task.end_date,
                'tatus': new_task.status,
                'user_id': new_task.owner_id
            }),
            201,
        )
    else:
        response = make_response(
            jsonify({"error": "Method not allowed"}),
            405,
        )
    return response

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        response = make_response(
            jsonify({"message": "Task deleted successfully"}),
            200,
        )
    else:
        response = make_response(
            jsonify({"error": "Task not found"}),
            404,
        )
    return response

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task:
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.start_date = data.get('start_date', task.start_date)
        task.end_date = data.get('end_date', task.end_date)
        task.status = data.get('status', task.status)
        task.user_id = data.get('user_id', task.user_id)
        db.session.commit()
        response = make_response(
            jsonify({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'start_date': task.start_date,
                'end_date': task.end_date,
                'status': task.status,
                'user_id': task.user_id
                }),
                200,
                )

    else:
        response = make_response(
            jsonify({"error": "Task not found"}),
            404,
        )
        return response
    return response

@app.route('/tasks/<int:task_id>/reviews', methods=['GET', 'POST'])
def reviews(task_id):
    if request.method == 'GET':
        reviews_to_dict = []
        for review in Review.query.filter_by(task_id=task_id).order_by('created_at').all():
            to_dict = {
                'id': review.id,
                'content': review.content,
                'rating': review.rating,
                'created_at': review.created_at
            }
            reviews_to_dict.append(to_dict)
        response = make_response(
            jsonify(reviews_to_dict),
            200,
        )
    elif request.method == 'POST':
        data = request.get_json()
        new_review = Review(
            content=data.get('content'),
            rating=data.get('rating'),
            task_id=task_id
        )
        db.session.add(new_review)
        db.session.commit()
        response = make_response(
            jsonify({
                'id': new_review.id,
                'content': new_review.content,
                'rating': new_review.rating,
                'created_at': new_review.created_at
            }),
            201,
        )
    return response

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        response = make_response(
            jsonify({"message": "Review deleted successfully"}),
            200,
        )
    else:
        response = make_response(
            jsonify({"error": "Review not found"}),
            404,
        )
    return response

@app.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get(review_id)
    if review:
        data = request.get_json()
        review.content = data.get('content', review.content)
        review.rating = data.get('rating', review.rating)
        db.session.commit()
        response = make_response(
            jsonify({
                'id': review.id,
                'content': review.content,
                'rating': review.rating,
                'created_at': review.created_at
                }),
                200,
                )

    else:
        response = make_response(
            jsonify({"error": "Review not found"}),
            404,
        )
        return response
    return response

@app.route('/tasks/<int:task_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_review_from_task(task_id, review_id):
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        response = make_response(
            jsonify({"message": "Review deleted successfully"}),
            200,
        )
    else:
        response = make_response(
            jsonify({"error": "Review not found"}),
            404,
        )
    return response

@app.route('/tasks/<int:task_id>/reviews/<int:review_id>', methods=['PUT'])
def update_review_from_task(task_id, review_id):
    review = Review.query.get(review_id)
    if review:
        data = request.get_json()
        review.content = data.get('content', review.content)
        review.rating = data.get('rating', review.rating)
        db.session.commit()
        response = make_response(
            jsonify({
                'id': review.id,
                'content': review.content,
                'rating': review.rating,
                'created_at': review.created_at
                }),
                200,
                )

    else:
        response = make_response(
            jsonify({"error": "Review not found"}),
            404,
        )
        return response
    return response

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
