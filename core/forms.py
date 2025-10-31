
from django import forms

from .models import ContactMessage, Review


class StyledFormMixin:
    """Apply Bootstrap classes to form fields automatically."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            base_class = widget.attrs.get("class", "")

            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                widget.attrs["class"] = (base_class + " form-check-input").strip()
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = (base_class + " form-select").strip()
            else:
                widget.attrs["class"] = (base_class + " form-control").strip()

            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("rows", 4)


class ContactForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}


class ReviewForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ("name", "comment", "rating")
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4, "placeholder": "Share your stay experience"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].choices = Review.RATING_CHOICES
