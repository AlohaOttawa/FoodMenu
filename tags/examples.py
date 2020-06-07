manage shell

from tags.models import Tag

qs = Tag.objects.all()
print(qs)

asian = Tag.objects.first()
asian.title
asian.slug

asian.MenuItem


asian.menuItem.all()

asian.menuItem.all().first()


from Menu.models import MenuItem

qs = MenuItem.objects.all()
print(qs)

canhchua = qs.first()
canchua.title
canhchua.description
canhchua.tag_set  # get the tag set that contains canh chua

canhchua.tag_set.all()  # all tag items containing canh chua
canhchua.tag_set.filter(title__iexact="Starters")  # returns the tags containing starters holding canh chua
