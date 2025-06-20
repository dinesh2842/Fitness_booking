from django.db import models

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} at {self.datetime} {self.instructor}'
    
    class meta:
        verbose_plural_name = 'FitnessClasses'
    
class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass,on_delete=models.CASCADE)
    client_name = models.CharField(max_length=50)
    client_id = models.PositiveIntegerField(default=0)
    client_email = models.EmailField(max_length=50)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'booking by {self.client_email}  at  {self.fitness_class}'
    
    