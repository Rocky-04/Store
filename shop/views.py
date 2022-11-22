from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView
from django.views.generic import TemplateView

from online_store.settings import EMAIL_HOST_USER
from .forms import ReviewsForm
from .utils import *


class FilterView(ShopMixin):
    def get_queryset(self):
        """
        Filters the product by the selected attributes
        Available filters: min_price, max_price, color, size, manufacturer
        """
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        self.product_list_pk = [int(i) for i in
                                self.request.GET.get('product_list_pk')[
                                1:-1].split(', ')]

        if self.request.GET.getlist("color"):
            filter_color = AttributeColor.objects.filter(
                Q(color__in=self.request.GET.getlist("color"))).values_list(
                'product', flat=True)
        else:
            filter_color = AttributeColor.objects.all().values_list('product',
                                                                    flat=True)

        if self.request.GET.getlist("size"):
            filter_size = AttributeSize.objects.filter(
                Q(size__in=self.request.GET.getlist("size"))).values_list(
                'product__product', flat=True)
        else:
            filter_size = AttributeSize.objects.all().values_list(
                'product__product', flat=True)

        if self.request.GET.getlist("manufacturer"):
            filter_manufacturer = Manufacturer.objects.filter(
                Q(id__in=self.request.GET.getlist(
                    "manufacturer"))).values_list('manufacturer', flat=True)
        else:
            filter_manufacturer = Manufacturer.objects.all().values_list(
                'manufacturer', flat=True)

        queryset = Product.objects.filter(
            Q(pk__in=self.product_list_pk) & Q
            (pk__in=filter_color) & Q
            (pk__in=filter_size) & Q
            (pk__in=filter_manufacturer) & Q
            (price_now__gte=min_price,
             price_now__lte=max_price)
        )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Filter'
        return context


class SkipFilterView(ShopMixin):
    """
    Resets enabled filters
    """

    def get_queryset(self):
        self.product_list_pk = [int(i) for i in
                                self.request.GET.get('product_list_pk')[
                                1:-1].split(', ')]
        queryset = Product.objects.filter(pk__in=self.product_list_pk)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Products')
        return context


class ShopView(ShopMixin):
    """
    Shows all available products
    """

    def get_queryset(self):
        product = Product.objects.all()
        self.product_list_pk = list(product.values_list('pk', flat=True))
        return product


class CategoryView(ShopMixin):
    """
    Shows products by category
    """
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        list_categories_pk = Category.objects.get(
            slug=self.kwargs['slug']).get_list_nested_categories()
        product = Product.objects.filter(category_id__in=list_categories_pk)
        self.product_list_pk = list(product.values_list('pk', flat=True))
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = cat
        context['slug'] = cat.slug
        context['parent'] = cat.pk
        return context


class TagView(ShopMixin):
    """
    Shows products by tag
    """
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        product = Product.objects.filter(
            tags=Tag.objects.get(slug=self.kwargs['slug']))
        self.product_list_pk = list(product.values_list('pk', flat=True))
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Tag.objects.get(slug=self.kwargs['slug'])
        context['slug'] = Tag.objects.get(slug=self.kwargs['slug']).pk
        context['parent'] = False
        return context


class BrandView(ShopMixin):
    """
    Shows products by brand
    """
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        product = Product.objects.filter(
            manufacturer=Manufacturer.objects.get(slug=self.kwargs['slug']))
        self.product_list_pk = list(product.values_list('pk', flat=True))
        return product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Manufacturer.objects.get(slug=self.kwargs['slug'])
        context['slug'] = Manufacturer.objects.get(slug=self.kwargs['slug']).pk
        context['parent'] = False
        return context


class HomeView(ListView):
    """
    Shows the main page of the site
    """
    template_name = 'shop/index.html'
    context_object_name = 'category'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Main')
        return context

    def get_queryset(self):
        return Category.objects.all()


class SendUserMailView(TemplateView):
    template_name = 'shop/info/contact.html'

    def post(self, request):
        """
        Sending a message from a user
        """
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        if name and email and subject and message:
            text_subject = f"contact form: {subject} {name}"
            text_message = (f"You have received a new message from your website contact form.\n\n"
                            f"Here are the details:\n\nName: {name}\n\n\nEmail: {email}\n\n"
                            f"Subject: {subject}\n\nMessage: {message}")
            mail = send_mail(text_subject, text_message, EMAIL_HOST_USER,
                             [email], fail_silently=False)
            if mail:
                messages.success(request, _('Thank you for your request'))
            else:
                messages.error(request,
                               _('Error sending the letter. Try again later'))
        else:
            messages.error(request,
                           _('Error sending the letter. Try again later'))

        return render(request, self.template_name)


class ProductDetailView(DetailView):
    """
    Shows the detailed page of the product card
    """
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'context'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])
        active_color = self.request.GET.get('color')
        active_size = self.request.GET.get('size')

        try:
            if active_color is not None:
                context['active_color'] = product.attribute_color.get(
                    color_id=active_color)
            elif product.available:
                context['active_color'] = product.get_color()[0]
            else:
                context['active_color'] = AttributeColor.objects.filter(product=product)[0]
            if active_size is not None:
                context['active_size'] = context[
                    'active_color'].attribute_size.get(size_id=active_size)
            elif context['active_color'].available:
                context['active_size'] = context['active_color'].get_size()[0]
            else:
                context['active_size'] = context['active_color'].get_size(available=False)[0]
        except Exception as e:
            print(e)

        context['title'] = _('Product')
        context['product'] = product
        context['slug'] = product.category.pk
        context['colors'] = product.get_color(available=False)
        context['form'] = ReviewsForm

        return context


class AboutView(TemplateView):
    template_name = 'shop/info/about-us.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('About us')


class HelpView(TemplateView):
    template_name = 'shop/info/help.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Help')


class TermsView(TemplateView):
    template_name = 'shop/info/terms.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Terms')


class ContactView(TemplateView):
    template_name = 'shop/info/contact.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Contact')


class SearchView(ListView):
    """
    Shows the product search page
    """
    template_name = 'shop/search.html'
    paginate_by = 9
    model = Product
    context_object_name = 'products'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Search')
        context['text'] = f"text={self.request.GET.get('text')}&"
        context['empty'] = self.request.GET.get('text')
        return context

    def get_queryset(self):
        """
        The search is based on the name of the product
        """
        return Product.objects.filter(title__icontains=self.request.GET.get('text'))


class AddReviewView(View):
    """
    Adds a product review
    """

    def post(self, request):
        form = ReviewsForm(request.POST)
        current = request.POST.get('current')

        if form.is_valid() and self.request.user.is_authenticated:
            text = form.data['text']
            rating = form.data['rating']
            user = self.request.user
            product_id = request.POST.get('product_id')

            review = Reviews.objects.filter(user=user, product=product_id)

            if len(review) >= 1:
                review.update(text=text,
                              rating=rating)
            else:
                Reviews.objects.create(user=user,
                                       product_id=product_id,
                                       text=text,
                                       rating=rating)
            messages.success(request, _('Feedback successfully left'))
        else:
            messages.error(request, _('Failed to leave feedback. Try again later'))
        return HttpResponseRedirect(current)


def custom_page_not_found_view(request, exception):
    """
    Custom page not found.
    Status 404 is required for correct operation of LocaleMiddleware
    """
    return render(request, 'shop/page_not_found.html', status=404)
