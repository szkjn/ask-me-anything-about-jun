<script>
  let question = "";
  let answer = "";
  let loading = false;
  let error = "";

  // Function to send the question to the backend
  async function askQuestion() {
    loading = true;
    error = "";
    answer = "";

    try {
      const response = await fetch("http://localhost:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();

      if (response.ok) {
        answer = data.answer;
      } else {
        error =
          data.error || "An error occurred while processing your question.";
      }
    } catch (err) {
      error = "Failed to connect to the backend.";
    } finally {
      loading = false;
    }
  }
</script>

<main class="container">
  <h1>Ask Me Anything</h1>
  <p>Type a question to learn more about me:</p>

  <input
    type="text"
    placeholder="Type your question here"
    bind:value={question}
    class="input"
    disabled={loading}
  />

  <button on:click={askQuestion} class="button" disabled={loading || !question}>
    {loading ? "Loading..." : "Submit"}
  </button>

  {#if answer}
    <p><strong>Answer:</strong> {answer}</p>
  {/if}
  {#if error}
    <p style="color: red;"><strong>Error:</strong> {error}</p>
  {/if}
</main>

<style>
  .container {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
    padding: 20px;
    font-family: Arial, sans-serif;
    background-color: #ddd;
  }
  .input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  .button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  .button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  .answer {
    margin-top: 20px;
    font-weight: bold;
  }
  .error {
    color: red;
    margin-top: 20px;
  }
</style>
