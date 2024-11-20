import logging
from typing import List
from openai import OpenAI, Stream
from utils.config import OPENAI_API_KEY
from utils.schemas import AnswerPath, FollowUpQuestions
from utils.prompts import ANSWER_PATH_ASSESSMENT_PROMPT, FOLLOW_UP_QUESTION_PROMPT


class OpenAIService:
    def __init__(self):
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            logging.info("OpenAI client initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize OpenAI client: {e}")
            raise e

    def generate_embedding(self, question: str) -> list:
        """
        Generates an embedding for the given question using the OpenAI API.

        Args:
            question: The question for which to generate an embedding.

        Returns:
            list: The embedding vector for the question.
        """
        logging.info(f"Generating embedding for question: {question}")

        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002", input=question
            )
            return response.data[0].embedding
        except Exception as e:
            logging.error(f"Error generating embedding for question: {e}")
            raise

    def generate_chat_response(self, history: list) -> Stream:
        """
        Generates a chat response using the OpenAI API based on the conversation history.

        Args:
            history: A list of messages representing the conversation history.

        Returns:
            Stream: A stream of chat response tokens.
        """
        logging.info(f"Generating chat response with history")

        try:
            stream = self.client.chat.completions.create(
                model="gpt-4o-mini", messages=history, max_tokens=1000, stream=True
            )
            return stream
        except Exception as e:
            logging.error(f"Error generating chat response: {e}")
            raise

    def assess_question(self, question: str) -> int:
        """
        Assesses an 'Answer Path' of a question based on the contextual relevance :
        - answer_path = 0: The question is about general information on Jun's CV
        - answer_path = 1: The question is about Jun's recent activities such as blog posts, publications and talks

        Args:
            quesiton: The question to be assessed.

        Returns:
            int: An integer representing the 'Answer Path' to be followed dowstream.
        """
        logging.info(f"Assessing question: {question}")
        assessment_message = ANSWER_PATH_ASSESSMENT_PROMPT + question

        try:
            assessment_response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": assessment_message}],
                max_tokens=40,
                response_format=AnswerPath,
            )
            assessment_answer = assessment_response.choices[0].message.parsed
            logging.info(f"Answer Path Assessment: {assessment_answer.answer_path}")
            return assessment_answer.answer_path
        except Exception as e:
            logging.error(f"Error in assessing the question: {e}")
            return 0

    def generate_follow_up_questions(self, question: str, answer: str) -> List[str]:
        """
        Generates two relevant follow-up questions based on the latest user's question and the corresponding answer.

        Args:
            question: The latest user's question.
            answer: The most recent answer.

        Returns:
            List[str]: A list of two relevant follow-up questions.
        """
        logging.info("Generating follow-up questions")
        follow_up_context = f"User's question: {question}\n\nAnswer: {answer}"

        try:
            follow_up_response = self.client.beta.chat.completions.parse(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": FOLLOW_UP_QUESTION_PROMPT},
                    {"role": "user", "content": follow_up_context},
                ],
                max_tokens=200,
                response_format=FollowUpQuestions,
            )

            # Parse the follow-up questions from the chat response
            follow_up_questions = follow_up_response.choices[0].message.parsed

            results = [
                follow_up_questions.follow_up_1,
                follow_up_questions.follow_up_2,
            ]

            return results
        except Exception as e:
            logging.error(f"Error while generating follow-up questions: {e}")
            raise
