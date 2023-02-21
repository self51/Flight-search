from django.shortcuts import render

from .service import Parser


# receives input data, processes it, receives page content,
# extracts the necessary information, catches some errors
def flight_search(request):

    if 'start_city' in request.GET:
        start_city = request.GET.get('start_city')
        destination_city = request.GET.get('destination_city')
        date = request.GET.get('date')

        p = Parser(start_city, destination_city, date)
        page_source = p.get_html_content()
        flights = p.get_flights(page_source)

        if flights == 'error':
            error = 'Warning: We were unable to get a price for your selected itinerary.'
            return render(request, 'flight_search/flight_search.html', {'error': error})

        return render(request, 'flight_search/flight_search.html', {'flights': flights})

    return render(request, 'flight_search/flight_search.html')

