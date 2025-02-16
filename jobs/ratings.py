from ninja import Router
from ninja.responses import Response
from django.shortcuts import get_object_or_404
from .models import Rating, User
from .schemas import RatingSchema

router = Router()

@router.post("/rate/user/{user_id}/")
def submit_rating(request, user_id: int, payload: RatingSchema):
    """
    Allows applicants and clients to rate each other.
    """
    if not request.user.is_authenticated:
        return Response({"error": "Authentication required"}, status=401)

    if request.user.id == user_id:
        return Response({"error": "You cannot rate yourself"}, status=400)

    reviewed_user = get_object_or_404(User, id=user_id)

    # Validate rating value
    if not (0 <= payload.rating <= 100):
        return Response({"error": "Rating must be between 0 and 100"}, status=400)

    Rating.objects.create(
        reviewer=request.user,
        reviewed=reviewed_user,
        rating=payload.rating,
        feedback=payload.feedback
    )

    return Response({"message": "Rating submitted successfully"}, status=201)


@router.get("/ratings/{user_id}/")
def get_user_rating(request, user_id: int):
    """
    Returns the average rating and feedback for a user.
    """
    user = get_object_or_404(User, id=user_id)
    avg_rating = Rating.get_average_rating(user)
    feedback_list = Rating.objects.filter(reviewed=user).values_list("feedback", flat=True)

    return Response({
        "user_id": user.id,
        "average_rating": avg_rating,
        "feedback": list(feedback_list),
    }, status=200)
