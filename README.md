# DIY Blog

This is a Django-based blog project that allows users to create and manage their own blog posts. It provides a user-friendly interface for writing, editing, and publishing blog articles.

## Inspiration

The design of this blog was inspired by a Dribbble project created by [Abhinav Chhikara](https://dribbble.com/shots/2463983-Blog-design). The design showcases a modern and visually appealing layout that enhances the overall user experience.

## Features

- User registration and authentication
- Create, edit, and delete blog posts
- Commenting system for readers to engage with the content

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/Lionel-hub1/diyblog.git
   ```
2. Navigate to the project directory:
   ```bash
   cd diyblog
   ```
3. Create a virtual environment:
   ```
   python -m venv venv
   ```
   or activate an existing one by running
   ```bash
   source venv/bin/activate
   ```
   (Linux/Mac) or
   ```
   venv\Scripts\activate
   ```
   (Windows)
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up the database:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the blog by visiting `http://localhost:8000` in your web browser.
2. Explore the blog, read articles, and interact with the content.
3. Optionally register a new account or log in with your existing credentials.
4. (Require Login) Create your own blog posts by clicking on the "New Post" button.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the [GitHub repository](https://github.com/Lionel-hub1/diyblog).

## License

This project is licensed under the [MIT License](./LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.
