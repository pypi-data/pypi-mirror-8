import time
import os.path
import logging
import hashlib
import fnmatch
import datetime
from piecrust.baking.baker import Baker
from piecrust.baking.records import BakeRecord
from piecrust.chefutil import format_timed
from piecrust.commands.base import ChefCommand
from piecrust.processing.base import ProcessorPipeline


logger = logging.getLogger(__name__)


class BakeCommand(ChefCommand):
    def __init__(self):
        super(BakeCommand, self).__init__()
        self.name = 'bake'
        self.description = "Bakes your website into static HTML files."

    def setupParser(self, parser, app):
        parser.add_argument('-o', '--output',
                help="The directory to put all the baked HTML files into "
                     "(defaults to `_counter`)")
        parser.add_argument('-f', '--force',
                help="Force re-baking the entire website.",
                action='store_true')
        parser.add_argument('--portable',
                help="Uses relative paths for all URLs.",
                action='store_true')
        parser.add_argument('--no-assets',
                help="Don't process assets (only pages).",
                action='store_true')

    def run(self, ctx):
        if ctx.args.portable:
            # Disable pretty URLs because there's likely not going to be
            # a web server to handle serving default documents.
            ctx.app.config.set('site/pretty_urls', False)

        out_dir = (ctx.args.output or
                   os.path.join(ctx.app.root_dir, '_counter'))

        start_time = time.clock()
        try:
            # Bake the site sources.
            self._bakeSources(ctx, out_dir)

            # Bake the assets.
            if not ctx.args.no_assets:
                self._bakeAssets(ctx, out_dir)

            # All done.
            logger.info('-------------------------');
            logger.info(format_timed(start_time, 'done baking'));
            return 0
        except Exception as ex:
            if ctx.app.debug:
                logger.exception(ex)
            else:
                logger.error(str(ex))
            return 1

    def _bakeSources(self, ctx, out_dir):
        num_workers = ctx.app.config.get('baker/workers') or 4
        baker = Baker(
                ctx.app, out_dir,
                force=ctx.args.force,
                portable=ctx.args.portable,
                no_assets=ctx.args.no_assets,
                num_workers=num_workers)
        baker.bake()

    def _bakeAssets(self, ctx, out_dir):
        mounts = ctx.app.assets_dirs
        baker_params = ctx.app.config.get('baker') or {}
        skip_patterns = baker_params.get('skip_patterns')
        force_patterns = baker_params.get('force_patterns')
        num_workers = ctx.app.config.get('baker/workers') or 4
        proc = ProcessorPipeline(
                ctx.app, mounts, out_dir,
                force=ctx.args.force,
                skip_patterns=skip_patterns,
                force_patterns=force_patterns,
                num_workers=num_workers)
        proc.run()



class ShowRecordCommand(ChefCommand):
    def __init__(self):
        super(ShowRecordCommand, self).__init__()
        self.name = 'showrecord'
        self.description = "Shows the bake record for a given output directory."

    def setupParser(self, parser, app):
        parser.add_argument('-o', '--output',
                help="The output directory for which to show the bake record "
                     "(defaults to `_counter`)",
                nargs='?')
        parser.add_argument('-p', '--path',
                help="A pattern that will be used to filter the relative path "
                     "of entries to show.")

    def run(self, ctx):
        out_dir = ctx.args.output or os.path.join(ctx.app.root_dir, '_counter')
        record_cache = ctx.app.cache.getCache('baker')
        record_name = hashlib.md5(out_dir.encode('utf8')).hexdigest() + '.record'
        if not record_cache.has(record_name):
            raise Exception("No record has been created for this output path. "
                            "Did you bake there yet?")

        pattern = None
        if ctx.args.path:
            pattern = '*%s*' % ctx.args.path.strip('*')

        record = BakeRecord.load(record_cache.getCachePath(record_name))
        logging.info("Bake record for: %s" % record.out_dir)
        logging.info("Last baked: %s" %
                datetime.datetime.fromtimestamp(record.bake_time))
        logging.info("Entries:")
        for entry in record.entries:
            if pattern:
                rel_path = os.path.relpath(entry.path, ctx.app.root_dir)
                if not fnmatch.fnmatch(entry.rel_path, pattern):
                    continue
            logging.info(" - ")
            logging.info("   path:      %s" % entry.path)
            logging.info("   spec:      %s:%s" % (entry.source_name, entry.rel_path))
            logging.info("   taxonomy:  %s:%s" % (entry.taxonomy_name, entry.taxonomy_term))
            logging.info("   config:    %s" % entry.config)
            logging.info("   out URLs:  %s" % entry.out_uris)
            logging.info("   out paths: %s" % entry.out_paths)
            logging.info("   used srcs: %s" % entry.used_source_names)
            if entry.errors:
                logging.error("   errors: %s" % entry.errors)

