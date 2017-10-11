import logging

import os

from instagram_alpha.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True, default_retry_delay=3, max_retries=3)
def get_image_labels(self, image_id):
    from instagram_alpha.settings import GOOGLE_OAUTH2_CLIENT_SECRETS_JSON
    from dashboard.models import Picture, Label, Landmarks
    from dashboard.google_vision_lib import GoogleVision

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_OAUTH2_CLIENT_SECRETS_JSON

    try:
        picture = Picture.objects.get(id=image_id)
    except Picture.DoesNotExist:
        logger.exception('Could not find picture.')
        return

    file_name = picture.image.path
    try:
        google_vision = GoogleVision(file_name)
        image_labels = google_vision.get_image_labels()
        image_landmarks = google_vision.get_image_landmarks()
    except Exception as e:
        logger.exception("Exception: ".format(str(e)))
        raise self.retry(exc=Exception())
    else:
        if image_labels:
            picture.labels.all().delete()

            labels_to_add = []
            for label in image_labels:
                labels_to_add.append(Label(picture=picture, name=label.description, score=label.score))

            Label.objects.bulk_create(labels_to_add)
        if image_landmarks:
            picture.landmarks.all().delete()
            landmarks_to_add = []
            for landmark in image_landmarks:
                for location in landmark.locations:
                    lat_lng = location.lat_lng
                    landmarks_to_add.append(
                        Landmarks(picture=picture, name=landmark.description, lat=lat_lng.latitude, lng=lat_lng.longitude)
                    )

            Landmarks.objects.bulk_create(landmarks_to_add)

        # TODO send data to user by socket

        return True

