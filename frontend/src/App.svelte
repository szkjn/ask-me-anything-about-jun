<script>
  import { marked } from "marked";

  let question = "";
  let loading = false;
  let error = "";
  let history = [];

  // Function to send the question to the backend
  async function sendChatMessage() {
    if (!question.trim()) return;

    // Add user's question to history immediately
    history = [...history, { role: "user", content: question }];
    let userQuestion = question; // Store the question temporarily
    question = ""; // Clear input field for new entry

    loading = true;
    error = "";

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: userQuestion, history }),
      });

      if (!response.ok) {
        throw new Error(
          (await response.json()).error || "Error processing the message."
        );
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let accumulatedResponse = ""; // Use this to accumulate the complete response

      // Add a placeholder message for the assistant
      const assistantMessage = { role: "assistant", content: "" };
      history = [...history, assistantMessage];

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        accumulatedResponse += chunk;

        // Update the assistant message in the history with current accumulated response
        assistantMessage.content = accumulatedResponse;
        history = [...history.slice(0, -1), assistantMessage]; // Update only the last assistant message
      }

      // Finalize response addition to the history
      history = [
        ...history.slice(0, -1),
        { role: "assistant", content: accumulatedResponse },
      ];
    } catch (err) {
      error = "Failed to connect to the backend.";
    } finally {
      loading = false;
    }
  }
</script>

<main class="container">
  <div class="header"><h2>Chat with Jun Suzuki's CV</h2></div>

  <div class="chat-box">
    {#each history as msg (msg.content)}
      <div class="message {msg.role}">
        {@html marked(msg.content)}
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

    <button
      on:click={sendChatMessage}
      class="button"
      disabled={loading || !question.trim()}
    >
      <img
        src="https://img.icons8.com/ios-filled/50/000000/up.png"
        alt="Up Arrow"
        title="Up arrow icons created by Roundicons Premium - Flaticon"
        style="width: 25px; height: 25px;"
      />
    </button>
  </div>

  {#if error}
    <p class="error"><strong>Error:</strong> {error}</p>
  {/if}
</main>

<style>
  .container {
    display: flex;
    flex-direction: column;
    height: 98vh;
    max-width: 700px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
    background-color: #222;
    color: #bbb;
    border-radius: 6px;
    /* border: 1px solid #555; */
    min-height: 80vh;
  }
  .header {
    /* border-bottom: 1px solid #333; */
  }
  .chat-box {
    /* width: 100%; */
    max-height: 67vh;
    padding: 1rem 1rem 2rem 1rem;
    /* border: 1px solid #ddd; */
    background-color: #111;
    color: #ddd;
    height: 80%;
    font-size: 0.9rem;
    line-height: 1.5;
    overflow-y: auto;
  }
  .message {
    display: block;
    margin-bottom: 10px;
    margin-left: auto;
  }
  .message.user {
    background-color: #181818;
    border-radius: 20px;
    color: #ddd;
    padding: 1px 1.25rem;
    width: fit-content;
    margin-bottom: 1rem;
  }
  .message.assistant {
    text-align: left;
    color: #ddd;
    /* padding-bottom: 1rem; */
  }
  .input-section {
    width: 700px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    background-color: #222;
    padding: 26px 0 20px 0;
    /* box-shadow: inset 0 1px 0 0 #333; */
    /* border: 1px solid red; */
  }
  .input {
    width: 90%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    background-color: #151515;
    color: #f0f6fc;
  }
  .button {
    padding: 7px 20px;
    background-color: #ddd;
    color: white;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    width: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .button:disabled {
    background-color: #555;
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
