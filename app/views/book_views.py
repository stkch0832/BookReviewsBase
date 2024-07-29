from django.shortcuts import render
from django.views.generic import View
from .api_views import get_api_data
from app.forms.book_forms import BookSearchForm
from django.http import JsonResponse


class BookSearchView(View):
    def get(self, request, *args, **kwargs):
        form = BookSearchForm(request.POST or None)

        return render(request, 'app/book_form.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = BookSearchForm(request.POST or None)

        if form.is_valid():
            input_title = form.cleaned_data.get('title', '')
            input_author = form.cleaned_data.get('author', '')
            params = {
                'title': input_title,
                'hits': 30,
            }
            if input_author:
                params['author'] = input_author

            try:
                items = get_api_data(params=params)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

            if items is None:
                return render(request, 'app/book_list.html', context={
                    'search_words': f'{input_title} {input_author}' if input_author else input_title
                })

            book_data = []
            for i in items:
                item = i['Item']
                title = item['title']
                author = item['author']
                isbn = item['isbn']
                largeImageUrl = item['largeImageUrl']
                query = {
                'title': title,
                'author': author,
                'isbn': isbn,
                'image': largeImageUrl,
                }
                book_data.append(query)

            return render(request, 'app/book_list.html', context={
                'book_data': book_data,
                'search_words': f'{input_title} {input_author}' if input_author else input_title,
            })

        return render(request, 'app/book_form.html', context={
            'form': form,
        })


class BookDetailView(View):
    def get(self, request, *args, **kwargs):
        isbn = self.kwargs['isbn']
        params = {
            'isbn': isbn,
        }

        api_response = get_api_data(params)
        if api_response is None:
            return render(request, 'app/book_detail.html', {
                'error_message': 'APIのリクエストに失敗しました。'
            })

        items = api_response
        if not items:
            return render(request, 'app/book_detail.html', {
                'error_message': '該当のデータがありません。'
            })

        item = items[0]['Item']
        title = item['title']
        image = item['largeImageUrl']
        author = item['author']
        booksGenreId = item['booksGenreId']
        salesDate = item['salesDate']
        publisherName = item['publisherName']
        isbn = item['isbn']
        itemCaption = item['itemCaption']
        itemUrl = item['itemUrl']
        reviewAverage = item['reviewAverage']
        reviewCount = item['reviewCount']

        book_data = {
            'title': title,
            'image': image,
            'author': author,
            'booksGenreId': booksGenreId,
            'salesDate': salesDate,
            'publisherName': publisherName,
            'isbn': isbn,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
            'reviewAverage': reviewAverage,
            'reviewCount': reviewCount,
        }


        return render(request, 'app/book_detail.html', context={
            'book_data': book_data
        })
