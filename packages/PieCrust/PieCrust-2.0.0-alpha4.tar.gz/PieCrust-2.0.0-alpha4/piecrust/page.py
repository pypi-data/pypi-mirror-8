import re
import sys
import json
import codecs
import os.path
import hashlib
import logging
import datetime
import dateutil.parser
import collections
from werkzeug.utils import cached_property
from piecrust.configuration import (Configuration, ConfigurationError,
        parse_config_header)


logger = logging.getLogger(__name__)


class PageConfiguration(Configuration):
    def __init__(self, values=None, validate=True):
        super(PageConfiguration, self).__init__(values, validate)

    def _validateAll(self, values):
        values.setdefault('title', 'Untitled Page')
        values.setdefault('content_type', 'html')
        ppp = values.get('posts_per_page')
        if ppp is not None:
            values.setdefault('items_per_page', ppp)
        pf = values.get('posts_filters')
        if pf is not None:
            values.setdefault('items_filters', pf)
        return values


FLAG_NONE = 0
FLAG_RAW_CACHE_VALID = 2**0


class Page(object):
    def __init__(self, source, source_metadata, rel_path):
        self.source = source
        self.source_metadata = source_metadata
        self.rel_path = rel_path
        self._config = None
        self._raw_content = None
        self._flags = FLAG_NONE
        self._datetime = None

    @property
    def app(self):
        return self.source.app

    @property
    def ref_spec(self):
        return '%s:%s' % (self.source.name, self.rel_path)

    @cached_property
    def path(self):
        return self.source.resolveRef(self.rel_path)

    @cached_property
    def path_mtime(self):
        return os.path.getmtime(self.path)

    @property
    def flags(self):
        return self._flags

    @property
    def config(self):
        self._load()
        return self._config

    @property
    def raw_content(self):
        self._load()
        return self._raw_content

    @property
    def datetime(self):
        if self._datetime is None:
            if 'datetime' in self.source_metadata:
                self._datetime = self.source_metadata['datetime']
            elif 'date' in self.source_metadata:
                page_date = self.source_metadata['date']
                page_time = self.config.get('time')
                if page_time is not None:
                    if isinstance(page_time, str):
                        # Need to parse it...
                        try:
                            parsed_t = dateutil.parser.parse(page_time)
                        except Exception as ex:
                            raise ConfigurationError(
                                    "Invalid time '%s' in page: %s" %
                                    (page_time, self.path)) from ex
                        page_time = datetime.time(parsed_t.hour,
                                parsed_t.minute, parsed_t.second)

                    elif isinstance(page_time, int):
                        # Total seconds... convert to a time struct.
                        delta = datetime.timedelta(seconds=page_time)
                        dummy = datetime.datetime(1970, 1, 1)
                        dummy += delta
                        page_time = dummy.time()

                    try:
                        self._datetime = datetime.datetime.combine(
                                page_date, page_time)
                    except Exception as ex:
                        raise ConfigurationError(
                                "Invalid page time '%s' for: %s" % (
                                    page_time, self.path)) from ex
                else:
                    self._datetime = datetime.datetime(
                            page_date.year, page_date.month, page_date.day)
            else:
                self._datetime = datetime.datetime.fromtimestamp(
                        self.path_mtime)
                if self._datetime is None:
                    raise Exception("Got null datetime from path! %s" % self.path)
        return self._datetime

    @datetime.setter
    def datetime(self, value):
        self._datetime = value

    def getSegment(self, name='content'):
        return self.raw_content[name]

    def _load(self):
        if self._config is not None:
            return

        config, content, was_cache_valid = load_page(self.app, self.path,
                                                     self.path_mtime)
        self._config = config
        self._raw_content = content
        if was_cache_valid:
            self._flags |= FLAG_RAW_CACHE_VALID


class PageLoadingError(Exception):
    def __init__(self, path, inner=None):
        super(PageLoadingError, self).__init__(
                "Error loading page: %s" % path,
                inner)


class ContentSegment(object):
    debug_render_func = 'debug_render'

    def __init__(self, content=None, fmt=None):
        self.parts = []
        if content is not None:
            self.parts.append(ContentSegmentPart(content, fmt))

    def debug_render(self):
        return '\n'.join([p.content for p in self.parts])


class ContentSegmentPart(object):
    def __init__(self, content, fmt=None, line=-1):
        self.content = content
        self.fmt = fmt
        self.line = line

    def __str__(self):
        return '%s [%s]' % (self.content, self.fmt or '<default>')


