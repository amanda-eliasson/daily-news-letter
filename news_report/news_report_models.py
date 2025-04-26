from pydantic import BaseModel, Field


class ShortArticle(BaseModel):
    title: str = Field(default="")
    text: str = Field(default="")


class DailyWord(BaseModel):
    word: str = Field(default="")
    translation: str = Field(default="")


class NewsReportOutput(BaseModel):
    preamble: str = Field(
        default="", description="a short summary of the four articles"
    )
    articles: list[ShortArticle] = Field(
        default="", description="4 articles on different topics"
    )
    daily_words: list[DailyWord] = Field(
        default="",
        description="List of words that are helpful to understand the article",
    )
