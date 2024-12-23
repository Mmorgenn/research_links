from scholarly import scholarly
from scholarly.data_types import Author


class GooglePars:

    def __init__(self, user: str) -> None:
        self.user = user

    @staticmethod
    def get_most_cited(author: Author) -> str | None:
        most_cited_article = max(author['publications'], key=lambda pub: pub['num_citations'], default=None)
        if not most_cited_article:
            return None

        article = scholarly.fill(most_cited_article)
        return article["pub_url"]

    @staticmethod
    def get_organization(author: Author) -> str | None:
        affiliation = author.get('affiliation', None)
        return affiliation

    @staticmethod
    def get_hindex(author: Author) -> str | None:
        h = author.get("hindex", None)
        return h

    @staticmethod
    def get_i10(author: Author) -> str | None:
        i10 = author.get("i10index", None)
        return i10

    def get_info(self) -> dict[str, str | None] | None:
        search_query = scholarly.search_author(self.user)
        author = next(search_query, None)

        if not author:
            return None

        author = scholarly.fill(author)
        organization = self.get_organization(author)
        most_cited = self.get_most_cited(author)
        h = self.get_hindex(author)
        i10 = self.get_i10(author)

        return {
            "organization": organization,
            "most_cited": most_cited,
            "hindex": h,
            "i10index": i10
        }
