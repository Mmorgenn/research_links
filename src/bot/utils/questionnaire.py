class Questionnaire:
    def __init__(self, questionnaire_data: dict) -> None:
        self.q_data = questionnaire_data

    def show(self, title: str = "🔎 Профиль пользователя") -> str:
        questionnaire = (
            "<b>{}:</b>\n"
            f"<b>📖 Имя:</b> {self.q_data["name"]}\n"
            f"<b>❤️ Пол:</b> {self.q_data["gender"]}\n"
            f"<b>🎂 Возраст:</b> {self.q_data["age"]}\n"
            f"<b>📜 Статус:</b> {self.q_data["status"]}\n"
            f"<b>📒 Научная область:</b> {self.q_data["area"]}\n"
            f"<b>📝 О работе:</b>\n"
            f"{f"<b>📊 Компания:</b> {self.q_data["company"]}\n" if self.q_data.get("company", None) else ""}"
            f"{f"<b>💻 Любимый язык:</b> {self.q_data["language"]}\n" if self.q_data.get("language", None) else ""}"
            f"{f"<b>📈 Индекс h:</b> {self.q_data["hindex"]}\n" if self.q_data.get("hindex", None) else ""}"
            f"{f"<b>📋 Индекс i10:</b> {self.q_data["i10index"]}\n" if self.q_data.get("i10index", None) else ""}"
            f"{f"<b>🗄 Организация:</b> {self.q_data["organization"]}\n" if self.q_data.get("organization", None) else ""}"
            f"{f"<b>🔎 Популярный репозиторий:</b> {self.q_data["popular_repos"]}\n" if self.q_data.get("popular_repos", None) else ""}"
            f"{f"<b>💽 Популярная статья:</b> {self.q_data["most_cited"]}\n" if self.q_data.get("most_cited", None) else ""}"
            f"{self.q_data["info"]}"
        ).format(title)
        return questionnaire
