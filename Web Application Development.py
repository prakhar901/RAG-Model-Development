from rest_framework import generics
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer

class DocumentListView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentDetailView(generics.RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

# Add views for RAG model interaction and user authentication as needed
from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DocumentList = () => {
    const [documents, setDocuments] = useState([]);

    useEffect(() => {
        const fetchDocuments = async () => {
            const response = await axios.get('/api/documents/');
            setDocuments(response.data);
        };
        fetchDocuments();
    }, []);

    return (
        <div>
            <h1>Document List</h1>
            <ul>
                {documents.map(document => (
                    <li key={document.id}>{document.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default DocumentList;
import React from 'react';
import DocumentList from './components/DocumentList';

function App() {
  return (
    <div className="App">
      <DocumentList />
    </div>
  );
}

export default App;
from django.urls import path
from .views import DocumentListView, DocumentDetailView

urlpatterns = [
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    # Add URLs for RAG model interaction and user authentication as needed
]
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title
{
  "name": "rag_frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "axios": "^0.21.1",
    "react": "^17.0.2",
    "react-dom": "^17.0.2",
    "react-scripts": "4.0.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
