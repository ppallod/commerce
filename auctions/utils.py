from django import forms

#Bid Form
class BidForm(forms.Form):
    def __init__(self, *args, **kwargs):
        current_price = kwargs.pop('current_price')
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['amount'] = forms.IntegerField(label="Place Your Bid", min_value=current_price+1)

