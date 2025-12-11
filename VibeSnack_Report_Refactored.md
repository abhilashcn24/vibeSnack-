# VibeSnack: Context-Aware Snack Recommendation System

**Project Report**

---

### **Abstract**

VibeSnack is a context-aware snack recommendation system designed to help users easily find suitable snacks based on real-time factors such as mood, hunger, dietary preference, current activity, and situational context. The system uses a Random Forest classifier trained on 10,000 synthetically generated data samples to learn complex patterns between user context and snack choices, providing top-K recommendations. To improve transparency, the system integrates Explainable AI that generates personalized reasoning for each suggestion. 

Unlike traditional static tools, VibeSnack is built as a modern full-stack web application. It features a robust **FastAPI** backend that serves predictions and manages data, coupled with a dynamic **React** frontend styled with **Tailwind CSS** for a premium, responsive user experience. Data persistence for user history and feedback is handled by **MongoDB**, ensuring scalability. The system aims to reduce decision fatigue and deliver intelligent snack suggestions for a wide range of users such as students, office workers, fitness enthusiasts, gamers, and night-time users.

---

### **Introduction**

Modern users often face difficulty in choosing the right snack depending on factors like their mood, hunger level, activities, or diet restrictions. With many snack options available, users often feel overwhelmed, leading to poor or random choices. VibeSnack addresses this by using an AI-based recommendation engine that processes contextual inputs to deliver tailored snack suggestions.

The purpose of the project is to design a system that understands user context — such as time of day, hunger, mood, dietary needs, and current activity — and recommends snacks intelligently. The main objectives include collecting contextual inputs, training an ML model for prediction, generating top-K recommendations with confidence scores, ensuring diet-based filtering, producing explainable reasoning, and creating a highly interactive user interface using React and Framer Motion.

---

### **Existing and Proposed System**

Users typically struggle with snack decisions due to a lack of personalized guidance. The proposed VibeSnack system introduces several enhancements over traditional manual selection. 

The solution utilizes a **Random Forest** machine learning model trained on synthetic data to predict the best snack categories. Key features include:
*   **Context-Aware Encoding**: intelligently processing inputs like "Late Night" or "Study Session".
*   **Real-Time Recommendations**: Served via a high-performance REST API.
*   **Strict Diet-Based Filtering**: Ensuring recommendations meet user constraints (e.g., Vegan, Gluten-Free).
*   **Personalization**: Utilizing user feedback history stored in MongoDB to refine future suggestions.
*   **Explainable AI**: Providing clear reasons for every recommendation (e.g., "High protein for your workout").

The interface is implemented using **React**, offering a seamless Single Page Application (SPA) experience with dark mode support and smooth animations.

---

### **System Requirements**

**Hardware Requirements:**
*   Processor: 64-bit Multi-core processor (Intel i5/Ryzen 5 or better recommended).
*   RAM: 8GB or higher (for running frontend, backend, and database services simultaneously).
*   Storage: 500MB free space.

**Software Requirements:**
*   **Operating System**: Windows 10/11, macOS, or Linux.
*   **Backend Runtime**: Python 3.12+.
*   **Frontend Runtime**: Node.js (v18+).
*   **Database**: MongoDB (Local or Atlas).
*   **Key Libraries & Frameworks**:
    *   *Backend*: FastAPI, Uvicorn, Scikit-learn, Pandas, NumPy, Joblib, Motor (MongoDB driver).
    *   *Frontend*: React, Vite, Tailwind CSS, Framer Motion, Axios, Lucide-React.
    *   *Tools*: VS Code, Git, Postman (for API testing).

---

### **System Design**

VibeSnack follows a modern **Client-Server Architecture**:

1.  **Presentation Layer (Frontend)**: Built with **React** and **Vite**. It handles user interactions, displays the form for context input, and renders recommendations using responsive cards and animations. It communicates with the backend via HTTP requests (Axios).
2.  **Business Logic Layer (Backend)**: A **FastAPI** application acts as the core controller. It exposes REST endpoints (e.g., `/predict`, `/feedback`) to handle requests. It loads the trained Machine Learning model and orchestrates the logic for filtering and explanation generation.
3.  **Machine Learning Layer**: Contains the **Random Forest Classifier** pipeline (trained using Scikit-learn) and utility functions for feature encoding and probability estimation.
4.  **Data Layer**: **MongoDB** is used to store global user feedback and interaction history, allowing the system to learn from population trends over time. Static snack catalogs are loaded from optimized JSON/CSV files.

**Use Cases**:
*   **Get Recommendations**: User inputs context (Mood: Happy, Activity: Gaming); Frontend sends data to `/predict`; Backend returns ranked snacks with explanations.
*   **Submit Feedback**: User clicks a snack; Frontend sends the selection to `/feedback`; Backend updates the count in MongoDB to influence future popularity scores.

---

### **Implementation**

The implementation is divided into two main components:

**1. Backend (FastAPI):**
The `main.py` file initializes the FastAPI app and defines routes. The `/predict` endpoint accepts user context, preprocesses it using `model_utils.py`, and queries the loaded Random Forest model. It applies post-processing logic to filter by diet and generate natural language explanations. The `/feedback` endpoint updates the `user_history` collection in MongoDB.

**2. Frontend (React):**
The `App.jsx` serves as the main entry point. It manages state for user inputs (mood, hunger, etc.) and recommendation results. The UI is broken down into modular components (though currently centralized for simplicity in the prototype). **Tailwind CSS** is used for styling, implementing a sleek dark theme with glassmorphism effects. **Framer Motion** adds entrance animations to the recommendation cards, making the application feel responsive and polished.

---

### **Testing**

The project was validated using a comprehensive testing strategy:

*   **Unit Testing**: Python functions for data preprocessing and model prediction were tested in isolation to ensure accurate encoding of categorical variables.
*   **API Testing**: The FastAPI endpoints (`/predict`, `/health`) were tested using Swagger UI and Postman to verify correct JSON response structures and error handling (e.g., database connection failures).
*   **Integration Testing**: Verified the end-to-end flow from the React frontend form submission to the MongoDB database update.
*   **User Acceptance Testing**: Evaluated the UI/UX, confirming that the dark mode is visually appealing, animations are smooth, and recommendations are relevant to the input context (e.g., suggesting "Popcorn" for "Movie" context).

---

### **Future Enhancements**

*   **User Authentication**: Implement JWT-based login to track individual user history rather than global history.
*   **Mobile Application**: Wrap the React application using React Native or Capacitor for iOS/Android deployment.
*   **Nutritional API Integration**: Fetch real-time nutritional data (calories, macros) from external APIs like USDA or FatSecret.
*   **Deep Learning**: Upgrade the Random Forest model to a Neural Network for capturing more complex non-linear relationships in user behavior.

---

### **Conclusion**

VibeSnack successfully demonstrates the power of combining modern full-stack web development with machine learning. By migrating from a simple script-based interface to a robust Client-Server architecture, the system offers better scalability, a superior user experience, and a foundation for future growth. It effectively solves the problem of "snack decision fatigue" by providing intelligent, context-aware, and explainable recommendations.

---

### **References**

*   **FastAPI Documentation**: https://fastapi.tiangolo.com/
*   **React Documentation**: https://react.dev/
*   **Scikit-learn User Guide**: https://scikit-learn.org/stable/user_guide.html
*   **Tailwind CSS**: https://tailwindcss.com/
*   **MongoDB Manual**: https://www.mongodb.com/docs/manual/
