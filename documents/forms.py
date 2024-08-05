from django import forms


class RejectionCommentForm(forms.Form):
    rejection_comment = forms.CharField(
        required=False,  # Делаем поле необязательным
        widget=forms.Textarea(attrs={'rows': 24}),
        label='Комментарий к отклонению'
    )
