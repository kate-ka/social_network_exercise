from rest_framework.permissions import BasePermission


class AllowAuthorEditPost(BasePermission):
    def has_object_permission(self, request, view, post):
        if request.method in ("PATCH", "PUT", "DELETE") and request.user != post.user:
            return False

        return True
