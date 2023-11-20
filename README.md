# FlightX
Flight Ticket Booking API 
This is a Flight Ticket Booking API built from scratch using Flask and MongoDB Atlas. The API is documented using Swagger.
The API is Hosted in Render https://flightx-4fxd.onrender.com<br/>
Kindly Visit the Above site to see the project.<br/>
Admin Credentials:
  username:admin
  password: admin123

Note: This project was developed for the second round of Presidio recruitment process. Keeping in mind that reviewers from the organisation would test my system I have left the credentials out in open (For Now). 
Anyone outside the organisation kindly don't abuse it. Also, kindly follow "YYYY-MM-DD" format for inputing dates to the API.

Admin Use Cases:
1. /adminLogin: When logged in with credentials a API Key of TTL 60 mins in created. This key can be used to access the other admin endpoints. 
2. /addFllight: Allows admin to add flights to the DB. The flight_id must be unique for that particular date i.e. same flight Id can be used in future dates. The admin can't add
    flight to old dates.
3. /viewBookings: Allows the admin to filter the ticket bookings by flight name, flight Id and date. If no query is given then all the tickets are returned.

User Use Cases:
1. /userSignup: The user is allowed to signup to the system. The username and email must be unique and valid. Kindly follow the format described in the API documentation for the input format.
2. /userLogin: Similar to admin login. Generates an API key that would be alive for 60 mins.
3. /searchFlight: Allows user to seacrh for flight and filter it based on flight name, flight Id or date.
4.  /bookTicket: Allows the user to book ticket in the flight. Returns a booking Id on succssfull booking.

   
