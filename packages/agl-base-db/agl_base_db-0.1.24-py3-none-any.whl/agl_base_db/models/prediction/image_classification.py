from django.db import models

class ImageClassificationPrediction(models.Model):
    """
    A class representing an image classification prediction.

    Attributes:
        label (Label): The label of the prediction.
        frame (Frame): The frame of the prediction.
        confidence (float): The confidence of the prediction.
        date_created (datetime): The date the prediction was created.

    """
    label = models.ForeignKey("Label", on_delete=models.CASCADE, related_name="image_classification_predictions")
    frame = models.ForeignKey("Frame", on_delete=models.CASCADE, blank=True, null=True, related_name="image_classification_predictions")
    legacy_frame = models.ForeignKey("LegacyFrame", on_delete=models.CASCADE, blank=True, null=True, related_name="image_classification_predictions")
    legacy_image = models.ForeignKey("LegacyImage", on_delete=models.CASCADE, blank=True, null=True, related_name="image_classification_predictions")
    value = models.BooleanField()
    confidence = models.FloatField()
    model_meta = models.ForeignKey("ModelMeta", on_delete=models.CASCADE, related_name="image_classification_predictions")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('label', 'frame', 'model_meta')
