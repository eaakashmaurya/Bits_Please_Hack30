from django import forms

# Models
from posts.models import Post


class ComplaintForm(forms.ModelForm):
	"""Post model form"""

	class Meta:
		"""Form settings."""
		model = Post
		fields = ('userprofile', 'category', 'complaint_face_picture')