import os
from beets.plugins import BeetsPlugin
from beets.ui import Subcommand
from optparse import OptionParser
from confuse import ConfigSource, load_yaml
import beetsplug.ytimport.youtube
import beetsplug.ytimport.split
import subprocess

class YtImportPlugin(BeetsPlugin):
    def __init__(self):
        super(YtImportPlugin, self).__init__()
        config_file_path = os.path.join(os.path.dirname(__file__), 'config_default.yaml')
        source = ConfigSource(load_yaml(config_file_path) or {}, config_file_path)
        self.config.add(source)

    def commands(self):

        def run_import_cmd(lib, opts, args):
            ytdir = opts.directory
            urls = args
            headers = opts.auth_headers
            if headers:
                f = open(headers, 'r')
                headers = f.read()
                f.close()
            if opts.likes:
                print('Obtaining your liked songs from Youtube...')
                if not headers:
                    print('Using interactive authentication. To enable non-interactive authentication, set --auth-headers')
                auth = youtube.login(headers)
                likedIds = youtube.likes(auth, opts.max_likes)
                print('Found {:n} liked songs'.format(len(likedIds)))
                urls += ['https://www.youtube.com/watch?v='+id for id in likedIds]
            urls = [u for u in urls if not lib.items('comments:'+u)] # only new
            if urls:
                print('Downloading {:n} song(s) to {:s}'.format(len(urls), ytdir))
                h = {}
                # TODO: authenticate download requests.
                # The following makes download requests return a 400 reponse.
                # Maybe a cookiefile with some picked cookies from the headers can be generated?
                #if opts.auth and headers:
                #    h = dict([l.split(': ', 1) for l in headers.strip().split('\n')[1:]])
                youtube.download(urls, ytdir, min_len=opts.min_len, max_len=opts.max_len, auth_headers=h, split=opts.split_albums)
            else:
                print('Nothing to download')
            if opts.do_import:
                print('Importing downloaded songs into beets library')
                cmd = ['beet', 'import', ytdir, '-si', '--set', 'datasource=youtube']
                if opts.set:
                    cmd += ['--set', opts.set]
                if opts.quiet:
                    cmd += ['-q']
                if opts.pretend:
                    cmd += ['--pretend']
                subprocess.run(cmd)
            else:
                print('Skipping import')

        p = OptionParser()
        p.add_option('--directory', type='string',
            default=self.config['directory'].get(), \
            dest='directory', help='directory to download Youtube files to')
        p.add_option('--auth-headers', type='string',
            default=self.config['auth_headers'].get(), \
            dest='auth_headers', help="path to a file containing the HTTP headers of an authenticated POST request to music.youtube.com, copied from your browser's development tool")
        p.add_option('--likes', action='store_true',
            default=self.config['likes'].get(), \
            dest='likes', help='download liked songs')
        p.add_option('--nolikes', action='store_false',
            default=self.config['likes'].get(), \
            dest='likes', help="don't download liked songs")
        p.add_option('--max-likes', type='int',
            default=self.config['max_likes'].get(), \
            dest='max_likes', help='maximum number of likes to obtain')
        p.add_option('--split-albums', action='store_true',
            default=self.config['split_albums'].get(), \
            dest='split_albums', help='split albums into tracks')
        p.add_option('--nosplit-albums', action='store_false',
            default=self.config['split_albums'].get(), \
            dest='split_albums', help="don't split albums into tracks")
        p.add_option('--import', action='store_true',
            default=self.config['import'].get(), \
            dest='do_import', help='import downloaded songs into beets')
        p.add_option('--noimport', action='store_false',
            default=self.config['import'].get(), \
            dest='do_import', help="don't import downloaded songs into beets")
        p.add_option('--set', type='string',
            default=self.config['set'].get(), \
            dest='set', help='set a field on import, using FIELD=VALUE format')
        p.add_option('--min-len', type='int',
            default=self.config['min_len'].get(), \
            dest='min_len', help='minimum track length in seconds')
        p.add_option('--max-len', type='int',
            default=self.config['max_len'].get(), \
            dest='max_len', help='maximum track length in seconds')
        p.add_option('-q', '--quiet', action='store_true',
            default=False, \
            dest='quiet', help="don't prompt for input when importing")
        p.add_option('--pretend', action='store_true',
            default=False, \
            dest='pretend', help="don't import but print the files when importing")

        c = Subcommand('ytimport', parser=p, help='import songs from Youtube')
        c.func = run_import_cmd
        return [c]
