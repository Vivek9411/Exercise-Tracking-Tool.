# Calorie Tracking Web App

This project is a web application for tracking calories, powered by Flask, SQLAlchemy, SpaCy, and Flask-Form. It helps users calculate their calorie intake and track their nutritional needs.

## Requirements

- **Flask**
- **SpaCy**
- **Flask-WTF** (Flask Forms)
- **Flask-SQLAlchemy**

You can install the required libraries using `pip`:

```bash
pip install Flask spacy Flask-WTF Flask-SQLAlchemy
```

## How to Run the App

1. **Run the Backend:**

   Navigate to the `calorie_tracking_backend` directory in your project, where the backend file `complete_process_api.py` is located.

   Run the backend with the following command:

   ```bash
   python complete_process_api.py
   ```

2. **Configure the Backend URL:**

   After running the backend, you'll need to configure the URL of the backend in the **calorie tracking app**. Go to the appropriate settings in your frontend or configuration file and add the URL where the backend is running.

3. **Run the Frontend:**

   Now, you can run the `app.py` file located in the root directory of the frontend app.

   Before starting the frontend, **remember to turn off debug mode** in the `app.py` file. You can do this by setting `debug=False` in the app's run method:

   ```python
   app.run(debug=False)
   ```

   Then, run the app:

   ```bash
   python app.py
   ```

Your application should now be live and ready to use!

---

## Notes

- Ensure that both the backend and frontend are running simultaneously for the app to function correctly.
- If you're running the backend on a different server or port, make sure to update the URL in the frontend accordingly.

---

