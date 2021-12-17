import random

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory
from .models import *

COLOR_LIST = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgreen', 'lightgray', 'lightgrey', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'yellow', 'yellowgreen']


class WorkSpaceFactory(DjangoModelFactory):
    class Meta:
        model = WorkSpace

    title = factory.Faker("sentence", nb_words=4, variable_nb_words=True, locale='zh_CN')
    cover = factory.django.ImageField(width=555, height=380,
                                      color=factory.fuzzy.FuzzyChoice(COLOR_LIST))
    space = factory.LazyAttribute(lambda o: o)


class WorkSpacePositionFactory(DjangoModelFactory):
    class Meta:
        model = WorkSpacePosition

    title = factory.Faker("sentence", nb_words=4, variable_nb_words=True, locale='zh_CN')
    work_space = factory.LazyAttribute(lambda o: o)


class SpaceFactory(DjangoModelFactory):
    class Meta:
        model = Space

    factory.Faker.override_default_locale('zh_CN')

    title = factory.Faker("sentence", nb_words=12, variable_nb_words=True, locale='zh_CN')
    cover = factory.django.ImageField(width=670, height=380,
                                      color=factory.fuzzy.FuzzyChoice(COLOR_LIST))
    cover_s = factory.django.ImageField(width=190, height=190,
                                        color=factory.fuzzy.FuzzyChoice(COLOR_LIST))
    address = factory.fuzzy.FuzzyChoice([
        '上海市武夷路19弄',
        '上海市长宁区长宁路1018号龙之梦购物中心(长宁店)F1',
        '上海市浦东新区浦建路1151号',
        '上海市黄浦区中山南路1820号',
        '上海市杨浦区长阳路1665号',
        '上海市闵行区永德路416号',
        '上海市宝山区长江西路1953号',
        '北京市东城区崇文门外大街40号搜秀购物广场8层',
        '北京市东城区地安门外大街与帽儿胡同交叉口东南50米',
        '北京市东城区寿比胡同50号',
        '北京市海淀区西四环中路16号院五棵松体育馆西HI-UP底商111号',
        '北京市海淀区星巴克华熙写字楼店',
        '北京市朝阳区湖景东路11号新奥购物中心B1层',
        '北京市朝阳区天辰东路8-10-12号B3'
    ])
    intro = factory.Faker("sentence", nb_words=52, variable_nb_words=True, locale='zh_CN')
    opentime_from = '10:00'
    opentime_to = '20:00'
    favorite_count = factory.fuzzy.FuzzyInteger(low=5, high=221)

    status = Space.STATUS.published

    @factory.post_generation
    def post_tags(self, create, extracted, **kwargs):
        tags = random.choices((
            'tag#1',
            'tag#2',
            'tag#3',
            'tag#4',
            'tag#5',
            '1999/展',
            '2999/展',
            '3999/展',
            '4999/展',
            '5999/展',
        ), k=2)
        for i in tags:
            self.tags.add(i, through_defaults={
                'is_strike_through': False
            })


class ExhibitionFactory(DjangoModelFactory):
    class Meta:
        model = Exhibition

    factory.Faker.override_default_locale('zh_CN')

    title = factory.Faker("sentence", nb_words=12, variable_nb_words=True, locale='zh_CN')
    cover = factory.django.ImageField(width=670, height=380,
                                      color=factory.fuzzy.FuzzyChoice(COLOR_LIST))
    cover_s = factory.django.ImageField(width=190, height=190,
                                        color=factory.fuzzy.FuzzyChoice(COLOR_LIST))
    start_at = '2021-12-01 12:00'
    end_at = '2021-12-31 16:00'
    favorite_count = factory.fuzzy.FuzzyInteger(low=5, high=221)
    intro = factory.Faker("sentence", nb_words=100, variable_nb_words=True, locale='zh_CN')
    curator = factory.Faker("sentence", nb_words=5, variable_nb_words=True, locale='zh_CN')
    author = factory.Faker("sentence", nb_words=4, variable_nb_words=True, locale='zh_CN')
    status = Space.STATUS.published

    space = factory.lazy_attribute(lambda o: o)


class WorkFactory(DjangoModelFactory):
    class Meta:
        model = Work

    title = factory.Faker("sentence", nb_words=12, variable_nb_words=True, locale='zh_CN')
    cover = factory.django.ImageField(width=750, height=1000,
                                      color=factory.fuzzy.FuzzyChoice(COLOR_LIST))
    price = factory.fuzzy.FuzzyDecimal(low=200.00, high=99999.99, precision=2)
    status = 'on'
    status_text = 'Sold Out'
    intro = factory.Faker("sentence", nb_words=120, variable_nb_words=True, locale='zh_CN')
    size = factory.fuzzy.FuzzyChoice(('75 x 75 cm', '100 x 100 cm', '456 x 789 cm'))
    copyright = factory.Faker("sentence", nb_words=15, variable_nb_words=True, locale='zh_CN')
    inventory = factory.fuzzy.FuzzyInteger(low=1, high=5)

    exhibition = factory.lazy_attribute(lambda o: o)


def run():
    # for _ in range(11):
    #     space = SpaceFactory()
    #     space.clean()
    #     space.save()
    #     print('space --> ' + str(space))
    #
    #     for _ in range(4):
    #         work_space = WorkSpaceFactory(space=space)
    #
    #         for _ in range(4):
    #             position = WorkSpacePositionFactory(work_space=work_space)
    #             print('work_space_position --> ' + str(position))
    #
    #     i = 0
    #     for _ in range(4):
    #         ex = ExhibitionFactory(space=space)
    #         i += 1
    #         if i > 3:
    #             ex.end_at = random.choices(('2021-12-12 16:00', '2021-12-09 16:00', '2021-12-17 16:00')).pop()
    #             ex.save()
    #             print('exhibition ended')
    #         print('exhibition --> ' + str(ex))

    for ex in Exhibition.objects.all():
        for _ in range(random.randint(3, 7)):
            w = WorkFactory(exhibition=ex)
            print('work --> ' + str(w))

    print("completed.")
