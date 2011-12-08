## coding: utf-8
##
##Generated file by Revelator - (Kovalenko Pavel ice.tegliaf@gmail.com)
##
#from apps.data_utils    import randomize
#from models             import *
#import datetime
#
#def handle():
#    print u"\nGenerate Город:",
#    for i in range(10):
#        try:
#            City(
#                name = randomize.string(15),
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Район:",
#    for i in range(100):
#        try:
#            Metro(
#                name = randomize.string(15),
#                city = City.objects.order_by('?')[0],
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Группа категорий:",
#    for i in range(100):
#        try:
#            CategoryGroup(
#                name = randomize.string(15),
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Категория:",
#    for i in range(13):
#        try:
#            Category(
#                name = randomize.string(15),
#                group = CategoryGroup.objects.order_by('?')[0],
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Событие:",
#    for i in range(100):
#        try:
#            e=Event(
#                title = randomize.string(40),
#                address = randomize.string(40),
#                place = randomize.string(40),
#                description = randomize.text(),
#                begin = randomize.datetime(),
#                end = randomize.datetime(),
#                metro = Metro.objects.order_by('?')[0],
#                author = User.objects.order_by('?')[0],
#                published_by_author = randomize.boolean(),
#                published_by_moderator = randomize.boolean(),
#                category = Category.objects.order_by('?')[0],
#                 #visiters - unknown randomdb generator
#                rang = randomize.integer(),
#                event_of_week = randomize.boolean(),
#                min_participants = randomize.integer(),
#                max_participants = randomize.integer(),
#                )
#            e.save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#            
#        for i in range(randomize.integer(0, 30)):
#            try:
#                Comment(
#                    event = e,
#                    user = User.objects.order_by('?')[0],
#                    created = randomize.datetime(),
#                    text = randomize.text(),
#                    ).save()
#                randomize.out('.')
#            except:
#                randomize.out('*')
#
#    print u"\nGenerate Рейтинг - история:",
#    for i in range(100):
#        try:
#            RangHistory(
#                event = Event.objects.order_by('?')[0],
#                user = User.objects.order_by('?')[0],
#                rang = randomize.integer(),
#                datetime = randomize.datetime(),
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Сообщение мини блога:",
#    for i in range(100):
#        try:
#            MiniBlogPost(
#                author = User.objects.order_by('?')[0],
#                created = randomize.datetime(),
#                text = randomize.text(),
#                published = randomize.boolean(),
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Комментарий:",
#    for i in range(100):
#        try:
#            MiniBlogComment(
#                post = MiniBlogPost.objects.order_by('?')[0],
#                user = User.objects.order_by('?')[0],
#                when = randomize.datetime(),
#                text = randomize.text(),
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Черные метки:",
#    for i in range(100):
#        try:
#            Ban(
#                user = User.objects.order_by('?')[0],
#                event = Event.objects.order_by('?')[0],
#                when = randomize.datetime(),
#                who = User.objects.order_by('?')[0],
#                reason = randomize.text(),
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Фото:",
#    for i in range(100):
#        try:
#            Photo(
#                event = Event.objects.order_by('?')[0],
#                created = randomize.datetime(),
#                 #photo - unknown randomdb generator
#                title = randomize.string(255),
#                published = randomize.boolean(),
#                author = User.objects.order_by('?')[0],
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')
#
#    print u"\nGenerate Видео:",
#    for i in range(100):
#        try:
#            Video(
#                event = Event.objects.order_by('?')[0],
#                created = randomize.datetime(),
#                 #video - unknown randomdb generator
#                title = randomize.string(255),
#                published = randomize.boolean(),
#                user = User.objects.order_by('?')[0],
#                ).save()
#            randomize.out('.')
#        except:
#            randomize.out('*')




