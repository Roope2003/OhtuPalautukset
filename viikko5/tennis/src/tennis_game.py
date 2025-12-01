class TennisGame:
    _SCORE_NAMES = {
        0: "Love",
        1: "Fifteen",
        2: "Thirty",
        3: "Forty"
    }
    _EQUAL_SCORES = {
        0: "Love-All",
        1: "Fifteen-All",
        2: "Thirty-All",
    }
    _DEUCE = "Deuce"
    _ADVANTAGE_PLAYER1 = "Advantage player1"
    _ADVANTAGE_PLAYER2 = "Advantage player2"
    _WIN_PLAYER1 = "Win for player1"
    _WIN_PLAYER2 = "Win for player2"

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.m_score1 += 1
        elif player_name == self.player2_name:
            self.m_score2 += 1
        else:
            pass

    def _score_to_string(self, score_value):
        """Converts a numeric score to its string representation."""
        return self._SCORE_NAMES.get(score_value, "")

    def _get_equal_score(self):
        """Returns the score string when both players have equal points."""
        if self.m_score1 < 3:
            return self._EQUAL_SCORES[self.m_score1]
        return self._DEUCE

    def _get_advantage_or_win_score(self):
        """Returns the score string when one player has 4 or more points."""
        score_difference = self.m_score1 - self.m_score2
        if score_difference == 1:
            return self._ADVANTAGE_PLAYER1
        elif score_difference == -1:
            return self._ADVANTAGE_PLAYER2
        elif score_difference >= 2:
            return self._WIN_PLAYER1
        else:
            return self._WIN_PLAYER2

    def _get_regular_score(self):
        """Returns the score string for regular game progression (not equal, not advantage/win)."""
        score_str1 = self._score_to_string(self.m_score1)
        score_str2 = self._score_to_string(self.m_score2)
        return f"{score_str1}-{score_str2}"

    def get_score(self):
        if self.m_score1 == self.m_score2:
            score = self._get_equal_score()
        elif self.m_score1 >= 4 or self.m_score2 >= 4:
            score = self._get_advantage_or_win_score()
        else:
            score = self._get_regular_score()

        return score
