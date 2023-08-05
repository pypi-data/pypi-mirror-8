import time
import datetime
from collections import namedtuple

import pmxbot
from pmxbot import storage
from pmxbot.core import command

ALIASES = ('gl', )
HELP_DEFINE_STR = '!{} define <entry>: <definition>'.format(ALIASES[0])
HELP_QUERY_STR = '!{} <entry> [<num>]'.format(ALIASES[0])

DOCS_STR = (
    'To define an entry: `{}`. '
    'To get a definition: `{}`. '
    'Pass in an integer >= 1 to get a definition from the history. '
    'Get a random definition by omitting the entry argument.'
).format(HELP_DEFINE_STR, HELP_QUERY_STR)

OOPS_STR = 'One of us screwed this up. Hopefully you. ' + DOCS_STR


class Glossary(storage.SelectableStorage):
    @classmethod
    def initialize(cls):
        cls.store = cls.from_URI(pmxbot.config.database)
        cls._finalizers.append(cls.finalize)

    @classmethod
    def finalize(cls):
        del cls.store


class SQLiteGlossary(Glossary, storage.SQLiteStorage):
    CREATE_GLOSSARY_SQL = """
      CREATE TABLE IF NOT EXISTS glossary (
       entryid INTEGER NOT NULL,
       entry VARCHAR NOT NULL,
       definition TEXT NOT NULL,
       author VARCHAR NOT NULL,
       timestamp INTEGER NOT NULL,
       PRIMARY KEY (entryid)
    )
    """

    CREATE_GLOSSARY_INDEX_SQL = """
      CREATE INDEX IF NOT EXISTS ix_glossary_entry ON glossary(entry)
    """

    def init_tables(self):
        self.db.execute(self.CREATE_GLOSSARY_SQL)
        self.db.execute(self.CREATE_GLOSSARY_INDEX_SQL)
        self.db.commit()

    def add_entry(self, entry, definition, author):
        entry = entry.lower()

        sql = """
          INSERT INTO glossary (entry, definition, author, timestamp)
          VALUES (?, ?, ?, ?)
        """

        timestamp = int(time.mktime(datetime.datetime.now().utctimetuple()))

        self.db.execute(sql, (entry, definition, author, timestamp))
        self.db.commit()

        return self.get_entry_data(entry)

    def get_random_entry(self):
        sql = """
          SELECT entry FROM glossary
          WHERE entryid = (
            abs(random()) % (SELECT max(rowid) + 1 FROM glossary)
        );
        """

        result = self.db.execute(sql).fetchone()

        if not result:
            return None

        return result[0]

    def get_entry_data(self, entry, num=None):
        entry = entry.lower()

        sql = """
            SELECT entry, definition, author, timestamp
            FROM glossary
            WHERE entry LIKE ?
            ORDER BY timestamp
        """

        results = self.db.execute(sql, (entry, )).fetchall()

        if results:
            total_count = len(results)

            if num:
                index = num - 1
            else:
                index = total_count - 1

            target = results[index]

            return GlossaryQueryResult(
                target[0],
                target[1],
                target[2],
                datetime.datetime.fromtimestamp(float(target[-1])),
                index,
                total_count
            )

        return None


GlossaryQueryResult = namedtuple(
    'GlossaryQueryResult', 'entry definition author datetime index total_count'
)


def datetime_to_age_str(dt):
    """
    Return a human-readable age given a datetime object.
    """
    days = (datetime.datetime.utcnow() - dt).days

    if days > 365:
        age_str = '{0:.1f} years ago'.format(days / 365.0)
    elif days > 30:
        age_str = '{0:.1f} months ago'.format(days / 30.5)
    elif days == 0:
        age_str = 'today'
    else:
        age_str = '{} days ago'.format(days)

    return age_str


def handle_random_query():
    """
    Returns a formatted result string for a random entry.

    Uses the latest definition of the entry.
    """
    entry = Glossary.store.get_random_entry()

    if not entry:
        return "I can't find a single definition. " + DOCS_STR

    return handle_nth_definition(entry)


def handle_nth_definition(entry, num=None):
    """
    Return a formatted result string for an entry.

    If ``num`` is passed, it will return the corresponding numbered, historical
    definition for the entry.
    """
    if num:
        try:
            num = int(num)
        except (ValueError, TypeError):
            return OOPS_STR

        if not num > 0:
            return OOPS_STR

    try:
        query_result = Glossary.store.get_entry_data(entry, num)
    except IndexError:
        return OOPS_STR

    if query_result:
        return u'{} ({}/{}): {} [by {}, {}]'.format(
            query_result.entry,
            query_result.index + 1,
            query_result.total_count,
            query_result.definition,
            query_result.author,
            datetime_to_age_str(query_result.datetime)
        )

    return u'"{}" is undefined. {}'.format(entry, DOCS_STR)


def handle_definition_add(nick, rest):
    """
    Attempt to save a new definition.
    """
    if not ':' in rest:
        return OOPS_STR

    parts = rest.split(':', 1)

    if len(parts) != 2:
        return OOPS_STR

    entry = parts[0].split()[-1].strip()

    definition = parts[1].strip()

    existing = Glossary.store.get_entry_data(entry)

    if existing and existing.definition == definition:
        return "That's already the current definition."

    result = Glossary.store.add_entry(entry, definition, author=nick)

    return u'Okay! "{}" is now "{}"'.format(result.entry, result.definition)



@command('glossary', aliases=ALIASES, doc=DOCS_STR)
def quote(client, event, channel, nick, rest):
    """
    Glossary command. Handles all command versions.

    Assumes `rest` is a unicode object.
    """
    rest = rest.strip()

    if rest.startswith('define'):
        return handle_definition_add(nick, rest)

    parts = rest.strip().split()

    if not parts:
        return handle_random_query()

    entry = parts[0]

    if len(parts) == 2:
        return handle_nth_definition(entry, parts[1])
    elif len(parts) > 2:
        return OOPS_STR
    else:
        return handle_nth_definition(entry)
