'''
Provides word game-related tools, and can be configured with custom settings, letter scores, and wordlists.
'''

import contextlib, copy, json, os, pathlib, sys, typing

wordlist_full = list(
	json.loads(
		pathlib.Path(
			os.path.join(os.path.dirname(__file__), 'wordlist.json')
		).read_text()
	)
)

kwargs = [
	('all_lowercase', bool, False, None, 'Whether output should be lowercase'),
	('allow_repeats', bool, False, None, 'Whether letters are allowed to repeat'),
	('display_debug', bool, False, None, 'Whether to display debug information'),
	('exclude_words', str, [], '*', 'Words to exclude'),
	('ignore_scores', bool, False, None, 'Whether to ignore scores'),
	('include_words', str, [], '*', 'Words to include'),
	('letter_scores', str, 'quarrel', None, 'Scoring system to use'),
	('max_words_len', int, None, None, 'Maximum length of words'),
	('min_words_len', int, 2, None, 'Minimum length of words'),
]

def build_letter_scores(
	name: typing.Optional[str] = None,
) -> typing.Dict[str, int]:
	'''
	Returns the letter scores for the given name. To be passsed into the `Ruleset` class.

	Args:
		`name: Optional[str]`: The name of the letter scoring system. Defaults to *Quarrel*, and returns an empty dictionary if invalid.

	Returns:
		A dictionary of letter scores, with letters as keys and scores as values.
	'''

	if not name:
		name = 'quarrel'

	return next(
		(
			val for key, val in {
				'quarrel': {
					'a': 1, 'b': 5, 'c': 2, 'd': 3, 'e': 1, 'f': 5, 'g': 4,
					'h': 4, 'i': 1, 'j': 15, 'k': 6, 'l': 2, 'm': 4, 'n': 1,
					'o': 1, 'p': 3, 'q': 15, 'r': 2, 's': 1, 't': 1, 'u': 3,
					'v': 6, 'w': 5, 'x': 10, 'y': 5, 'z': 12
				},
				'scrabble': {
					'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
					'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
					'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1,
					'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
				},
			}.items() if name == key
		), {}
	)

def build_query(
	query: str,
	repeat_letters: bool = True,
) -> str:
	'''
	Returns a sorted query string, with optional repeats.

	Args:
		`query: str`: Query string to sort.
		`repeat_letters: bool = True`: Whether to allow repeating letters in the query string.

	Returns:
		The inputted query string, but sorted.
	'''

	return ''.join(
		sorted(query)
		if repeat_letters
		else sorted(list(set(dict.fromkeys(query))))
	).lower()

def build_settings(
	user_settings: typing.Optional[typing.Dict[str, typing.Any]] = None,
	wordlist: typing.Optional[typing.List[str]] = None,
):
	'''
	Returns the settings for the given user settings. To be passsed into the `Ruleset` class.

	Args:
		`user_settings: Optional[dict[str, Any]]`: Custom settings to override the default settings. Defaults to an empty dictionary.
		`wordlist: Optional[list[str]]`: Wordlist used to determine defaults for word-related settings.

	Returns:
		A dictionary of settings.
	'''

	if not user_settings:
		user_settings = {}

	if not wordlist:
		wordlist = wordlist_full

	if 'exclude_words' in user_settings:
		for word in user_settings['exclude_words']:
			if (word) and (word in wordlist):
				wordlist.remove(word)

	if 'include_words' in user_settings:
		for word in user_settings['include_words']:
			if (word) and (word not in wordlist):
				wordlist.append(word)

	settings = {
		**{
			arg: default for arg, _, default, _, _ in kwargs
		}, **user_settings
	}

	settings = {
		**settings, **{
			'max_words_len': min(
				settings['max_words_len'], max(len(word) for word in wordlist)
			),
			'min_words_len': max(
				settings['min_words_len'], 2
			),
		}
	}

	settings = {
		**settings, **{
			'letter_scores': settings['letter_scores']
				if build_letter_scores(settings['letter_scores'])
				else 'quarrel'
		}
	}

	return settings

