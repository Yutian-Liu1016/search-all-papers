# Get All Paper

This project is a simple web application built with Flask that allows users to search for all published papers of a computer science scholar from DBLP.

## Project Structure

```
get_all_paper
├── app
│   ├── __init__.py          # Initializes the Flask application and sets up configurations
│   ├── routes.py            # Defines the application routes and handles user requests
│   ├── static
│   │   ├── css
│   │   │   └── styles.css    # Contains CSS styles for the web application
│   │   └── js
│   │       └── scripts.js     # Contains JavaScript for front-end logic and user interaction
│   ├── templates
│   │   └── index.html        # Main HTML template with user input form and result display
├── requirements.txt          # Lists the required Python libraries and dependencies
├── run.py                    # Entry point to run the Flask development server
└── README.md                 # Project documentation and instructions
```

## Installation

1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```
python run.py
```

The application will be accessible at `http://127.0.0.1:5000/`.

## Features

- List all papers of the author.
- Only display the first matched author.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.
