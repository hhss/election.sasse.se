"""Generator for SASSE election candidates."""
import os.path
import logging
from pelican.contents import Page, is_valid_content
from pelican.generators import Generator
from pelican.readers import read_file
from pelican import signals

logger = logging.getLogger(__name__)

class Candidate(Page):
    """Represents a single candidate. Title should be candidate's name."""
    mandatory_properties = ('title', 'registration', 'position')
    default_template = "candidate"

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
        self.candidates = {}
        super(CandidateGenerator, self).__init__(*args, **kwargs)

    def generate_context(self):
        candidates_path = os.path.normpath(
            os.path.join(self.path, 'candidates')
        )

        for f in self.get_files(candidates_path):
            try:
                content, metadata = read_file(f, settings=self.settings)
            except Exception, e:
                logger.warning(u"Could not process candidate {}\n{}".format(os.path.basename(f), e))
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

    def generate_output(self, writer):
        for position, candidates in self.candidates.items():
            if position in CandidateGenerator.LISTING_CANDIDATES:
                # TODO Create listing here
                continue

            for candidate in candidates:
                output_path = os.path.join('candidates', candidate.position, "{}.html".format(candidate.slug))
                writer.write_file(output_path, self.get_template('page'), self.context, page=candidate)

def get_generators(pelican):
    return [CandidateGenerator]

def register():
    signals.get_generators.connect(get_generators)
