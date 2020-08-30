from api.views.processing_views import ProcessingListView

from rest_framework import routers


router = routers.DefaultRouter()

router.register('processing', ProcessingListView.as_view(), basename = 'processing_list')
