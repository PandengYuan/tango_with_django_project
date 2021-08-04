import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
					   'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, Product



# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories.
# This might seem a little bit confusing, but it allows us to iterate
# through each data structure, and add the data to our models.


# If you want to add more categories or pages,
# add them to the dictionaries above.

# The code below goes through the cats dictionary, then adds each category,
# and then adds all the associated pages for that category.


def populate():

    electronic_device = [
		{'title': 'Computer', 'views': 110, 
		 'url':'http://docs.python.org/3/tutorial/'},
		{'title':'Phone', 'views': 106, 
		 'url':'http://www.greenteapress.com/thinkpython/'},
		{'title':'Tablet', 'views': 109, 
		 'url':'http://www.korokithakis.net/tutorials/python/'} ]

    clothing = [
		{'title':'Jacket', 'views': 105, 
		 'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
		{'title':'Dress', 'views': 104, 
		 'url':'http://www.djangorocks.com/'},
		{'title':'Jeans', 'views': 108, 
		 'url':'http://www.tangowithdjango.com/'} ]
    
    cosmetics = [
		{'title':'Lipstick', 'views': 103, 
		'url':'http://bottlepy.org/docs/dev/'},
		{'title':'Eye Shadow', 'views': 107, 
		'url':'http://flask.pocoo.org'},
		{'title':'Foundation', 'views': 107, 
		'url':'http://flask.pocoo.org'} ]

    toys = [
		{'title': 'Doll', 'views': 110, 
		 'url':'http://docs.python.org/3/tutorial/'},
		{'title':'Teddy', 'views': 106, 
		 'url':'http://www.greenteapress.com/thinkpython/'} ]

    groceries = [
		{'title': 'Toothbrush', 'views': 110, 
		 'url':'http://docs.python.org/3/tutorial/'},
		{'title':'Shampoo', 'views': 106, 
		 'url':'http://www.greenteapress.com/thinkpython/'},
		{'title':'Candy', 'views': 109, 
		 'url':'http://www.korokithakis.net/tutorials/python/'} ]



    cats = {'Electronic Device': {'pages': electronic_device, 'views': 128, 'likes': 64},
        'Clothing': {'pages': clothing, 'views': 64, 'likes': 32},
        'Cosmetics': {'pages': cosmetics, 'views': 32, 'likes': 16}, 
        'Toys': {'pages': toys, 'views': 64, 'likes': 32},
        'Groceries': {'pages': groceries, 'views': 32, 'likes': 16}   
        }


    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])
        


    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')



def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c




# Start execution here!
if __name__ == '__main__':
	print('Starting Rango population script...')
	populate()