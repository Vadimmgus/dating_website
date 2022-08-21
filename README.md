# Web-site for dating

## Main task:

   Create backend for dating web-site.

### Tasks:

1. Create a participant model. The participant must have an avatar, gender, first and last name, mail.
2. Create a new member registration endpoint: `/api/clients/create`.
3. When registering a new participant, it is necessary to process his avatar: put a watermark on it.
4. Create an evaluation endpoint by a member of another member: `/api/clients/{id}/match`. In the event that mutual sympathy arises, then we issue a mail to the client in response and send it to the mail of the participants: `“You liked <name>! Participant's mail: <mail>"`.
5. Create a member list endpoint: `/api/list`. It should be possible to filter the list by gender, first name, last name.
6. Implement the definition of the distance between the participants. Add longitude and latitude fields. Add an additional filter to the list api that shows participants within a given distance relative to an authorized user.

## Installation and run:

1. Clone the repository:

   ```bash
   git clone 
   ```

1. Create and fill up a `.env` file according to the template `/DRF_blog/.env.template`. The `.env` file must be in the same directory as `settings.py`

1. Run containers in docker:

   ```bash
   docker-compose up -d --build
   ```

1. Run a migration:

   ```bash
   docker-compose run --rm web sh -c "python3 manage.py migrate"
   ```

1. Create a superuser:

   ```bash
   docker-compose run --rm web sh -c "python3 manage.py createsuperuser"
   ```
  
1. Collect static files:

   ```bash
   docker-compose run --rm web sh -c "python3 manage.py collectstatic"
   ```

1. Get a list of endpoints by url:

   ```html
   http://127.0.0.1:8011/swagger/ - documentation for API
   ```
