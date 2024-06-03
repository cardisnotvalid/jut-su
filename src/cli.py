import questionary
from questionary import Choice

from .formatter import Search, Series, Video


class Question:
    try:
        def ask(self):
            pass
    except Exception as err:
        raise NotImplementedError(err)


class TextQuestion(Question):
    _QUESTION = ""

    def ask(self):
        answer = questionary.text(self._QUESTION).ask()
        return answer


class SelectQuestion(Question):
    _QUESTION = ""

    def __init__(self, choices):
        self.choices = choices

    def ask(self):
        answer = questionary.select(self._QUESTION, self.choices).ask()
        return answer


class SearchQuestion(TextQuestion):
    _QUESTION = "Поиск:"


class AnimeQuestion(SelectQuestion):
    _QUESTION = "Выберите аниме:"


class SeasonQusetion(SelectQuestion):
    _QUESTION = "Выберите сезон:"


class EpisodeQuestion(SelectQuestion):
    _QUESTION = "Выберите эпизод:"


class VideoQuestion(SelectQuestion):
    _QUESTION = "Выберите качество:"


class ChoiceBuilder:
    def anime_choices(self, data: list[Search]):
        result = []
        for item in data:
            choice = Choice(item.name, item.url)
            result.append(choice)
        return result

    def season_choices(self, data: dict[str, list[Series]]):
        result = []
        for season, series in data.items():
            choice = Choice(season, series)
            result.append(choice)
        return result

    def episode_choices(self, data: list[Series]):
        result = []
        for series in data:
            choice = Choice(series.id, series.url)
            result.append(choice)
        return result

    def video_choices(self, data: list[Video]):
        result = []
        for video in data:
            choice = Choice(video.label, video.source)
            result.append(choice)
        return result


class Questioner:
    def __init__(self):
        self.choice_builder = ChoiceBuilder()

    def _ask(self, questioner):
        return questioner.ask()

    def search_question(self):
        return self._ask(SearchQuestion())

    def anime_question(self, choices):
        choices = self.choice_builder.anime_choices(choices)
        return self._ask(AnimeQuestion(choices))

    def season_question(self, choices):
        choices = self.choice_builder.season_choices(choices)
        return self._ask(SeasonQusetion(choices))

    def episode_question(self, choices):
        choices = self.choice_builder.episode_choices(choices)
        return self._ask(EpisodeQuestion(choices))

    def video_question(self, choices):
        choices = self.choice_builder.video_choices(choices)
        return self._ask(VideoQuestion(choices))