def json_load_segments(data):
    segments = {}
    for key, seg_data in data.items():
        seg = ContentSegment()
        for p_data in seg_data:
            part = ContentSegmentPart(p_data['c'], p_data['f'], p_data['l'])
            seg.parts.append(part)
        segments[key] = seg
    return segments


def json_save_segments(segments):
    data = {}
    for key, seg in segments.items():
        seg_data = []
        for part in seg.parts:
            p_data = {'c': part.content, 'f': part.fmt, 'l': part.line}
            seg_data.append(p_data)
        data[key] = seg_data
    return data


def load_page(app, path, path_mtime=None):
    try:
        return _do_load_page(app, path, path_mtime)
    except Exception as e:
        logger.exception("Error loading page: %s" %
                os.path.relpath(path, app.root_dir))
        _, __, traceback = sys.exc_info()
        raise PageLoadingError(path, e).with_traceback(traceback)


def _do_load_page(app, path, path_mtime):
    # Check the cache first.
    cache = app.cache.getCache('pages')
    cache_path = "%s.json" % hashlib.md5(path.encode('utf8')).hexdigest()
    page_time = path_mtime or os.path.getmtime(path)
    if cache.isValid(cache_path, page_time):
        cache_data = json.loads(cache.read(cache_path),
                object_pairs_hook=collections.OrderedDict)
        config = PageConfiguration(values=cache_data['config'],
                validate=False)
        content = json_load_segments(cache_data['content'])
        return config, content, True

    # Nope, load the page from the source file.
    logger.debug("Loading page configuration from: %s" % path)
    with codecs.open(path, 'r', 'utf-8') as fp:
        raw = fp.read()
    header, offset = parse_config_header(raw)

    if not 'format' in header:
        auto_formats = app.config.get('site/auto_formats')
        name, ext = os.path.splitext(path)
        header['format'] = auto_formats.get(ext, None)

    config = PageConfiguration(header)
    content = parse_segments(raw, offset)
    config.set('segments', list(content.keys()))

    # Save to the cache.
    cache_data = {
            'config': config.get(),
            'content': json_save_segments(content)}
    cache.write(cache_path, json.dumps(cache_data))

    return config, content, False


segment_pattern = re.compile(
        r"""^\-\-\-\s*(?P<name>\w+)(\:(?P<fmt>\w+))?\s*\-\-\-\s*$""",
        re.M)
part_pattern = re.compile(
        r"""^<\-\-\s*(?P<fmt>\w+)\s*\-\->\s*$""",
        re.M)


def parse_segments(raw, offset=0):
    matches = list(segment_pattern.finditer(raw, offset))
    num_matches = len(matches)
    if num_matches > 0:
        contents = {}

        first_offset = matches[0].start()
        if first_offset > 0:
            # There's some default content segment at the beginning.
            seg = ContentSegment()
            seg.parts = parse_segment_parts(raw, offset, first_offset)
            contents['content'] = seg

        for i in range(1, num_matches):
            m1 = matches[i - 1]
            m2 = matches[i]
            seg = ContentSegment()
            seg.parts = parse_segment_parts(raw, m1.end() + 1,
                    m2.start(), m1.group('fmt'))
            contents[m1.group('name')] = seg

        # Handle text past the last match.
        lastm = matches[-1]
        seg = ContentSegment()
        seg.parts = parse_segment_parts(raw, lastm.end() + 1,
                len(raw), lastm.group('fmt'))
        contents[lastm.group('name')] = seg

        return contents
    else:
        # No segments, just content.
        seg = ContentSegment()
        seg.parts = parse_segment_parts(raw, offset, len(raw))
        return {'content': seg}


def parse_segment_parts(raw, start, end, first_part_fmt=None):
    matches = list(part_pattern.finditer(raw, start, end))
    num_matches = len(matches)
    if num_matches > 0:
        parts = []

        # First part, before the first format change.
        parts.append(
                ContentSegmentPart(raw[start:matches[0].start()],
                    first_part_fmt,
                    start))

        for i in range(1, num_matches):
            m1 = matches[i - 1]
            m2 = matches[i]
            parts.append(
                    ContentSegmentPart(
                        raw[m1.end() + 1:m2.start()],
                        m1.group('fmt'),
                        m1.end() + 1))

        lastm = matches[-1]
        parts.append(ContentSegmentPart(raw[lastm.end() + 1:end],
                lastm.group('fmt'),
                lastm.end() + 1))

        return parts
    else:
        return [ContentSegmentPart(raw[start:end], first_part_fmt)]

