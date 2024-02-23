# RAG-Model-Development
This code combines all the previous snippets into a single script that preprocesses PDF data, initializes the RAG model, trains it, evaluates its performance, and saves the trained model. Make sure to have your PDF documents placed in the 'pdf_documents' directory before running the script.

To run the web application, you'll need to start both the Django backend server and the React frontend development server separately. Here's how to do it:
1. Run Django Backend:
Navigate to the Django project directory where manage.py is located:

cd rag_project

2. Run the Django development server:
   
python manage.py runserver
This will start the Django backend server, which will serve the REST API 

3. Run React Frontend:
Open a new terminal or command prompt window.
Navigate to the React project directory where package.json is located:

cd rag_frontend

4. Install dependencies (if not installed already):
npm install

5.Start the React development server:
npm start
