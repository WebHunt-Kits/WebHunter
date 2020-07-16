"""urls
Example:

    from api.v1.index import Index
    urlpatterns = [
        ('index/', Index)
    ]
"""
from api.v1.components import Components, SpecifyComponents
from api.v1.users import LoginApiView

urlpatterns = [
    ('components/', Components),
    ('components/<string:c_id>/', SpecifyComponents),
    ('login/', LoginApiView)
]
