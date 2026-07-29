import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET, require_POST

from shop.models import Product

from reviews.models import Comment


@require_GET
def comment_list(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    reviews = (
        Comment.objects.filter(product=product, parent__isnull=True)
        .select_related("user")
        .prefetch_related("replies__user")
    )

    rating = request.GET.get("rating")
    if rating in ("1", "2", "3", "4", "5"):
        reviews = reviews.filter(rating=int(rating))

    sort = request.GET.get("sort", "-created_at")
    if sort not in ("-created_at", "created_at", "-rating", "rating"):
        sort = "-created_at"
    reviews = reviews.order_by(sort)

    html = render_to_string(
        "reviews/_comment_thread.html", {"comments": reviews}, request=request
    )
    return JsonResponse({"html": html, "count": reviews.count()})


@login_required
@require_POST
def comment_create(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    data = json.loads(request.body)
    body = data.get("body", "").strip()
    if not body:
        return JsonResponse({"ok": False, "error": "Comment can't be empty."}, status=400)

    parent_id = data.get("parent_id")
    parent = get_object_or_404(Comment, pk=parent_id, product=product) if parent_id else None

    rating = data.get("rating") if parent is None else None
    if parent is None and not rating:
        return JsonResponse({"ok": False, "error": "Rating required for a review."}, status=400)

    comment = Comment.objects.create(
        product=product, user=request.user, parent=parent, rating=rating, body=body
    )
    html = render_to_string(
        "reviews/_comment_single.html", {"comment": comment}, request=request
    )
    return JsonResponse({"ok": True, "html": html, "id": comment.pk})


@login_required
@require_POST
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user_id != request.user.id:
        return HttpResponseForbidden()

    data = json.loads(request.body)
    body = data.get("body", "").strip()
    if not body:
        return JsonResponse({"ok": False, "error": "Comment can't be empty."}, status=400)

    comment.body = body
    if comment.parent_id is None and data.get("rating"):
        comment.rating = data["rating"]
    comment.save()
    return JsonResponse({"ok": True, "body": comment.body, "rating": comment.rating})


@login_required
@require_POST
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user_id != request.user.id:
        return HttpResponseForbidden()
    comment.delete()
    return JsonResponse({"ok": True})

@login_required
@require_POST
def comment_like(request, pk):
    pass 

@login_required
@require_POST
def comment_dislike(request, pk):
    pass