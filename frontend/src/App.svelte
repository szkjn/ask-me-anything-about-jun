<script>
  import { marked } from "marked";

  let question = "";
  let loading = false;
  let error = "";
  let history = [];

  // Function to send the question to the backend
  async function sendChatMessage() {
    if (!question.trim()) return;

    loading = true;
    error = "";

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question, history }),
      });

      const data = await response.json();
      console.log("API response", data);

      if (response.ok && data.answer) {
        history = [...history, { role: "user", content: question }];
        history = [...history, { role: "assistant", content: data.answer }];
        question = "";
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
  <h2>Ask Me Anything (About Myself)</h2>

  <div class="chat-box">
    {#each history as msg (msg.content)}
      {msg.role}
      <div class="message {msg.role}">
        {@html marked(msg.content)}
        <!-- Render content with Markdown -->
      </div>
    {/each}
  </div>

  <div class="input-section">
    <input
      type="text"
      placeholder="Type your message..."
      bind:value={question}
      class="input"
      disabled={loading}
      on:keydown={(e) => e.key === "Enter" && sendChatMessage()}
    />

    <button on:click={sendChatMessage} class="button" disabled={loading}>
      {loading ? "Sending..." : "Send"}
    </button>
  </div>

  {#if error}
    <p class="error"><strong>Error:</strong> {error}</p>
  {/if}
</main>

<style>
  .container {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
    padding: 0 20px;
    font-family: Arial, sans-serif;
    background-color: #f0f6fc;
    background-color: #0d1117;
    color: #bbb;
    border-radius: 6px;
    border: 1px solid #555;
    min-height: 80vh;
  }
  h2 {
    text-align: left;
  }
  .chat-box {
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 20px;
    border: 1px solid #ddd;
    padding: 10px;
    color: #ddd;
    height: 80vh;
  }
  .message {
    display: block;
    margin-bottom: 10px;
  }
  .message.user {
    text-align: right;
    color: #ddd;
  }
  .message.assistant {
    text-align: left;
    color: #ddd;
    font-weight: bold;
  }
  .input-section {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .input {
    width: 80%;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    background-color: #151b23;
    color: #f0f6fc;
  }
  .button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    width: 18%;
  }
  .button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  .answer {
    margin-top: 20px;
    text-align: left;
    white-space: pre-wrap;
  }
  .error {
    color: red;
    margin-top: 20px;
  }
</style>
