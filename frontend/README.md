### Frontend

The frontend is a Svelte-based application that provides a user-friendly interface for submitting questions and receiving answers.

- **User Input:**

  - A single input field for users to ask questions.

- **Dynamic Updates:**

  - Displays the response from the backend in real-time.

- **Keyboard Submission:**
  - Supports pressing Enter for question submission.

**Key Components:**

1. **App.svelte:**

   - The main Svelte component handling user input, API calls, and response rendering.

2. **Question Suggestions:**

Suggests relevant follow-up questions based on the latest interaction.

3. **API Integration:**
   - Sends user queries to the `/ask` endpoint in the backend.

**Directory Structure:**

```
frontend/
│
├── public/                 # Publicly served assets
│
├── src/                    # Source files
│   ├── App.svelte          # Main Svelte application
│   └── main.js             # Entry point for the Svelte app
│
└── package.json            # Project dependencies

```
