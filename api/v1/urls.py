"""urls
Example:

    from api.v1.index import Index
    urlpatterns = [
        ('index/', Index)
    ]
"""
from api.v1.components import Components
from api.v1.users import LoginApiView
from api.v1.tasks import Tasks

urlpatterns = [
    ('components/', Components),
    ('login/', LoginApiView),
    ('tasks/', Tasks)
]
