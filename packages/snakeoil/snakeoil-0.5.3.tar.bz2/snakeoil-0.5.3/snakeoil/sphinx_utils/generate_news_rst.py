#!/usr/bin/python
import errno
import os
import re
import sys


def regenerate_if_needed(project, src, out, release_extlink=None, git_extlink=None):
    cut_off = int(max(os.stat(x).st_mtime for x in [src,__file__]))
    try:
        if int(os.stat(out).st_mtime) >= cut_off:
            return
    except EnvironmentError, e:
        if e.errno != errno.ENOENT:
            raise
    print "regenerating %s news for %s -> %s" % (project, src, out)
    new_text = convert_news(open(src, 'r').read(), project, release_extlink, git_extlink)
    open(out, 'w').write(new_text)
    os.utime(out, (-1, cut_off))


def convert_news(text, project_name, release_extlink=None, git_extlink=None):
    project_name = project_name.strip()

    # First, escape all necessary characters so that since NEWS doesn't use true
    # ReST syntax.
    text = re.sub("\\\\", "\\\\", text)
    def f(match):
        return match.group(0).replace('_', '\_')
    #text = re.sub('((?:[^_]+_)+)(?=[;:.])', f, text)
    text = re.sub('_', '\\_', text)
    text = re.sub('(?<!\n)\*', '\\*', text)

    seen = set()

    def f(match):
        ver = match.group(1).strip()
        if ver == 'trunk':
            tag = 'master'
            char = '-'
        else:
            tag = 'v%s' % ver
            char = '+'
        date = match.group(2)
        s = ' '.join([project_name, ver])
        date = date.strip()
        # Ensure we leave a trailing and leading newline to keep ReST happy.
        l = ['']

        # Mangle any -rc2/_rc1/_p1 crap
        major = ver.replace('-', '.')
        major = major.replace('_', '.')
        major = '.'.join(major.split('.')[:2])
        if major not in seen:
            l += ['.. _release-latest-%s:' % major, '']
            if major != 'trunk':
                header = '%s %s releases' % (project_name, major)
                l += [header, '-' * len(header), '']
            seen.add(major)
        l += ['.. _release-%s:' % (ver,), '', s, char * len(s), '']

        l2 = []
        if date:
            l2.append("Released %s" % date.strip())
        if ver != 'trunk' and release_extlink is not None:
            l2.append(':%s:`Download<%s>`' % (release_extlink, ver))
        if git_extlink is not None:
            l2.append(':%s:`Git Shortlog<%s>`' % (git_extlink, tag))

        if l2:
            if date:
                l2[1:] = [(', '.join(l2[1:])) + '.']
            l.append('.  '.join(l2))
            l.append('')

        l.append('Notable changes:')
        l.append('')
        return '\n'.join(l)
    text = re.sub(r'(?:\n|^)%s +(\d+\.\d+[^:\s]*|trunk):?([^\n]*)(?:\n|$)' % (project_name,),
        f, text)
    return ".. _releases:\n\n%s" % (text,)


if __name__ == '__main__':
    if len(sys.argv) not in (4, 6):
        print "wrong args given; need project_name src out"
        sys.exit(1)
    regenerate_if_needed(*sys.argv[1:6])
