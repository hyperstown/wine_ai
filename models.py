from core import models


class Wine(models.Base, models.BaseModelMixin):

    id = models.auto_field('wines')
    name = models.string_field(max_length=120)
    type = models.string_field(max_length=120)
    price = models.int_field()
    is_alcoholic = models.boolean_field()
    is_vegan = models.boolean_field()
