from django.utils.safestring import mark_safe
import copy

"""
customized pagination

Instruction for using the pagination class:

In the view.py:
    
    def pretty_list(request):
        
       
       ## 1. filter the data
       queryset = models.PrettyNum.objects.all()
       
       ## 2. instantiate a paginator object
       page_object = Pagination(request, queryset)
       
       context = {
       "queryset": page_object.page_queryset, # Paged data
       "page_string": page_object.html()  # generate page numbers
       }
       
       return render(request, 'num_list.html', context)
       
AND THEN:

In the HTML:

     {% for item in queryset %}   
        {{item.xx}}
     {% endfor %}
    
     <ul class="pagination">  
         {{ page_string }}
    </ul>

"""

class Pagination():

    def __init__(self, request, queryset, page_size=10, page_param="page", plus = 5):
        """
        :param request: request an object
        :param queryset: eligible data (through the search function), according to the data, process the pagination
        :param page_size: how many items per page
        :param page_param: GET the "page" in URL, for example: /num/list/?page=1
        :param plus: the number of previous or next page number
        """
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        self.total_page = (total_count // page_size) + 1

        self.plus = plus

        self.page_param = page_param

        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict




    def html(self):
        if self.total_page <= self.plus * 2:
            start_page = 1
            end_page = self.total_page
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = self.plus * 2 + 1
            else:
                if self.page + self.plus > self.total_page:
                    start_page = self.total_page - 2 * self.plus
                    end_page = self.total_page
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = []

        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">Previous Page</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = f'<li><a href="?{self.query_dict.urlencode()}">Previous Page</a></li>'
        page_str_list.append(prev)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            else:
                ele = f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>'
            page_str_list.append(ele)

        if self.page < self.total_page:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = f'<li><a href="?{self.query_dict.urlencode()}">Next Page</a></li>'
        else:
            self.query_dict.setlist(self.page_param, [self.total_page])
            next = f'<li><a href="?{self.query_dict.urlencode()}">Next Page</a></li>'
        page_str_list.append(next)



        page_string = mark_safe("".join(page_str_list))

        # search_string
        return page_string