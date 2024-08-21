from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment, Notification
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'sendNotification/post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data( **kwargs)
        context['notification'] = self.request.user.notifications.filter(is_read=False)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'sendNotification/post_detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm

        return context

class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('pk'))
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()  # This triggers the post_save signal for notifications
            return redirect('post-detail', pk=post.id)
        return JsonResponse({'error': 'Invalid form submission'}, status=400)

@login_required
def get_notifications(request):
    notifications = request.user.notifications.filter(is_read=False)
    notifications_list = [
        {
            'message': n.message,
            'timestamp': n.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'post_id': n.post.id
        }
        for n in notifications
    ]
    return JsonResponse({'notifications': notifications_list})