class Ruleset:
	def __init__(
		self,
		settings: typing.Optional[typing.Dict[str, typing.Any]] = None,
		wordlist: typing.Optional[typing.List[str]] = None,
	) -> None:
		'''
		Defines a word game ruleset with the given settings and wordlist.

		Args:
			`settings: Optional[dict[str, Any]]`: Custom settings to override the default settings. Defaults to an empty dictionary. Should be an output from `build_settings()`.
			`wordlist: Optional[list[str]]`: A list of words to be used in the ruleset. Defaults to the full Scrabble wordlist.

		Returns:
			A `Ruleset` with the specified settings and wordlist.
		'''

		if settings is None:
			settings = {}

		if not wordlist:
			wordlist = wordlist_full

		if 'exclude_words' in settings:
			for word in settings['exclude_words']:
				if (word) and (word in wordlist):
					wordlist.remove(word)

		if 'include_words' in settings:
			for word in settings['include_words']:
				if (word) and (word not in wordlist):
					wordlist.append(word)

		settings = build_settings(settings, wordlist)

		try:
			with open(settings['custom_dictionary'], 'r') as f:
				wordlist = f.read().splitlines()
		except (FileNotFoundError, KeyError):
			wordlist = wordlist_full

		wordlist = [
			word for word in wordlist if settings['min_words_len'] <= len(word) <= settings['max_words_len']
		]

		self.settings = settings
		self.scores = {
			word: sum(build_letter_scores(self['letter_scores'])[char] for char in word) for word in sorted(
				sorted(wordlist),
				key=lambda word: (
					len(word), sum(build_letter_scores(self['letter_scores'])[char] for char in word)
				), reverse=True
			)
		}
		self.wordlist = wordlist

	def __getitem__(self, key: str) -> typing.Any:
		'''
		Returns the value of the given setting, as defined in the ruleset's settings.

		Args:
			`key: str`: The setting to get the value of.

		Returns:
			The value of the given setting.
		'''

		if key in self.settings.keys():
			return self.settings[key]
		else:
			raise KeyError(f'{key} not found in settings')

	def get_settings(
		self,
	) -> typing.Dict[str, typing.Any]:
		'''
		Returns the current settings.
		'''

		return self.settings

	def get_settings_str(
		self,
	) -> str:
		'''
		Returns the current settings as a JSON string, formatted with tabs.
		'''

		return json.dumps(self.settings, indent=2, sort_keys=True).replace('  ', '\t') + '\n'

	def solve(
		self,
		query: str,
	) -> typing.Tuple[typing.Dict[int, typing.List[typing.Union[typing.List[str], str]]], bool]:
		'''
		Finds all possible words that can be formed from the given query string, using the set wordlist.

		Args:
			`query: str`: A string representing the query to be solved.

		Returns:
			A tuple containing a dictionary of best words by length, and a boolean indicating whether an anagram was found.
		'''

		query = build_query(query, not self['allow_repeats'])

		scores_out = {}

		if self['display_debug']:
			print('')

		for len_iter in range(
			2, (self['max_words_len'] if self['allow_repeats'] else len(query)) + 1
		)[::-1]:
			scores_out = {
				**scores_out, **{
					len_iter: [[], 0]
				}
			}

			for word in self.scores:
				query_iter, word_iter = copy.deepcopy(query), copy.deepcopy(word)
				word_fits = False

				if (
					len(word) == len_iter if self['ignore_scores'] else len(word) <= len_iter
				) and set(word) <= set(query):
					if not self['ignore_scores'] and self.scores[word] < scores_out[len_iter][1]:
						continue

					if self['allow_repeats']:
						word_fits = all(char in query for char in word)

					else:
						for char in word:
							query_iter = query_iter.replace(char, ' ', 1)
							word_iter = word_iter.replace(char, ' ', 1)

							if self['display_debug']:
								print(f'input: {[query_iter]} | {[word]}: {[word_iter]}')

						if query_iter.count(' ') == word_iter.count(' ') != 0:
							word_fits = True

					if self['display_debug']:
						print(f'{[word]} fits for {[len_iter]}')

				if word_fits:
					scores_out[len_iter][0].append(word)

					if not self['ignore_scores']:
						scores_out[len_iter][1] = self.scores[scores_out[len_iter][0][0]]

			if self['display_debug']:
				print(f' - output for {[len_iter]}: {scores_out[len_iter][0]}')

		try:
			anagram_found = len(scores_out[len(query)][0][0]) == len(query)
		except (IndexError, KeyError):
			anagram_found = False

		for key, val in copy.deepcopy(scores_out).items():
			with contextlib.suppress(IndexError, KeyError):
				if not val:
					del scores_out[key]
					if self['display_debug']:
						print(f' - removed {[key]} for empty list')
				elif not self['ignore_scores'] and any(
					word in scores_out[key][0] for word in scores_out[key-1][0]
				):
					del scores_out[key]
					if self['display_debug']:
						print(f' - removed {[key]} for duplicate/s')

		return scores_out, anagram_found

	def solve_str(
		self,
		query: str
	):
		'''
		Finds all possible words that can be formed from the given query string, using the set wordlist.

		Args:
			`query: str`: A string representing the query to be solved.

		Returns:
			A string representing the output of the solver.
		'''

		query = build_query(query, not self['allow_repeats'])

		scores_out, anagram_found = self.solve(query)

		anagram_found = '' if anagram_found else '  \t warning: anagram not found\n\n'

		return str(
			f'\n  \t--- query: {query} ({len(query)} letters'
			+ (' + repeats' if self['allow_repeats'] else '') + ') ---\n\n' + (
				(
					anagram_found + '\n\n'.join(
						f'\t{key} letters'
						+ (
							''
							if self['ignore_scores']
							else f' - {scores_out[key][1]} points'
						) + '\n\t ' + ', '.join(
							sorted(
								word.lower() if self['all_lowercase'] else word.upper()
								for word in scores_out[key][0]
							)
						)
						for key in scores_out.keys()
						if scores_out[key][0]
					)
				)
				if any(scores_out[key][0] for key in scores_out.keys())
				else '\t no words found'
			)
		)

	def get_wordlist(
		self,
	) -> typing.List[str]:
		'''
		Returns the current wordlist, as defined in the ruleset settings.
		'''

		return self.wordlist
