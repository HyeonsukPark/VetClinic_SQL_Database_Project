# testing 
# Page loads (GET/pets, GET/owners, GET/vets, GET/appointments)
# Search appointment in the main page (GET/appointments/search?pet_name=xxx)

from locust import HttpUser, task, between
import random 

class VetClinicUser(HttpUser):
    wait_time = between(1, 3) # Simulate user think time between 1 and 3 seconds
    
    # Updated with real pet names from database
    pet_names = ["Luna", "Simba", "Daisy", "Leo", "Molly", "Bunny"]
    
    @task(6)
    def search_appointments(self):
        pet_name = random.choice(self.pet_names)
        self.client.get(f"/appointments/search?pet_name={pet_name}")
    
    @task(2) 
    def view_pets(self):
        self.client.get("/pets")
        
    @task(2)
    def view_owners(self):
        self.client.get("/owners")
        
    @task(2)
    def view_vets(self):
        self.client.get("/vets")
        
    @task(2)
    def view_appointments(self):
        self.client.get("/appointments")
        
    @task(2)
    def view_prescriptions(self):
        self.client.get("/prescription")
        
    @task(2)
    def view_medical_records(self):
        self.client.get("/medical-records")
        
    