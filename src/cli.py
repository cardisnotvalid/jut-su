import questionary
from questionary import Choice

from .formatter import Search, Series, Video


class Question:
    def ask(self):
        try:
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


class ActionQuestion(SelectQuestion):
    _QUESTION = "Выберите действие:"


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

    def print(self, text):
        questionary.print(text)

    def action_question(self, choices):
        return self._ask(ActionQuestion(choices))

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


def start_questions(jutsu):
    questioner = Questioner()

    while True:
        search_target = questioner.search_question()
        if search_target == "q":
            exit(0)
        elif not search_target:
            questioner.print("Вы ничего не ввели")
            action = questioner.action_question(["Поиск", "Выйти"])
            if action == "Выйти":
                exit(0)
        else:
            break

    searched_list = jutsu.search_anime(search_target)
    anime_url = questioner.anime_question(searched_list)
    episodes = jutsu.get_anime_episodes(anime_url)
    season = questioner.season_question(episodes)
    episode_url = questioner.episode_question(season)
    videos = jutsu.get_episode_videos(episode_url)
    return questioner.video_question(videos)
