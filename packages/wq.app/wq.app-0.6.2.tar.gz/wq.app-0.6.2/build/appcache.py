import os
import re


def appcache(conf, indir, outdir, version):

    # Open output files
    s_acpath = indir + '/' + conf['name']
    b_acpath = outdir + '/' + conf['name']
    s_ac = open(s_acpath, 'w')
    b_ac = open(b_acpath, 'w')

    # Start in source directory - read @imports from main CSS file
    s_css = [conf['css']]
    s_css.extend(_parse_css_urls(indir, conf['css']))

    # Built CSS file contains image URLs from the @import-ed CSS files above
    images = _parse_css_urls(outdir, conf['css'])

    # build.txt contains a list of built javascript files and their sources
    s_js, b_js = _parse_js_buildfile(outdir + '/build.txt')

    b_css = [conf['css']]

    # Collect path names and create appcaches
    cache = list(conf['cache'])
    source_cache = cache + s_js + s_css + images
    built_cache = cache + b_js + b_css + images

    network = list(conf['network'])
    fallback = list(conf['fallback'])

    s_ac.write(APPCACHE_TMPL % {
        'version':  '%s_dev' % version,
        'cache':    '\n'.join(source_cache),
        'network':  '\n'.join(network),
        'fallback': '\n'.join(fallback)
    })
    b_ac.write(APPCACHE_TMPL % {
        'version':  version,
        'cache':    '\n'.join(built_cache),
        'network':  '\n'.join(network),
        'fallback': '\n'.join(fallback)
    })
    s_ac.close()
    b_ac.close()
    print "%s: %s items" % (s_acpath, len(source_cache + network + fallback))
    print "%s: %s items" % (b_acpath, len(built_cache + network + fallback))


def _parse_js_buildfile(filename):
    text = open(filename).read()
    sources = []
    built = []
    for group in text[1:].split('\n\n'):
        files = group.split('\n')

        if files[0][-2:] != 'js':
            continue
        sources.extend(files[2:])
        built.append(files[0])

    return sources, built


def _parse_css_urls(path, filename):
    cur = os.getcwd()
    os.chdir(path)
    text = open(filename).read()
    base = os.path.dirname(filename)

    def parse_url(url):
        if url.startswith('data:') or url.startswith('#'):
            return None
        if url.startswith('http://') or url.startswith('https://'):
            return url

        url = os.path.normpath(base + '/' + url)
        if os.sep != '/':
            url = url.replace(os.sep, '/')
        return url

    urls = []
    for line in text.split('\n'):
        m = re.search(r"url\(['\" ]*(.+?)['\" ]*\)", line)
        if m:
            url = parse_url(m.group(1))
            if url:
                urls.append(url)
    os.chdir(cur)
    return urls

APPCACHE_TMPL = """CACHE MANIFEST

# Version %(version)s

CACHE:
%(cache)s

NETWORK:
%(network)s

FALLBACK:
%(fallback)s
"""
