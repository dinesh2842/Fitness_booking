create virtual environment virtualenv env  (in windows platform)
activate virtual environment env\Scripts\activate
pip install -r requirements.txt
make the necessary migrations using python manage.py makemigrations and python manage.py migrate
open the shell in the terminal using   python manage.py shell
after that run this inside the terminal to create a test data which is inside seed_data.py 
from booking_app.seed_data import run
run()
after that exit the terminal and create superuser using python manage.py createsuperuser to check the data (dont enter manually)
run the server using python manage.py runserver
test with postman or test using the port and the url 
testing with postman 
Method: POST (this is for creating new data)
URL: http://127.0.0.1:8000/book/
Body: raw JSON:

sample data with post request
{
  "fitness_class": 1,
  "client_name": "dinesh",
  "client_id": 123,
  "client_email": "dinesh@example.com"
}

to view all the classes present 
Method: GET
http://127.0.0.1:8000/classes/

to view all bookings made by a specific email address
Method: GET
http://127.0.0.1:8000/bookings/?email=dinesh@example.com

the slot will get reduced after successfull booking and throw an error if there is no slots
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "error": "No slots available"
}
the fitness booking app is successfully built .
you can view all these in the postman / or using urls or django admin
