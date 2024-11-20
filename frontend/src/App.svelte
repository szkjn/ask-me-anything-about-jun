<script>
  import { marked } from "marked";

  let question = "";
  let loading = false;
  let error = "";
  let history = [];
  let initialState = true;
  const initialQuestions = [
    "Any experience in Data Engineering ?",
    "Have you contributed to AI talks ?",
    "What NLP libraries do you master?",
  ];
  let followUpQuestions = [];

  // Function to handle follow-up question clicks
  function handleFollowUpClick(followUpQuestion) {
    question = followUpQuestion;
    followUpQuestions = [];
    sendChatMessage();
  }

  // Function to send the question to the backend
  async function sendChatMessage() {
    if (!question.trim()) return;

    // Add user's question to history immediately
    history = [...history, { role: "user", content: question }];
    initialState = false;
    followUpQuestions = [];

    let userQuestion = question;
    question = "";
    loading = true;
    error = "";

    let accumulatedResponse = "";

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
      fetchFollowUpQuestions(userQuestion, accumulatedResponse);
    }
  }

  // Add this function to fetch follow-up questions
  async function fetchFollowUpQuestions(userQuestion, assistantAnswer) {
    try {
      const response = await fetch("http://localhost:5000/follow-ups", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
          answer: assistantAnswer,
        }),
      });

      if (!response.ok) {
        throw new Error("Error fetching follow-up questions.");
      }

      const questions = await response.json();
      followUpQuestions = questions;
    } catch (error) {
      console.error("Error fetching follow-up questions:", error);
    }
  }
</script>

<main class="container">
  <div class="header"><h2>Chat with Jun's CV</h2></div>

  <div class="chat-box">
    <!-- <ul class="f-up-questions">
      <li class="f-up-question">
        Quelles expériences professionnelles as-tu en Python ?
      </li>
      <li class="f-up-question">
        Quelles expériences professionnelles as-tu en Python ?
      </li>
    </ul> -->
    {#if initialState}
      <div class="initial-window">
        <div class="initial-message">Ask me anything</div>
        <div class="initial-questions">
          <ul class="f-up-questions">
            {#each initialQuestions as question}
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              <li
                class="f-up-question"
                on:click={() => handleFollowUpClick(question)}
              >
                {question}
              </li>
            {/each}
          </ul>
        </div>
      </div>
    {:else}
      {#each history as msg (msg.content)}
        <div class="message {msg.role}">
          {@html marked(msg.content)}
        </div>
      {/each}
      <ul class="f-up-questions">
        {#each followUpQuestions as followUpQuestion}
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <li
            class="f-up-question"
            on:click={() => handleFollowUpClick(followUpQuestion)}
          >
            {followUpQuestion}
          </li>
        {/each}
      </ul>
    {/if}
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
    max-width: 780px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
    background-color: #222;
    color: #bbb;
    border-radius: 6px;
    /* border: 1px solid #555; */
    min-height: 80vh;
  }
  .chat-box {
    /* width: 100%; */
    max-height: 67vh;
    padding: 1rem 1rem 2rem 1rem;
    border: 1px solid #333;
    background-color: #151515;
    color: #ddd;
    height: 80%;
    font-size: 0.9rem;
    line-height: 1.5;
    overflow-y: auto;
  }

  .initial-window {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
  }

  .initial-message {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 25%;
    font-size: 1.25rem;
  }

  .initial-questions {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .f-up-questions {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    margin: 0;
  }

  .f-up-question {
    border: 1px solid #555;
    border-radius: 20px;
    padding: 0.5rem 0.75rem;
    margin: 0.2rem;
    width: fit-content;
    color: #ddd;
    /* font-size: 0.8rem; */
    cursor: pointer;
  }

  .f-up-question:hover {
    background-color: #222;
  }

  .message {
    display: block;
    margin-bottom: 10px;
    margin-left: auto;
  }
  .message.user {
    background-color: #1b1b1b;
    border: 1px solid #222;
    border-radius: 30px;
    color: #ddd;
    padding: 1px 1.5rem;
    width: fit-content;
    /* margin: 0 !important; */
    margin-bottom: 1rem;
  }
  .message.assistant {
    text-align: left;
    color: #ddd;
    /* padding-bottom: 1rem; */
  }
  .input-section {
    width: 780px;
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
