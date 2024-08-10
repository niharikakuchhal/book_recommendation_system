# Book Recommendation System

## Project Overview

The Book Recommendation System is a web application designed to allow users to recommend books, view recommendations, and interact with comments and likes. Built using Django, this project demonstrates a full-featured book recommendation system with user authentication, search functionality, and dynamic content.

## Features

- **User Authentication**: Users can register, log in, and manage their accounts.
- **Book Recommendations**: Users can add, view, and recommend books.
- **Search Functionality**: Users can search for books by title, author, or keywords.
- **Likes and Comments**: Users can like and comment on book recommendations.
- **Responsive Design**: The application is designed to be user-friendly on both desktop and mobile devices.

## Technologies Used

- Django
- Python
- HTML/CSS
- JavaScript
- Bootstrap (for styling)

## Installation

Follow these steps to set up the project on your local machine:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/niharikakuchhal/book_recommendation_system.git
   cd book_recommendation_system

2. **Create and Activate a Virtual Environment**

    ```bash
    python -m venv myenv
    myenv\Scripts\activate

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt

4. **Apply Migrations**

    ```bash
    python manage.py migrate

5. **Create a Superuser (Optional, for admin access)**
    ```bash
    python manage.py createsuperuser

6. **Run the Development Server**

    ```bash
    python manage.py runserver

Navigate to http://127.0.0.1:8000/ in your web browser to view the application.

## Usage
- **Register/Log In:** Create an account or log in to access the full functionality.
- **Add Recommendations:** Use the "Recommend a Book" form to submit new book recommendations.
- **View Recommendations:** Browse through the list of recommended books.
- **Like and Comment:** Interact with book recommendations by liking and commenting on them.
- **Search:** Use the search functionality to find books by title, author, or keywords.

## Contributing

If you would like to contribute to the project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature').
5. Push to the branch (git push origin feature-branch).
6. Create a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
