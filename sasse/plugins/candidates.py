"""Generator for SASSE election candidates."""
import os.path
import collections
import logging
from pelican.contents import Page, is_valid_content
from pelican.generators import Generator
from pelican.readers import read_file
from pelican import signals

logger = logging.getLogger(__name__)

class Candidate(Page):
    POSITIONS = collections.OrderedDict([
        ('president', u"President"),
        ('vice-president', u"Vice President"),
        ('treasurer', u"Treasurer"),
        ('idu', u'President of the Sports Committee'),
        ('intu', u'President of the International Committee'),
        ('itu', u'President of the IT Committee'),
        ('medu', u'President of the Media Committee'),
        ('nu', u'President of the Business Committee'),
        ('su', u'President of the Social Committee'),
        ('pu', u'President of the Entertainment Committee'),
        ('uu', u'President of the Education Committee'),
        ('fum', u"Student Council"),
        ('board-of-directors', u"Board of Directors"),
        ('speaker-of-the-council', u"Speaker of the Council"),
        ('equality-representative', u"Equality Representative"),
        ('safety-representative', u"Safety Representative"),
        ('internal-accountant', u"Internal Accountant")
    ])

    """Represents a single candidate. Title should be candidate's name."""
    mandatory_properties = ('title', 'registration', 'position')
    default_template = "candidate"

    def __init__(self, *args, **kwargs):
        super(Candidate, self).__init__(*args, **kwargs)

    @property
    def position_title(self):
        return Candidate.POSITIONS.get(self.position, self.position)

    @property
    def url(self):
        return u"candidates/{position}{hash_or_slash}{slug}".format(
            position=self.position,
            hash_or_slash="/" if self.position not in CandidateGenerator.LISTING_CANDIDATES else "#",
            slug=self.slug
        )

class CandidateGenerator(Generator):
    # Candidates for these positions don't get a personal candidate page,
    # but will only be listed on a common page.
    LISTING_CANDIDATES = [
        'fum',
        'board-of-directors',
        'speaker-of-the-council',
        'equality-representative',
        'safety-representative',
        'internal-accountant'
    ]

    def __init__(self, *args, **kwargs):
        self.candidates = collections.OrderedDict()
        for position in Candidate.POSITIONS.keys():
            self.candidates[position] = []

        super(CandidateGenerator, self).__init__(*args, **kwargs)

    def generate_context(self):
        candidates_path = os.path.normpath(
            os.path.join(self.path, 'candidates')
        )

        for f in self.get_files(candidates_path):
            try:
                content, metadata = read_file(f, settings=self.settings)
            except Exception, e:
                continue

            # Position is determined by directory
            position = os.path.basename(os.path.dirname(f)).decode('utf-8')
            metadata['position'] = position

            candidate = Candidate(content, metadata, settings=self.settings, filename=f)

            if not is_valid_content(candidate, f):
                continue

            if not self.candidates.has_key(position):
                self.candidates[position] = []

            self.candidates[position].append(candidate)

        self._update_context(('candidates',))
        self.context['POSITION_TITLES'] = Candidate.POSITIONS
        self.context['LISTING_CANDIDATES'] = CandidateGenerator.LISTING_CANDIDATES

    def generate_output(self, writer):
        for position, candidates in self.candidates.items():
            if position in CandidateGenerator.LISTING_CANDIDATES:
                # TODO Create listing here
                continue

            for candidate in candidates:
                output_path = os.path.join('candidates', candidate.position, candidate.slug, "index.html")
                writer.write_file(output_path, self.get_template('candidate-single'), self.context, candidate=candidate)

        self.generate_lists(writer)

    def generate_lists(self, writer):
        for position in Candidate.POSITIONS.keys():
            if position not in CandidateGenerator.LISTING_CANDIDATES:
                pass

            output_path = os.path.join('candidates', position, 'index.html')

            writer.write_file(output_path, self.get_template('candidates-position'), self.context,
                position=position,
                position_title=Candidate.POSITIONS[position],
                candidates=self.candidates[position]
            )

        # /candidates
        writer.write_file(
            os.path.join('candidates', 'index.html'),
            self.get_template('candidates'),
            self.context
        )

def get_generators(pelican):
    return [CandidateGenerator]

def register():
    signals.get_generators.connect(get_generators)
