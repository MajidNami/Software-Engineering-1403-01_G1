from django.db import models

NUM_BOXES = 9
BOXES = range(1, NUM_BOXES + 1)

class Word(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=150)
    box = models.IntegerField(
        choices=zip(BOXES, BOXES),
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)
    
    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]

        if new_box in BOXES:
            self.box = new_box
            self.save()

        return self

    def __str__(self):
        return self.word
    