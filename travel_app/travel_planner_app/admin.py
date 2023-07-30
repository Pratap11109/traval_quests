from django.contrib import admin
from travel_planner_app.models import TravelGroup, BudgetPlanner
from .models import Review
# Register your models here.
admin.site.register(TravelGroup)
admin.site.register(BudgetPlanner)
admin.site.register(Review)
