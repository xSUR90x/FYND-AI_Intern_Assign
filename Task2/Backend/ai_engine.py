from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda,RunnableParallel,RunnablePassthrough
from pydantic import BaseModel, Field
from typing import Literal
import os


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   
    temperature=0.1,
)

class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="Overall sentiment of the review."
    )

sentiment_parser = PydanticOutputParser(pydantic_object=SentimentResult)

sentiment_prompt = PromptTemplate(
    template=(
        "You are a sentiment classifier.\n"
        "Classify the sentiment of the following user review and rating which is from 1 to 5 only,  strictly as 'positive' or 'negative'.\n\n"
        "Review:\n{review}\n\n"
        "Rating: {rating}/5\n"
        "{format_instructions}"
    ),
    input_variables=["review","rating"],
    partial_variables={"format_instructions": sentiment_parser.get_format_instructions()},
)

# feedback -> LLM -> SentimentResult
classifier_chain = sentiment_prompt | llm | sentiment_parser


# 2) STRUCTURED OUTPUT MODEL
class FeedbackAIOutputs(BaseModel):
    user_response: str = Field(description="Reply shown to the user.")
    summary: str = Field(description="Internal admin summary.")
    actions: str = Field(description="Recommended actions for the team.")

outputs_parser = PydanticOutputParser(pydantic_object=FeedbackAIOutputs)


# 3) BRANCH PROMPTS
positive_prompt = PromptTemplate(
    template=(
        "The following user feedback is POSITIVE.\n\n"
        "Rating: {rating}/5\n"
        "Review: \"\"\"{review}\"\"\"\n\n"
        "Generate a JSON object with the following keys:\n"
        "- user_response: a friendly thank-you style reply to the user (1–3 short sentences).\n"
        "- summary: a short internal summary of what the user liked or appreciated (1–2 sentences).\n"
        "- actions: concrete next steps for the team to continue improving (1–3 sentences).\n\n"
        "{format_instructions}"
    ),
    input_variables=["rating", "review"],
    partial_variables={"format_instructions": outputs_parser.get_format_instructions()},
)

negative_prompt = PromptTemplate(
    template=(
        "The following user feedback is NEGATIVE.\n\n"
        "Rating: {rating}/5\n"
        "Review: \"\"\"{review}\"\"\"\n\n"
        "Generate a JSON object with the following keys:\n"
        "- user_response: an empathetic, apologetic reply to the user (1–3 short sentences).\n"
        "- summary: a short internal summary of what went wrong from the user's perspective (1–2 sentences).\n"
        "- actions: specific improvement steps for the product/support team (1–3 sentences).\n\n"
        "{format_instructions}"
    ),
    input_variables=["rating", "review"],
    partial_variables={"format_instructions": outputs_parser.get_format_instructions()},
)
classifier_with_passthrough = RunnableParallel(
    sentiment_result=classifier_chain, 
    passthrough=RunnablePassthrough(),
) | RunnableLambda(lambda x: {
    "sentiment_result": x["sentiment_result"],
    "rating": x["passthrough"]["rating"],
    "review": x["passthrough"]["review"],
})

# 4) BRANCH CHAIN


branch_chain = RunnableBranch(
    # If model classified as positive → use positive prompt chain
    (lambda x: x["sentiment_result"].sentiment == "positive",
        positive_prompt | llm | outputs_parser),

    # If model classified as negative → use negative prompt chain
    (lambda x: x["sentiment_result"].sentiment == "negative",
        negative_prompt | llm | outputs_parser),
    RunnableLambda(lambda x: print(f"Error: Unexpected sentiment '{x['sentiment_result'].sentiment}'"))
)

# Combine: classifier → branch
full_chain = classifier_with_passthrough | branch_chain


# 5) MAIN ENTRYPOINT FOR FLASK


def get_ai_outputs(rating: int, review: str) -> dict:

    outputs: FeedbackAIOutputs = full_chain.invoke({
        "rating": rating,     # for branch prompts
        "review": review,     # for branch prompts
    })

    return {
        "user_response": outputs.user_response.strip(),
        "summary": outputs.summary.strip(),
        "actions": outputs.actions.strip(),
    }
