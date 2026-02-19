from article.models import Category


c1 = Category(name='Sport')
c1.save()
print(f'Created: {c1.name}')

c2 = Category(name='Technologia')
c2.save()
print(f'Created: {c2.name}')

c3 = Category(name='Kultura')
c3.save()
print(f'Created: {c3.name}')


print('\nAll categories in database:')
for category in Category.objects.all():
    print(f'- ID: {category.id}, Name: {category.name}')

