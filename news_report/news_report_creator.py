from pathlib import Path

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from news_report.scraper.news_scraper import scrape_omni
from news_report.scraper.scraper_constants import TMP_DIR, GPT_MODEL_NAME
from news_report.email_sender import EmailSender
from news_report.news_report_models import NewsReportOutput

class NewsReportCreator:
    def __init__(self):
        Path(TMP_DIR).mkdir(parents=True, exist_ok=True)
        self.news_file_path = f"{TMP_DIR}/top_news.txt"
        self.model = ChatOpenAI(model=GPT_MODEL_NAME, temperature=0)
        self.email_sender = EmailSender()

    def _load_news_file_content(self) -> str:
        with open(self.news_file_path, "r") as f:
            content = f.read()
        return content

    def scrape_news_and_generate_article_and_send_email(self, recipient_emails: list[str]):
        scrape_omni(self.news_file_path)
        news_content: str = self._load_news_file_content()
        news_report: NewsReportOutput = self.get_article_from_scraped_news(news_content)
        email_content = self.email_sender.pretty_print_news_report(news_report)
        for recipient_email in recipient_emails:
            self.email_sender.send_email(recipient_email=recipient_email, subject="Your Daily Newsletter in German", body=email_content)

    def get_article_from_scraped_news(self, news_content: str) -> NewsReportOutput:

        query = f"""
        I am a Swede trying to learn German, so I want to read some news in German. Here I have scraped the top news from omni.se, could you collect the most insightful news, try to focus on the concrete event that has happened rather that new takes on old subjects. Create 4 short, diverse news articles based on the top news from Omni and write them in beginner level German. Based on the 4 articles you wrote, chose 10 words that will help me understand the context of the articles and provide their swedish translation, these are the Daily words, consider the fact that some German and Swedish words are very similar and avoid translating words that are very similar in the two languages as those are easy to understand either way. I also want to to provide a short preamble summarising shortly what the 4 articles are about.  

        --------------OMNI TOP NEWS--------------
        {news_content}
        -----------------------------------------
        """
        parser = JsonOutputParser(pydantic_object=NewsReportOutput)
        prompt = PromptTemplate(
            template="Answer the user query.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.model | parser
        result = chain.invoke(query)
        return NewsReportOutput(**result)


