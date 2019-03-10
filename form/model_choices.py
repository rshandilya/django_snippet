# models.py
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 

# forms.py
from django import forms
from .models import Category, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'category', )

    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
     

## views.py
from django.shortcuts import render, redirect
from .forms import ProductForm

@login_required
def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.user, request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('products_list')
    else:
        form = ProductForm(request.user)
    return render(request, 'products/product_form.html', {'form': form})
    
    
#####  using ModelFormSet ######
#models.py
@login_required
def edit_all_products(request):
    ProductFormSet = modelformset_factory(Product, fields=('name', 'price', 'category'), extra=0)
    data = request.POST or None
    formset = ProductFormSet(data=data, queryset=Product.objects.filter(user=request.user))
    for form in formset:
        form.fields['category'].queryset = Category.objects.filter(user=request.user)

    if request.method == 'POST' and formset.is_valid():
        formset.save()
        return redirect('products_list')

    return render(request, 'products/products_formset.html', {'formset': formset})
